import fileinput
import os
import subprocess
import tomlkit
from typing import List

# Rich is a cookiecutter dependency, so these should be safe here
from rich.console import Console
from rich.markdown import Markdown


class DocsUpdateException(Exception):
    """Exception raised when an error is encountered during a documentation update."""

    def __init__(self, message: str):
        self._message = message

    def __str__(self) -> str:
        return f"{self._message}"


def update_pyproject_toml(destination_table: List, key: str,val: str) -> None:
    """ Add to the pyproject.toml file an entry of the form:
    [tool.poetry.scripts]
    my_exe_name = "my_package_name.cli:cli"
    """

    # Read pyproject.toml file
    with open("pyproject.toml", "r") as fp:
        pyproject_toml = tomlkit.load(fp)

    # Make sure the destination table exists
    check_table = pyproject_toml
    for level in destination_table:
        if not level in check_table.keys():
            tab = tomlkit.table()
            tab.add(key, val)
            check_table[level] = tab
        check_table = check_table[level]

    # Add the entry
    check_table[key] = val

    # Re-write pyproject.toml file
    with open("pyproject.toml", "w") as fp:
        tomlkit.dump(pyproject_toml, fp)

    pass


def add_entry_to_docs_toc(entry: str) -> None:
    """Add an entry to the documentation index.rst for the cli.rst content we are adding"""


    def indent_entry(indent:int) -> str:
        return " "*indent + entry

    def write_toc(buffer: List) -> None:

        # Find the last non-empty line and determine the indent being used
        last_line_index=0
        indent = -1
        for i_line,line in enumerate(buffer):
            if len(line.strip())>0:
                last_line_index=i_line
                # Determine the indent
                line_indent = len(line) - len(line.lstrip())
                if indent < 0:
                    if line_indent > 0:
                        indent = line_indent
                elif indent!=line_indent and line_indent>0:
                    raise DocsUpdateException(f"Indentation error at TOC line {i_line+1}: {line_indent} spaces instead of {indent}")

        # Sanity checks
        if indent <=0:
            raise DocsUpdateException(f"Indentation error in TOC: invalid indent of {indent} determined.")

        # Insert new line into buffer, after last non-empty line
        buffer[last_line_index] = buffer[last_line_index] + indent_entry(indent) + os.linesep

        # Write the buffer
        for line in buffer:
            print(line, end='')

    # Re-write the index.rst file with the given line added
    filename="{{cookiecutter | repo_path}}/docs/index.rst"
    try:
        with fileinput.input(files=filename, inplace=True, backup='.bak') as file:
            flag_processing_toc = False
            flag_update_done = False
            indent = 0
            buffer = []
            for i_line, line_in in enumerate(file):
                line_in_strip = line_in.strip()
                line_in_lstrip = line_in.lstrip(' ')
                line_in_length = len(line_in_strip)
                line_in_indent = len(line_in) - len(line_in_lstrip)
                line_out = line_in # re-write line unchanged by default
                if line_in_length>0:
                    if line_in_strip.startswith(".."):
                        if line_in_strip.lstrip(". ").startswith("toctree"):
                            if flag_processing_toc:
                                raise DocsUpdateException(f"Multiple insert points found in '{filename}.'")
                            flag_processing_toc = True
                        else:
                            if flag_processing_toc:
                                if flag_update_done:
                                    raise DocsUpdateException(f"Multiple insert points found in '{filename}.'")
                                write_toc(buffer)
                                flag_update_done = True
                            flag_processing_toc = False
                    elif line_in_indent==0:
                        # If we were reading the toc but aren't now, write the modified toc
                        if flag_processing_toc:
                            if flag_update_done:
                                raise DocsUpdateException(f"Multiple insert points found in '{filename}.'")
                            write_toc(buffer)
                            flag_update_done = True
                        flag_processing_toc = False
                if flag_processing_toc:
                    buffer.append(line_in)
                else:
                    print(line_out, end='')
    except DocsUpdateException as e:
        os.remove(filename)
        os.rename(filename + ".bak", filename)
        raise DocsUpdateException("Could not update documentation.  File left unchanged.") from e
    else:
        os.remove(filename + ".bak")



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
    if not {{ cookiecutter.__test }}:
        console.print(Markdown(lines))


if __name__ == "__main__":
    update_pyproject_toml(['tool','poetry','scripts'], 
                          "{{ cookiecutter | package_name }}",
                          "{{ cookiecutter | package_name }}.cli:cli")
    add_entry_to_docs_toc("CLI Documentation <content/cli.rst>")
    print_instructions()
