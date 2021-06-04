"""Contains a general classes checker for the pylint that checks the correctness of classes.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from astroid import ClassDef
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class ClassesChecker(BaseChecker):
    """Checks the classes from all modules.

    The following linting errors get caught:
        multiple-class-definitions: Emitted when a file has more than one class.

    Attributes:
        __implements__ (IAstroidChecker): Astroid checker interface.
        name (str): Name of the checker.
        msgs (dict[str, (str, str, str)]): Dictionary with error codes and pylint messages.
    """
    __implements__ = IAstroidChecker

    name = 'incorrect-amount-of-classes'

    msgs = {
        'C1229': ('File contains more than one class',
                  'multiple-class-definitions',
                  'Emitted when a file has more than one class'
                  ),
    }

    def visit_module(self, node):
        """Called for each module that pylint processes and perform basic checks.

        Args:
            node (astroid.scoped_nodes.Module): Module definition astroid creates.
        """
        self.check_amount_of_classes(node)

    def check_amount_of_classes(self, node):
        """Checks that each file has at most one class.

        Args:
            node (astroid.scoped_nodes.Module): Module definition astroid creates.
        """
        class_names = [entity for entity in node.globals if isinstance(node.globals[entity][0], ClassDef)]
        if len(class_names) > 1:
            self.add_message('multiple-class-definitions',
                             node=node)


def register(linter):
    """Required method to auto register this checker.

    Args:
        linter (pylint.lint.pylinter.PyLinter): Linter to which checks can be added.
    """
    linter.register_checker(ClassesChecker(linter))
