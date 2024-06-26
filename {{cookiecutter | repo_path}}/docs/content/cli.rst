{{ [cookiecutter | package_name,' CLI Documentation'] | join | underline('=') }}

This package provides a CLI interface through which common tasks can be accomplished.

.. click:: {{ cookiecutter | package_name }}.cli:cli
   :prog: {{ cookiecutter | package_name }}
   :show-nested:
