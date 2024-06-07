from utils import bake_in_temp_dir


def test_bake_with_defaults(cookies):

    # List of filenames that need to be present in a properly rendered template
    check_toplevel_pathnames = [
        ".git",
        ".github",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".pre-commit-db.json",
        ".readthedocs.yml",
        "LICENSE",
        "README.md",
        "docs",
        "pyproject.toml",
        "python",
    ]

    with bake_in_temp_dir(cookies, extra_context={"__test": True}) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_pathnames = [
            path_i.name for path_i in result.project_path.iterdir()
        ]

        for filename_i in check_toplevel_pathnames:
            assert filename_i in found_toplevel_pathnames
