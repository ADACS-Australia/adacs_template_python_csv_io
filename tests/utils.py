from contextlib import contextmanager
import shlex
import os
import subprocess
from pathlib import Path
from cookiecutter.utils import rmtree
from pytest_cookies.plugin import Cookies, Result
from cookiecutter.main import cookiecutter


def run_inside_dir(command: str, path: Path):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param path: String, path of the directory the command is being run.
    """
    with inside_dir(path):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command: str, path: Path):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(path):
        return subprocess.check_output(shlex.split(command))


def project_info(result: Result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_slug = result.project_path.name
    project_dir = result.project_path / project_slug
    return str(result.project_path), str(project_slug), str(project_dir)


@contextmanager
def inside_dir(path: Path):
    """
    Execute code from inside the given directory
    :param path: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies: Cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """

    # Bake the base template
    result = cookies.bake(
        *args, **kwargs, template="/Users/gpoole/my_code/adacs_python_template"
    )

    # Bake this template on top of the base template
    cookiecutter(
        "./",
        no_input=True,
        output_dir=result.project_path.parent,
        overwrite_if_exists=True,
    )

    import os

    print(os.listdir(result.project_path))

    # Check for error, yield the result on success and clean-up afterward
    if not result.project_path:
        raise OSError("Could not bake project.")
    try:
        yield result
    finally:
        rmtree(str(result.project_path))
