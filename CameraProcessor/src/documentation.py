import os
from pathlib import Path
import pkgutil
from typing import List
import pdoc
import pdoc.web


def main():
    """Generates pdoc documentation for all Python modules in CameraProcessor project."""
    # Take file level of current Python modules as root_folder.
    root_folder = os.path.dirname(__file__)

    # Points pdoc to used jinja2 template and sets Google docstrings as the used docstring format.
    pdoc.render.configure(template_directory=Path(os.path.join(root_folder, '../docs/template')),
                          docformat='google')

    pdoc.render.env.filters['to_tree'] = to_tree

    # Get all project modules.
    modules = get_modules(root_folder)

    # Create docs html dir if it doesn't exist.
    Path("../docs/html").mkdir(parents=True, exist_ok=True)

    # Generate documentation for all found modules in the /docs.
    pdoc.pdoc(*modules, output_directory=Path(os.path.join(root_folder, '../docs/html')))

    # pdoc.web.DocServer(addr=('localhost', 63500), all_modules=pdoc.web.AllModules())


def get_modules(root_folder: str) -> List[str]:
    """Gets all modules starting from the top folder,
    excludes Python modules that are deemed as hidden.

    Gets all modules starting from the top folder given as root_folder.
    Starts by searching for all sub folders of the root folder,
    excluding folders starting with '.' or '_'.
    Looks for modules in all found folders (root_folder + both direct and indirect sub folders).

    Args:
        root_folder: root folder to look through modules at current level and in the sub folders

    Returns:
        List of all Python modules located in root_folder and its sub folders
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
        modules: list of strings of all module paths (like used in an import statement).

    Returns: dictionary containing the tree structure as mentioned above.
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
    main()
