# Documentation

documentation.py generates documentation for Python modules using pdoc.
Modules can be excluded for documentation generation, and the templating of the documentation can be adjusted via the Jinja2 templates.

## How to run

- Install requirements from docs/requirements.txt
- Run documentation.py from project root (located in docs) with the following command: 
  `python docs/documentation.py [-ci] [-rs code_path1 code_path2 etc]`
  - `-ci` (or `--create-index`): if flag is present, generates index page with links to all documentation index files.
  - `-rs` (or `roots`): defaults to empty list.
    Contains all arguments provided after flag as code paths to start documentation generation at.

## Exclude Python file from documentation generation

You can exclude certain Python files from documentation generation by adding the `__all__` attribute.
The `__all__` attribute must reside in the `__init__.py` file, 
every module name in `__all__`. gets documentation, 
and every module name not in it gets excluded.


## Constraints

- pdoc runs the global code of each module included in the documentation generation. 
  This brings some issues with it since this global code can throw errors. 
  The global code includes import statements, statements in global space, 
  class inheritance (thus requiring the superclass), 
  and class constants.
  Some of these issues imposed by pdoc have built-in solutions; others need to be prevented.
  - Imports: packages must be installed if they are necessary for the other mentioned issues. 
    However, documentation automatically creates a mock object for all modules that haven't been loaded in 
    or will not have documentation generated for the module.
    This also means that a mock is created for a project module if a module is ignored from documentation via `__all__`.
  - Global space: code can be run in the global space if they have no required configuration and all necessary packages are installed in the Python interpreter.
  - Class inheritance: the superclass of a specific class must be included in the loaded modules. 
    This is necessary for pdoc inheritance checks.
    This requires the Python interpreter to have the package installed if a class of it is used as superclass.
    An example is the WebsocketHandler of Tornado. This is the superclass of all WebSocket classes in this project.
    Another example is using a class from src code as superclass in testing code; this would crash the documentation generation.  
  - Class constants: ensure that the constants can be initialized without additional project configuration not handled before pdoc execution.
- Init files: when an `__init__.py` contains imports or code with side effects. 
  You must include the imports (or remove the side effects) in your Python environment to respect the `__all__` property.
  An `__init__.py` that at most contains attributes (like `__all__`) and documentation is preferred.
