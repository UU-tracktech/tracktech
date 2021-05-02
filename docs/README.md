# Documentation

documentation.py generates documentation for Python modules using pdoc.
Modules can be excluded for documentation generation, and 
the templating of the documentation can be adjusted via the Jinja2 templates.

## How to run

- Install requirements from docs/requirements.txt
- Run documentation.py from project root (located in docs) with the following command: 
  `python docs/documentation.py [-ci] [-rs code_path1 code_path2 etc]`
  - `-ci` (or `--create-index`): if flag is present, generates index page with links to all documentation index files.
  - `-rs` (or `roots`): defaults to empty list.
    Contains all arguments provided after flag as code paths to start documentation generation at.

## Constraints

- pdoc runs the global code of each module included in the documentation generation. 
  This brings some issues with it since this global code can throw errors. 
  The global code includes import statements, statements in global space, 
  class inheritance (thus requiring the super class), 
  and class constants.
  Some of these issues imposed by pdoc have built-in solutions, others need to be prevented.
  - Imports: packages must be installed if they are necessary for the other mentioned issues. 
    However documentation automatically creates a mock object for all modules that haven't been loaded in 
    or will not have documentation generated for the module.
    This also means that a mock is created for a project module if a module is ignored from documentation via __all__.
  - Global space: code can be run in the global space if they have no required configuration 
    and all necessary packages are installed in the Python interpreter.
  - Class inheritance: the super class of a certain class must be included in the loaded modules. 
    This is necessary for pdoc inheritance checks.
    This requires the Python interpreter to have the package installed if a class of it is used as super class.
    An example is the WebsocketHandler of tornado, this is the super class of all Websocket classes in this project.
  - Class constants: ensure that the constants can be initialized 
    without additional project configuration not handled before pdoc execution.
