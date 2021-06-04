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
        'C1230': ('Class name is incorrect, expected name: "%s"%s',
                  'incorrect-class-name',
                  'Emitted when a class name doesn\'t correspond to the filename (correctly)'
                  )
    }

    def visit_module(self, node):
        """Called for each module that pylint processes and perform basic checks.

        Args:
            node (astroid.scoped_nodes.Module): Module definition astroid creates.
        """
        self.check_amount_of_classes(node)
        self.check_file_class_names(node)

    def check_amount_of_classes(self, node):
        """Checks that each file has at most one class.

        Args:
            node (astroid.scoped_nodes.Module): Module definition astroid creates.
        """
        class_names = [entity for entity in node.globals if isinstance(node.globals[entity][0], ClassDef)]
        if len(class_names) > 1:
            self.add_message('multiple-class-definitions',
                             node=node)

    def check_file_class_names(self, node):
        class_info = [(entity, node.globals[entity][0].blockstart_tolineno) for entity in node.globals if
                      isinstance(node.globals[entity][0], ClassDef)]
        if not class_info:
            return
        class_name, class_line = class_info[0]
        file_name = node.name.split('.')[-1]

        file_words = file_name.split('_')
        file_words = [file_word.capitalize() for file_word in file_words]
        expected_class_name = "".join(file_words)
        if class_name == expected_class_name:
            return

        expected_interface_name = self.get_expected_interface_name(expected_class_name)
        if file_words[0] == 'Test' and file_words[1][0] == 'I':
            test_class_suffix = "".join(file_words[1:])
            expected_interface_name = "Test" + self.get_expected_interface_name(test_class_suffix)

        if class_name == expected_interface_name:
            return

        if not expected_interface_name:
            self.add_message('incorrect-class-name',
                             node=node,
                             args=(expected_class_name, ""),
                             line=class_line)
        else:
            self.add_message('incorrect-class-name',
                             node=node,
                             args=(expected_class_name, f' or "{expected_interface_name}"'),
                             line=class_line)

    def get_expected_interface_name(self, name):
        if name[0] != 'I':
            return ""
        expected_interface_name = name[0] + name[1].upper() + name[2:]
        return expected_interface_name


def register(linter):
    """Required method to auto register this checker.

    Args:
        linter (pylint.lint.pylinter.PyLinter): Linter to which checks can be added.
    """
    linter.register_checker(ClassesChecker(linter))
