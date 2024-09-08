<p align="center">
  <img src="https://github.com/ADACS-Australia/adacs_template_python_base/blob/main/docs/assets/adacs_logo.png?raw=true" alt="ADACS Logo">
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3110/">
    <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python 3.11">
  </a>
  <a href='https://adacs-csv-io-python-template.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/adacs-csv-io-python-template/badge/?version=latest' alt='Documentation Status' />
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  </a>
</p>

# This template will ...

**... add a CSV I/O workflow to your ADACS Template project.**

## Getting Started

1. ***Make sure you have started a new Python project with the Base ADACS Python template***

``` console
cookiecutter gh:ADACS-Australia/adacs_template_python_base
```

See the [Base ADACS Python Template page](https://github.com/ADACS-Australia/adacs_template_python_base) for detailed instructions.

2. ***Ensure that any changes in the project have been committed***

``` console
cd PROJECT_ROOT_DIRECTORY
```
``` console
git add .
git commit -m "Your commit message."
```

3. ***Create and checkout a new branch to add the code to***

``` console
git checkout -b feature/add-a-csv-io-workflow
```

4. ***Make sure all required Python dependencies are installed***

This template has a Python dependency (on `tomlkit`) that needs to be installed before running `cookiecutter`.  If you are running `cookiecutter` via `pipx` (recommended), this can be achieved as
follows:
``` console
pipx inject cookiecutter tomlkit
```

Otherwise, install it into the environment you are running `cookiecutter` from as follow:
``` console
pip install tomlkit
```

5. ***Render this template on top of the project***

``` console
cookiecutter -f gh:ADACS-Australia/adacs_template_python_csv_io
```
... giving the path (relative or absolute) to the project when prompted (`.` if you are currently in the root directory)

6. ***Commit these changes to the repository***

Look at the changes that have been made, modify them as you see fit, and then commit them to the repo:
``` console
git add .
git commit -m "Add a CSV I/O workflow."
```

7. ***Add the code to the main branch so others can use it***

Push the new (current) branch to *GitHub*:
``` console
git push -u origin HEAD
```

... and create/merge a PR to incorporate the code into the main branch.

## What do you get for this?
1. A simple and fully tested ASCII file read/process/write workflow
2. A CLI interface, providing simple and self-documenting terminal access to the codebase for your users
