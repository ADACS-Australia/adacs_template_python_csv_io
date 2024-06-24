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


def add_entry_to_docs_toc(entry: str) -> None:
    """Add an entry to the documentation index.rst for the cli.rst content we are adding"""


    def indent_entry(indent:int) -> str:
        return " "*indent + entry

    # Re-write the index.rst file with the given line added
    with fileinput.input(files="{{cookiecutter | repo_path}}/docs/index.rst", inplace=True) as file:
        flag_toc_found = False
        flag_options_done = False
        flag_update_done = False
        indent = 0
        for i_line, line_in in enumerate(file):
            line_in_strip = line_in.strip()
            line_in_lstrip = line_in.lstrip(' ')
            line_in_length = len(line_in_strip)
            line_in_indent = len(line_in) - len(line_in_lstrip)
            line_out = line_in # re-write line unchanged by default
            if line_in_length>0 and not flag_update_done:
                # Don't modify until we find the TOC block
                if not flag_toc_found:
                    if line_in_strip.startswith(".. toctree"):
                        flag_toc_found = True
                # ... once we have, don't modify until after the end of the parameter block ...
                elif not flag_options_done:
                    if not indent:
                        indent = line_in_indent
                    elif indent != line_in_indent:
                        raise Exception(f"Indentation error at line {i_line}: {line_in_indent} spaces instead of {indent}; line_length={line_in_length}.")
                    flag_line_is_option = line_in_strip.startswith(":")
                    if not flag_line_is_option:
                        flag_options_done = True
                # ... don't modify anything before the end of the parameter block or after we have written the new entry
                if flag_options_done and not flag_update_done:
                    if line_in_indent==0:
                        line_out = indent_entry(indent) + os.linesep + line_in
                        flag_update_done = True
            elif flag_options_done and not flag_update_done:
                line_out = indent_entry(indent) + os.linesep + line_in
                flag_update_done = True

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
    add_entry_to_docs_toc("CLI Documentation <content/cli.rst>")
    print_instructions()
