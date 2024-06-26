import os
import pytest
import tempfile
from subprocess import CalledProcessError
from utils import run_inside_dir

BASE_TEMPLATE_URL = "https://github.com/ADACS-Australia/adacs_template_python_base"


@pytest.fixture(scope="session")
def base_template_path():
    with tempfile.TemporaryDirectory() as path_temp:
        try:
            result = run_inside_dir(f"git clone {BASE_TEMPLATE_URL}", path_temp)
            if result != 0:
                raise CalledProcessError(
                    "Failed to clone base repo.  Are you connected to a network?"
                )
        except CalledProcessError as e:
            pytest.fail(str(e))
        path_template = path_temp + f"/{os.path.basename(BASE_TEMPLATE_URL)}"
        yield path_template
