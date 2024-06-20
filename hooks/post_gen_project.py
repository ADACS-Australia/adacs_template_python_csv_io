import fileinput
import os
import subprocess
import tomlkit

# Rich is a cookiecutter dependency, so these should be safe here
from rich.console import Console
from rich.markdown import Markdown


def update_pyproject_toml() -> None:
    """ Add to the pyproject.toml file an entry of the form:
    [tool.poetry.scripts]
    my_exe_name = "my_package_name.cli:cli"
    """

    # Read pyproject.toml file
    with open("pyproject.toml", "r") as fp:
        pyproject_toml = tomlkit.load(fp)

    # Add CLI item to tool.poetry.scripts
    key = "{{ cookiecutter | package_name }}"
    val = "{{ cookiecutter | package_name }}.cli:cli"
    if not 'scripts' in pyproject_toml['tool']['poetry'].keys():
        tab = tomlkit.table()
        tab.add(key, val)
        pyproject_toml['tool']['poetry']['scripts'] = tab
    else:
        pyproject_toml['tool']['poetry']['scripts'][key] = val

    # Re-write pyproject.toml file
    with open("pyproject.toml", "w") as fp:
        tomlkit.dump(pyproject_toml, fp)

    pass


def update_documentation() -> None:
   """Add an entry to the documentation index.rst for the cli.rst content we are adding"""

   # Seatch to the place we want to add content.
   with fileinput.input(files="{{cookiecutter | repo_path}}/docs/index.rst", inplace=True) as file:
       for line_in in file:
           if line_in.startswith("   Home <self>"):
               line_out = line_in + "   CLI Documentation <content/cli.rst>" + os.linesep
           else:
               line_out = line_in
           print(line_out, end='')


def print_instructions() -> None:
    """Print instructions about how to configure the rendered project for use"""

    # Read the instructions file, ignoring lines that start with '***'
    with open("INSTRUCTIONS.template", "r") as file:

        # Add a notification that the rendering is complete to the instructions being written
        lines = "# Rendering Complete"

        line_in = file.readline()
        while line_in:
            if line_in[0:2] != "//":
                lines = lines + line_in
            line_in = file.readline()

    # Render the file as Markdown with Rich
    console = Console()
    console.print(Markdown(lines))


if __name__ == "__main__":
    update_pyproject_toml()
    update_documentation()
    print_instructions()
