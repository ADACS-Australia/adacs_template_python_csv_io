#############
# Base image
#############
FROM python:3.11-buster

ENV HOME=/home/pytest \
    USERNAME=pytest

RUN pip install poetry==1.4.2

RUN mkdir -p ${HOME} && \
    useradd --home-dir ${HOME} ${USERNAME} && \
    chown ${USERNAME} ${HOME}

#############################################################
# Switch to the user that we just created.  In what follows,
# we set-up their runtime environment.
#############################################################
USER ${USERNAME}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV PACKAGE_ROOT ${HOME}/package

WORKDIR ${HOME}

################
# Configure git 
################
RUN git config --global user.email "docker@test.com"
RUN git config --global user.name "Docker test"

RUN poetry config virtualenvs.create false && \
    python -m virtualenv venv && \
    . venv/bin/activate

################################################################
# Copy and install Poetry dependencies (but not the actual 
# application, which will get installed by the entry_point 
# script when we start the container)
################################################################
COPY pyproject.toml poetry.lock .
RUN . venv/bin/activate && \
    poetry install --no-root --compile && \
    rm -rf ${POETRY_CACHE_DIR} && \
    rm pyproject.toml && \
    mv poetry.lock ${HOME}/poetry.lock.image

##########################
# Set-up the entry script
##########################
RUN touch entry_script.sh
RUN chmod a+rx entry_script.sh
RUN echo \
'#!/bin/bash \n\
if ! test -d ${PACKAGE_ROOT} ; then\n\
  echo "The project directory has not been mounted properly.  Please run the container with: docker run -v $""PWD:"${PACKAGE_ROOT}" etc."\n\
  exit 1\n\
fi\n\
if ! cmp -s ${HOME}/poetry.lock.image ${PACKAGE_ROOT}/poetry.lock ; then\n\
  echo poetry.lock has been updated since the image was built.  Please rebuild it and try again.\n\
  exit 1\n\
fi\n\
cd ${HOME}\n\
. venv/bin/activate\n\
cd ${PACKAGE_ROOT}\n\
\n\
poetry install --only-root\n\
echo\n\
echo "A:"${TEST_ROOT}\n\
ls -la ${HOME}/venv/bin/\n\
echo "B:"\n\
ls -la ${HOME}/package\n\
echo "C:"\n\
pwd\n\
ls\n\
echo\n\
pytest' \
>> entry_script.sh
