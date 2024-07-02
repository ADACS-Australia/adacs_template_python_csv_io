import os
import pytest
import tempfile
from subprocess import CalledProcessError
from utils import run_inside_dir
from test_parameter_grid import test_these_changes_to_default_parameters
from utils import bake_in_temp_dir

# Check to see if a local repo is indicated by the environment, or use the GitHub repo
# (this is useful for workflows where we don't have to deal with identity when cloning the repo for testing)
BASE_TEMPLATE_LOCATION = (
    os.getenv("BASE_TEMPLATE_PATH")
    or "https://github.com/ADACS-Australia/adacs_template_python_base"
)


@pytest.fixture(scope="session")
def base_template_path():
    with tempfile.TemporaryDirectory() as path_temp:
        try:
            result = run_inside_dir(f"git clone {BASE_TEMPLATE_LOCATION}", path_temp)
            if result != 0:
                raise CalledProcessError(
                    "Failed to clone base repo.  Are you connected to a network?"
                )
        except CalledProcessError as e:
            pytest.fail(str(e))
        path_template = path_temp + f"/{os.path.basename(BASE_TEMPLATE_LOCATION)}"
        yield path_template


@pytest.fixture(params=test_these_changes_to_default_parameters)
def bake_path(cookies, base_template_path, request):
    extra_context_base = request.param[0]
    extra_context_template = request.param[1]
    exit_code_expected = request.param[2]
    exception_expected = request.param[3]
    with bake_in_temp_dir(
        cookies,
        base_template_path,
        extra_context_base=extra_context_base,
        extra_context_template=extra_context_template,
    ) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == exit_code_expected
        assert result.exception is exception_expected
        yield result.project_path
