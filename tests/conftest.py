import os
import pytest
import tempfile
from utils import run_inside_dir

BASE_TEMPLATE_URL = "https://github.com/ADACS-Australia/adacs_template_python_base"


@pytest.fixture(scope="session")
def base_template_path():
    with tempfile.TemporaryDirectory() as path_temp:
        run_inside_dir(f"git clone {BASE_TEMPLATE_URL}", path_temp)
        path_template = path_temp + f"/{os.path.basename(BASE_TEMPLATE_URL)}"
        yield path_template
