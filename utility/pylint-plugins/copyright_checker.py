"""Contains a checker which verifies the file contains the copyright notice.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker


class CopyrightChecker(BaseChecker):
    """Checks the module for our own license.

    The following linting errors get caught:
        file-no-copyright: File contains no copyright message.

    Attributes:
        __implements__ (IRawChecker): Raw checker in order to enumerate the lines.
        name (str): Name of the checker.
        msgs (dict[str, (str, str, str)]): Dictionary with error codes and pylint messages.
    """

    __implements__ = IRawChecker

    name = 'custom_copy'
    msgs = {'W9902': ('Include copyright in file',
                      'file-no-copyright',
                      'Your file has no copyright'),
            }

    def process_module(self, node):
        """Process a module and checks whether the docstring contains the correct copyright notice.

        Args:
            node (astroid.scoped_nodes.Module): Module definition containing the raw content of the file.
        """
        # A limitation of Pylint is that it adds the root __init__.py regardless of whether it is ignored.
        if node.path[0].endswith('__init__.py'):
            return

        # What the copyright statement should be.
        copyright_statement = [
            'This program has been developed by students from the bachelor Computer Science at',
            'Utrecht University within the Software Project course.',
            '© Copyright Utrecht University (Department of Information and Computing Sciences)'
        ]

        # Create a small state.
        contains_copyright = False
        current_copyright_line = 0
        number_quotes = 0

        # Go through the file.
        with node.stream() as stream:
            for (_, line) in enumerate(stream):
                line = line.decode('utf-8')

                # Break when there are two triple quotes passed already.
                if line.__contains__('"""'):
                    number_quotes += 1
                if number_quotes > 2:
                    break

                # Check consequent lines on copyright string.
                # Uses startswith to ignore line endings of the os.
                if current_copyright_line == 0 and line.startswith(copyright_statement[0]):
                    current_copyright_line = 1
                elif current_copyright_line == 1 and line.startswith(copyright_statement[1]):
                    current_copyright_line = 2
                elif current_copyright_line == 2 and line.startswith(copyright_statement[2]):
                    contains_copyright = True
                    break
                # Line was not the following line.
                elif current_copyright_line > 0:
                    break

            # File does not contain copyright notice.
            if not contains_copyright:
                self.add_message('file-no-copyright',
                                 line=0)


def register(linter):
    """Required method to auto register this checker.

    Args:
        linter (pylint.lint.pylinter.PyLinter): Linter to which checks can be added.
    """
    linter.register_checker(CopyrightChecker(linter))
