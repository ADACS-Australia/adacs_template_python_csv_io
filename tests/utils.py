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
def bake_in_temp_dir(
    cookies: Cookies,
    base_template_path,
    extra_context_base={},
    extra_context_template={},
):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """

    # Silence printing of base instructions
    extra_context_base["__test"] = True

    print("XXXXXXXXXXX:", type(base_template_path), base_template_path)

    # Bake the base template
    result = cookies.bake(
        template=base_template_path,
        extra_context=extra_context_base,
    )

    # This is the place for any logic that affects the context of the template being tested
    extra_context_template["repo_path"] = result.context["repo_name"]

    # Bake this template on top of the base template
    cookiecutter(
        "./",
        extra_context=extra_context_template,
        no_input=True,
        output_dir=result.project_path.parent,
        overwrite_if_exists=True,
    )

    # Check for error, yield the result on success and clean-up afterward
    if not result.project_path:
        raise OSError("Could not bake project.")
    try:
        yield result
    finally:
        rmtree(str(result.project_path))
