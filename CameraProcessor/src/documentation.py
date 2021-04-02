import os
from pathlib import Path
import pdoc
import pdoc.web
import pkgutil
from typing import List


def docs():
    """Generates pdoc documentation for all Python modules in CameraProcessor project."""
    # Take file level of current Python modules as root_folder.
    root_folder = os.path.dirname(__file__)

    # Points pdoc to used jinja2 template and sets Google docstrings as the used docstring format.
    pdoc.render.configure(template_directory=Path(os.path.join(root_folder, '../docs/template')), docformat='google')

    # Get all project modules.
    modules = get_modules(root_folder)

    # Generate documentation for all found modules in the /docs.
    pdoc.pdoc(*modules, output_directory=Path(os.path.join(root_folder, '../docs/html')))

    # pdoc.web.DocServer(addr=('localhost', 63500), all_modules=pdoc.web.AllModules())


def get_modules(root_folder: str) -> List[str]:
    """Gets all modules starting from the top folder, excludes Python modules that are deemed as hidden.

    Gets all modules starting from the top folder given as root_folder.
    Starts by searching for all sub folders of the root folder, excluding folders starting with '.' or '_'.
    Looks for modules in all found folders (root_folder + both direct and indirect sub folders).

    Args:
        root_folder: root folder to look through modules at current level and in the sub folders

    Returns:
        List of all Python modules located in root_folder and its sub folders
    """
    # Find all valid sub folders (dir name doesn't start with '.' or '_', starting at the root_folder.
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


if __name__ == '__main__':
    docs()
