from utils import bake_in_temp_dir
import pathlib


def test_for_files_in_default_build(cookies, base_template_path):

    with bake_in_temp_dir(cookies, base_template_path) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        # List of filenames that need to be present in a properly rendered template

        # Filenames from base template
        package_name = result.context["__package_name"]
        check_toplevel_pathnames_base = [
            ".git",
            "pyproject.toml",
            "docs/index.rst",
            f"python/{package_name}/__init__.py",
        ]

        # Filenames from base template
        check_toplevel_pathnames_template = [
            f"python/{package_name}/cli.py",
            f"python/{package_name}/files.py",
            f"python/{package_name}/lines.py",
        ]

        # Get a list of paths in the project, excluding those that are within the git directory
        found_toplevel_pathnames = set()
        root_dir = result.project_path
        git_path = root_dir / ".git"
        for path_i in root_dir.rglob("*"):
            if git_path not in path_i.parents:
                found_toplevel_pathnames.add(path_i)
            else:
                found_toplevel_pathnames.add(git_path)

        # Check that the needed files from the base project are present
        for path_i in check_toplevel_pathnames_base:
            assert root_dir / pathlib.Path(path_i) in found_toplevel_pathnames

        # Check that the needed files from this template are present
        for path_i in check_toplevel_pathnames_template:
            assert root_dir / pathlib.Path(path_i) in found_toplevel_pathnames
