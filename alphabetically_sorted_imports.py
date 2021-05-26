import astroid

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker


class AlphabeticallySortedImports(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'alphabetically-sorted-imports-checker'

    UNSORTED_IMPORT_FROM = 'unsorted-import-from'

    DIR_HIGHER = 'higher'
    DIR_LOWER = 'lower'
    # here we define our messages
    msgs = {
        'C5001': ('"%s" in "%s" is in the wrong position. Move it %s.',
                  UNSORTED_IMPORT_FROM,
                  'Refer to project rules on wiki'),
    }
    options = ()

    priority = -1

    def visit_importfrom(self, node):
        # node is an astroid.node_classes.ImportFrom instance
        # it has names property with 2-element tuples that contain
        # object name and it's alias (or None, if not aliased)
        names = [name for name, _alias in node.names]
        # print(names)
        # we sort all names to get desired structure
        sorted_names = sorted(names)
        for actual_index, name in enumerate(names):
            correct_index = sorted_names.index(name)
            # if our object is not placed in the same order as in
            # sorted_names, then we report this fact as a violation
            if correct_index != actual_index:
                direction = self.DIR_LOWER if correct_index > actual_index else self.DIR_HIGHER
                args = name, node.as_string(), direction
                # this function causes pylint to emit warning
                self.add_message(
                    self.UNSORTED_IMPORT_FROM, node=node, args=args
                )


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(AlphabeticallySortedImports(linter))
