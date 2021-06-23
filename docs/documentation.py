"""Generate the documentation using PDOC and jinja templating.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import sys
import argparse
import logging
from pathlib import Path
import dis
import importlib
import importlib.util
import shutil
import pkgutil
import pkg_resources
import pdoc
import mock


def generate_documentation(component_source_path):
    """Generates PDOC documentation for all Python modules in given Python source path.

    Removes the previously created documentation if it exists.

    Args:
        component_source_path (Path): path to root folder of Python code.
    """
    doc_folder = os.path.dirname(__file__)
    abs_component_source_path = os.path.realpath(os.path.join(os.path.dirname(doc_folder), component_source_path))
    component_root = os.path.dirname(abs_component_source_path)

    # Points pdoc to used jinja2 template and sets Google docstrings as the used docstring format.
    pdoc.render.configure(template_directory=Path(os.path.realpath(os.path.join(doc_folder, 'template'))),
                          docformat='google')

    # Add to_tree to Jinja2 environment filters to generate tree from modules list.
    pdoc.render.env.filters['to_tree'] = to_tree

    # Output directory.
    output_dir = Path(os.path.realpath(os.path.join(doc_folder, 'html', component_source_path)))

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Create docs html dir if it doesn't exist.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all modules included by pdoc, respecting the __all__ attribute in __init__.py.
    included_paths = get_modules(abs_component_source_path)

    # Create module imports from included paths.
    included_modules = [path_to_module(component_root, included_path) for included_path in included_paths]
    logging.info(f'Included modules: {included_modules}')

    # Remove modules for which pdoc is going to generate documentation.
    for module in included_modules:
        if module in sys.modules:
            logging.info(f'Removed the following module so it can generate documentation: {module}')
            del sys.modules[module]

    # Get modules that might need to get mocked.
    mock_modules = get_mock_modules(included_paths, included_modules)
    logging.info(f'Mocked modules: {mock_modules}')

    # Get modules that have been mocked.
    mocked_modules = get_mocked(mock_modules)

    # Generate documentation for all found modules in the /docs.
    pdoc.pdoc(abs_component_source_path, output_directory=output_dir)

    logging.info('Cleaning up the mocked modules')

    # Remove mocked modules.
    for module in mocked_modules:
        del sys.modules[module]


def generate_index():
    """Generate index.html file that links to all generated HTML in sub-folders.
    """
    html_root = os.path.join(os.path.dirname(__file__), 'html')

    index_loc = os.path.join(html_root, 'index.html')

    # Removes the current index.html to later generate it anew.
    # Must be removed before searching to prevent conflicting finds.
    if os.path.exists(index_loc):
        os.remove(index_loc)

    index_paths = []

    for path, sub_dirs, files in os.walk(html_root):
        if 'index.html' in files:
            index_paths.append(os.path.join(path, 'index.html').replace(html_root, '', 1).replace('\\', '/'))

            # Stop walking into sub_dirs, index has already been found in current branch.
            sub_dirs[:] = []

    with open(index_loc, 'w') as index_file:
        index_file.write('<style>')
        index_file.write('body{background-color: #212529;color:#f7f7f7;font-family:system-ui,-apple-system,"Segoe UI",'
                         'Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif,"Apple Color Emoji",'
                         '"Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";}')
        index_file.write('a{background-color:rgb(51, 51, 51);color:#f7f7f7;margin:.1rem;padding:.1rem.5rem;'
                         'box-sizing: border-box;text-decoration: none;margin-bottom:2px;display:inline-block}')
        index_file.write('</style>')

        for index_path in index_paths:
            index_file.write(f'&mdash;<a href=".{index_path}">{index_path.replace("/index.html","")[1:]}</a>\n<br>\n')


def get_imports(file_path):
    """Get all import names from import statements used in the Python file located at file_path.

    Args:
        file_path (str): path to the module, can be the python file, or dir name containing an __init__.py.

    Returns:
        List[str]: list of import names.
    """
    # Check if Python module exists and form path to open module.
    if file_path.endswith('.py') and Path.exists(Path(file_path)):
        py_file_path = file_path
    elif Path.exists(Path(f'{file_path}.py')):
        py_file_path = f'{file_path}.py'
    elif Path.exists(Path(f'{file_path}/__init__.py')):
        py_file_path = f'{file_path}/__init__.py'
    else:
        raise FileNotFoundError(f'Python module not found in file: {file_path}')

    # Open Python file as if it is a normal file.
    file = open(Path(py_file_path), encoding='UTF-8')

    # Get all instructions in Python file.
    instructions = dis.get_instructions(file.read())

    # Filter on IMPORT_NAME.
    instruction_names = ['IMPORT_NAME']

    # Argval of allowed instruction arguments.
    imports = [instruction.argval for instruction in instructions if instruction.opname in instruction_names]

    return imports


def get_modules(root_folder):
    """Gets all modules starting from the top folder, excludes Python modules that are deemed as hidden.

    Gets all modules starting from the top folder given as root_folder.
    Starts by searching for all sub folders of the root folder,
    excluding folders starting with '.' or '_'.
    Looks for modules in all found folders (root_folder + both direct and indirect sub folders).

    Args:
        root_folder (str): root folder to look through modules at current level and in the sub folders

    Returns:
        list[str]: list of all Python modules located in root_folder and its sub folders
    """
    # Append root_folder dirname to sys.path to import modules.
    component_root = os.path.dirname(root_folder)
    sys.path.append(component_root)

    # Find all sub folders that do not start with '.' or '_', starting at the root_folder.
    folders = [root_folder]
    add_submodule_to_folders(folders)

    includes = dict()

    for iter_folder in folders:
        # Import all packages to retrieve the __all__ attribute (if there is one).
        for module in pkgutil.iter_modules([iter_folder]):
            if not module.ispkg:
                continue

            module_path = os.path.join(module.module_finder.path, module.name)

            import_path = path_to_module(component_root, module_path)

            # Package module shouldn't contain code with side effects.
            try:
                imported_module = importlib.import_module(import_path)

                # Get included modules from the __all__ attribute.
                # Module excluded if it isn't inside the __all__ attribute if the __init__.py has an __all__ attribute.
                if hasattr(imported_module, '__all__'):
                    all_included = getattr(imported_module, '__all__')
                    includes[module_path] = all_included
            # Package cannot be imported.
            except ImportError as err:
                logging.warning(f'Module path {module_path} with import {import_path} throws {err}.\n'
                                'Most likely the __init__.py contains imports or code with side-effects.\n'
                                'You must include the imports in your Python environment to '
                                'respect the __all__ property')

    # Find all modules in found folders and append the full path.
    modules = [root_folder]
    for iter_folder in folders:
        for module in pkgutil.iter_modules([iter_folder]):
            if module.name.startswith('_'):
                continue

            module_path = os.path.join(module.module_finder.path, module.name)

            # Check if module is included.
            include = True
            for key in includes:
                # Module excluded if present in __all__ attribute within __init__.py file.
                if key != module_path and key in module_path and module.name not in includes[key]:
                    include = False
                    break

            if include:
                modules.append(module_path)

    sys.path.remove(component_root)

    return modules


def add_submodule_to_folders(folders):
    """Add the submodules recursively to the folder.

    Args:
        folders ([str]): Folders that get.
    """
    index = 0
    while index < len(folders):
        current_folder = folders[index]

        # Find all folders/directories in the current folder,
        # add full path if folder name doesn't start with '.' or '_'.
        for folder in os.scandir(current_folder):
            if not folder.is_dir() or folder.name.startswith('.') or folder.name.startswith('_'):
                continue

            folder_name = os.path.join(current_folder, folder.name)

            folders.append(folder_name)

        index += 1


def path_to_module(component_root, path):
    """Turns a path into a module using the root as the starting place for module imports.

    Args:
        component_root (str): root to start import from.
        path (str): path to convert to module import.

    Returns:
        str: module import in Python notation.
    """
    # Remove path leading up to component root/path before import statement starts.
    module = path.replace(component_root, '')

    # Remove potential initial slash from path.
    if module.startswith('/') or module.startswith('\\'):
        module = module[1:]

    # Remove potential trailing slash from path.
    if module.endswith('/') or module.endswith('\\'):
        module = module[:-1]

    # Replace all slashes with dots.
    module = module.replace('/', '.').replace('\\', '.')

    # Path is now converted to module import.
    return module


def get_module_import_parts(module_import):
    """Get all module imports from an initial module import, this includes all higher level imports.

    module_import = 'example.module.import.part' generates the following list:
    [
        'example.module.import.part',
        'example.module.import',
        'example.module',
        'example'
    ]

    Args:
        module_import (str): initial module import to derive higher level imports from.

    Returns:
        List[str]: list of module import parts.
    """
    module_imports = [module_import]

    index = len(module_import) - 1
    while index > 0:
        if module_import[index] == '.':
            module_imports.append(module_import[:index])

        index -= 1

    return module_imports


def get_mock_modules(included_paths, included_modules):
    """Get all modules that need to be loaded in the environment when code is run by pdoc.

    Args:
        included_paths ([str]): all paths to Python modules that get documentation generated.
        included_modules ([str]): all package and module level imports.

    Returns:
        set(str): all modules that might need to get mocked if no alternative has been loaded.
    """
    mocks = set()

    # Create mock for all import statements not included in included_modules.
    for included_module in included_paths:
        # Get imports of module from the included module.
        module_imports = get_imports(included_module)

        # Loop over all found imports.
        for module_import in module_imports:
            # Get all possible module parts.
            for module_import_part in get_module_import_parts(module_import):
                # Create mock if module part hasn't been included yet.
                if module_import_part not in included_modules:
                    mocks.add(module_import_part)

    return mocks


def get_mocked(mock_modules):
    """Get all modules that get mocked, because they were not loaded into the environment.

    Args:
        mock_modules (set(str)): modules that need to get mocked if they are not loaded in.

    Returns:
        [str]: modules that are mocked.
    """
    installed_packages = [p.project_name for p in pkg_resources.working_set]
    # pylint: disable=not-an-iterable

    mocked = []

    # Add mock if sys.modules doesn't include an import statement or if the package is already installed.
    for mod_name in mock_modules:
        # Don't mock object if it has already been installed.
        skip = False
        for package in installed_packages:
            if mod_name == package or mod_name.startswith(f'{package}.'):
                skip = True

        if skip:
            continue

        # Add mock object with associated module name if it hasn't been loaded in yet.
        if mod_name not in sys.modules:
            mod_mock = mock.Mock(name=mod_name)
            sys.modules[mod_name] = mod_mock

            # The mocked module.
            mocked.append(mod_name)

    return mocked


def to_tree(modules):
    """Turn a list of modules into a dictionary representing a tree which gets turned into a JSON object by Jinja2.

    The tree dictionary contains a dictionary for each package/module.
    A module has an empty dictionary and packages leading up to
    a module are filled with all contained module dictionaries.

    Args:
        modules (list[str]): list of strings of all module paths (like used in an import statement).

    Returns:
        dict(str, dict): dictionary containing the tree structure as mentioned above.
    """
    tree = dict()

    for module in modules:
        module_path = module.split('.')
        subtree = tree
        for part in module_path:
            if part not in subtree:
                subtree[part] = dict()
            subtree = subtree[part]
    return tree


if __name__ == '__main__':
    # Configure the logger.
    logging.basicConfig(filename='documentation.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # Argument parser for configuration.
    parser = argparse.ArgumentParser(description='Generate documentation.')

    # Create index if flag is given.
    # Generates the index combining all documentation index.html files together in a root html/index.html file.
    parser.add_argument(
        '-ci',
        '--create-index',
        action='store_true',
        help='Create new index if flag is specified.',
        dest='create_index'
    )

    # Set root_folder as required argument to call documentation.py.
    parser.add_argument(
        '-rs',
        '--roots',
        action='extend',
        nargs='*',
        default=[],
        type=str,
        help='Root folders containing all top-level modules. '
             'Includes all modules included via __init__.py, '
             'except for modules not included in __all__ inside __init__.py when provided.',
        metavar='root_folder',
        dest='roots'
    )

    # Parse arguments.
    args = parser.parse_args()

    # Generate documentation for all provided roots.
    for root in args.roots:
        component_path = Path(root)
        logging.info(f'Generating documentation for: {component_path}')
        # Generate documentation for all packages included (via __init__ or if specified __all__ in __init__).
        generate_documentation(component_path)

    # Create index if flag was provided.
    if args.create_index:
        logging.info('Generating index')
        generate_index()
