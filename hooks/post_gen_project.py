import subprocess

# Rich is a cookiecutter dependency, so these should be safe here
from rich.console import Console
from rich.markdown import Markdown


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
    {% raw %}
    # venv("{{ cookiecutter.virtual_environment }}")
    # install("{{ cookiecutter.virtual_environment }}")
    {% endraw %}
    print_instructions()
