import pytest
from utils import bake_in_temp_dir, run_inside_dir

# Each entry in this list should have:
#   1. a dict of base template parameter changes
#   2. a dict of this template's parameter changes
#   3. the expected exit code
#   4. the exoected exception
test_these_changes_to_default_parameters = [
    ({"author": "O'connor"}, {}, 0, None),
    ({"author": 'name "quote" name'}, {}, 0, None),
    ({"author": "Last, First"}, {}, 0, None),
    ({"project_name": "something-with-a-dash"}, {}, 0, None),
    ({"project_name": "something with a space"}, {}, 0, None),
]


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


def test_bake_and_run_tests(bake_path):
    assert run_inside_dir("pytest", bake_path) == 0


def test_template_make_docs(bake_path):
    assert run_inside_dir("make docs", bake_path) == 0


def test_template_run_black(bake_path):
    assert run_inside_dir("black .", bake_path) == 0


def test_template_run_ruff(bake_path):
    assert run_inside_dir("ruff .", bake_path) == 0
