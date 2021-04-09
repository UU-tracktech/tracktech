import os
from pathlib import Path
import pkgutil
import pdoc


def generate_documentation(root_folder):
    """Generates pdoc documentation for all Python modules in CameraProcessor project.

    Args:
        root_folder (Path): path to root folder of Python code.
    """
    doc_folder = os.path.dirname(__file__)

    # Points pdoc to used jinja2 template and sets Google docstrings as the used docstring format.
    pdoc.render.configure(template_directory=Path(os.path.join(doc_folder, 'template')),
                          docformat='google')

    # Add to_tree to Jinja2 environment filters to generate tree from modules list.
    pdoc.render.env.filters['to_tree'] = to_tree

    # Output directory
    output_dir = Path(os.path.join(doc_folder, 'html', root_folder))

    # Create docs html dir if it doesn't exist.
    output_dir.mkdir(parents=True, exist_ok=True)

    real_root = os.path.join(doc_folder, '..', root_folder)

    # Generate documentation for all found modules in the /docs.
    pdoc.pdoc(real_root, output_directory=output_dir)


def get_modules(root_folder):
    """Gets all modules starting from the top folder,
    excludes Python modules that are deemed as hidden.

    Gets all modules starting from the top folder given as root_folder.
    Starts by searching for all sub folders of the root folder,
    excluding folders starting with '.' or '_'.
    Looks for modules in all found folders (root_folder + both direct and indirect sub folders).

    Args:
        root_folder (str): root folder to look through modules at current level and in the sub folders

    Returns:
        list[str]: list of all Python modules located in root_folder and its sub folders
    """
    # Find all valid sub folders (dir name doesn't start with
    # '.' or '_', starting at the root_folder.
    folders = [root_folder]
    index = 0
    while index < len(folders):
        current_folder = folders[index]

        for folder in os.scandir(current_folder):
            if not folder.is_dir() or folder.name.startswith('.') or folder.name.startswith('_'):
                continue

            folder_name = os.path.join(current_folder, folder.name)

            folders.append(folder_name)

        index += 1

    # Find all modules in found folders and append the full path.
    modules = []
    for module in pkgutil.iter_modules(folders):
        if module.name.startswith('_'):
            continue

        module_name = os.path.join(module.module_finder.path, module.name)

        modules.append(module_name)

    return modules


def to_tree(modules):
    """Turn a list of modules into a dictionary representing a tree
    which gets turned into a JSON object by Jinja2.

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
    import argparse

    # Set root_folder as required argument to call documentation.py.
    parser = argparse.ArgumentParser(description='Generate documentation for provided root folder')
    parser.add_argument('root_folder',
                        type=str,
                        help='Root folder containing all top-level modules. '
                             'Includes all modules included via __init__.py, '
                             'except for modules not included in __all__ inside __init__.py when provided.'
                        )

    # Parse arguments.
    args = parser.parse_args()

    # Prepend .. to args root_folder to start one level higher (starting at root of project).
    root = Path(args.root_folder)

    # Generate documentation for all packages included (via __init__ or if specified __all__ in __init__).
    generate_documentation(root)
