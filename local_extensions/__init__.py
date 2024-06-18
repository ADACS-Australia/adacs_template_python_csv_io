import datetime
import os
import tomlkit
import pathlib
from re import sub
from collections import OrderedDict
from jinja2.ext import Extension
from jinja2.environment import Environment


class ProjectMetaData(object):

    # @functools.lru_cache(typed=True) # would be nice to use this but OrderedDict is not hashable
    def __init__(self, cookiecutter: OrderedDict):
        self.output_path = pathlib.Path(cookiecutter["_output_dir"])
        self.repo_name = self.output_path.parts[-1]
        self.repo_path = pathlib.Path(cookiecutter["repo_path"])
        if not os.path.isabs(cookiecutter["repo_path"]):
            self.repo_path = self.output_path / self.repo_path

        # Read pyproject.toml file
        with open(f"{self.repo_path}/pyproject.toml", "r") as fp:
            pyproject_toml = tomlkit.load(fp)

        packages = pyproject_toml["tool"]["poetry"]["packages"]
        if len(packages) != 1:
            raise ValueError(
                "The repo you've given has something other than 1 package.  Don't know what to do with this."
            )

        self.package_name = packages[0]["include"]


class ParsePathExtension(Extension):
    """Jinja2 extension to parse information (e.g. package name, repo name, etc.) from the the repo path."""

    def __init__(self, environment: Environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def repo_path(cookiecutter: OrderedDict) -> str:
            """Parse the repo path from the cookiecutter object

            Parameters
            ----------
            cookiecutter : OrderedDict
                Cookiecutter object

            Returns
            -------
            str
                Repo path as a string
            """

            meta = ProjectMetaData(cookiecutter)

            return str(meta.repo_path)

        def repo_name(cookiecutter: OrderedDict) -> str:
            """Parse the repo name from the cookiecutter object

            Parameters
            ----------
            cookiecutter : OrderedDict
                Cookiecutter object

            Returns
            -------
            str
                Repo name as a string
            """

            meta = ProjectMetaData(cookiecutter)

            return str(meta.repo_name)

        def package_name(cookiecutter: OrderedDict) -> str:
            """Parse the package name from the repo path

            Parameters
            ----------
            path : str
                Path as a string

            Returns
            -------
            str
                Package name as a string
            """

            meta = ProjectMetaData(cookiecutter)

            return meta.package_name

            return package_name

        environment.filters.update({"repo_path": repo_path})
        environment.filters.update({"repo_name": repo_name})
        environment.filters.update({"package_name": package_name})


class CurrentYearExtension(Extension):
    """Jinja2 extension to return the current year as a string."""

    def __init__(self, environment: Environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        environment.globals.update({"current_year": datetime.datetime.utcnow().year})


class UnderlineExtension(Extension):
    """Jinja2 extension to return an underlined version of a string."""

    def __init__(self, environment: Environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def underline(s: str, char_ul: str = "-") -> str:
            """Create an underlined version of a string

            Parameters
            ----------
            s : str
                String to underline
            char_ul : str
                Character to underline with (default: '-')

            Returns
            -------
            str
                Underlined string
            """
            return f"{s}\n{char_ul*len(s)}"

        environment.filters.update({"underline": underline})


class PascalCaseExtension(Extension):
    """Jinja2 extension to return a Pascal Case version of a string."""

    def __init__(self, environment: Environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def pascal_case(s: str) -> str:
            """Create a Pascal Case version of a string

            Parameters
            ----------
            s : str
                String to reformat

            Returns
            -------
            str
                Reformated string
            """
            return "".join(sub(r"(_|-)+", " ", s).title().replace(" ", ""))

        environment.filters.update({"pascal_case": pascal_case})


class EscapeQuotes(Extension):
    """Jinja2 extension to return a version of a string with escape-encoded quotes."""

    def __init__(self, environment: Environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def escape_quotes(s: str) -> str:
            """Create a version of a string with escape-encoded quotes

            Parameters
            ----------
            s : str
                String to encode

            Returns
            -------
            str
                Encoded string
            """
            return s.replace('"', r"\"")

        environment.filters.update({"escape_quotes": escape_quotes})
