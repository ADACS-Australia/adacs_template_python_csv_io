# Looking to add some code for processing Comma-Separated Value (CSV) files to your ADACS templated Python project?
This template takes the effort out of starting from a good place.

## Getting Started
***Make sure you have started a new Python project with the Base ADACS Python template***
``` console
cookiecutter gh:ADACS-Australia/adacs_template_python_base
```

See the [Base ADACS Python Template page](https://github.com/ADACS-Australia/adacs_template_python_base) for detailed instructions.

***...render this template on top of it...***
``` console
cookiecutter -f gh:ADACS-Australia/adacs_template_python_csv_io
```
Make sure any changes to your project have been committed first.

***...give the path to your previously rendered Base Template project (absolute or relative), look at the changes that have been made, modify them as you see fit, and then commit them to the repository.***

## What do you get for this?
***A codebase that eases collaboration and automatically:***
* A simple ASCII file read/process/write workflow
* A CLI interface, providing simple and self-documenting terminal access to the codebase for your users
