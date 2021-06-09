"""Contains a general docstring checker for the pylint that checks modules, classes and functions.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import re

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class DocstringChecker(BaseChecker):
    """Checks the docstrings from several layers.

    The following linting errors get caught:
        last-docstring-line-contains-letters: Last line should only contain apostrophes.
        multiple-new-lines-in-docstring: There should never be more than one white line.
        docstring-section-not-separated: A section should be after an empty line.
        first-line-in-docstring-must-end-with-period: First line must end with a period.
        make-docstring-one-line: When docstring is able to be put in one line.
        second-docstring-line-must-be-empty: Second docstring line has to be empty.
        docstring-last-line-empty: There should be no trailing white lines.
        docstring-starts-with-space: Docstrings should start with a character.
        docstring-is-empty: Docstring should not be empty.

    Attributes:
        __implements__ (IAstroidChecker): Astroid checker interface.
        name (str): Name of the checker.
        msgs (dict[str, (str, str, str)]): Dictionary with error codes and pylint messages.
    """
    __implements__ = IAstroidChecker

    name = 'incorrect-docstring'

    msgs = {
        'C1220': ('Last docstring line should only be \"\"\"',
                  'last-docstring-line-contains-letters',
                  'Emitted when a docstring does not end with triple quotes'
                  ),
        'C1221': ('Multiple consequent new lines in docstring',
                  'multiple-new-lines-in-docstring',
                  'Emitted when a docstring function has multiple newlines'
                  ),
        'C1222': ('There should be a newline before section %s',
                  'docstring-section-not-separated',
                  'Emitted when a docstring section is started without a newline'
                  ),
        'C1223': ('First line of docstring should end with a period',
                  'first-line-in-docstring-must-end-with-period',
                  'Emitted when a docstring first line has no period'
                  ),
        'C1224': ('Make docstring single line',
                  'make-docstring-one-line',
                  'Unnecessary multiline docstring'
                  ),
        'C1225': ('Second line of docstring should be empty',
                  'second-docstring-line-must-be-empty',
                  'Second line in docstring'
                  ),
        'C1226': ('Last line of docstring should not be empty',
                  'docstring-last-line-empty',
                  'Last line is empty in docstring'
                  ),
        'C1227': ('Docstring should start with a character',
                  'docstring-starts-with-space',
                  'Emitted when first character is a space'
                  ),
        'C1228': ('Docstring is missing or empty',
                  'docstring-is-missing',
                  'Emitted when first character is a space'
                  ),
        }

    def visit_functiondef(self, node):
        """Called for each function inside a python file that pylint processes.

        Args:
            node (astroid.scoped_nodes.FunctionDef): Function definition containing the .doc property.
        """
        # If the function has empty body then return, missing docstring already gets emitted.
        if not node.doc:
            self.add_message('docstring-is-missing',
                             node=node
                             )
            return

        self.check_docstring(node)

    def visit_classdef(self, node):
        """Called for each class inside the files that pylint processes.

        Args:
            node (astroid.scoped_nodes.ClassDef): Class definition containing the .doc property.
        """
        if not node.doc:
            self.add_message('docstring-is-missing',
                             node=node
                             )
            return

        self.check_docstring(node)

    def visit_module(self, node):
        """Called for each module that pylint processes and perform basic checks.

        Args:
            node (astroid.scoped_nodes.Module): Module definition astroid creates
        """
        if not node.doc:
            self.add_message('docstring-is-missing',
                             node=node
                             )
            return

        self.check_docstring(node)

    def check_docstring(self, node):
        """Retrieves the lines of the documentation and runs several checks on it.

        Args:
            node (Any): Function or class definition containing the docstring.
        """
        # Get documentation.
        doc_lines = self.get_full_docstring(node)

        # Check first and last line.
        self.check_summary(node, doc_lines)
        self.check_last_line(node, doc_lines)

        # See if body is correctly formatted.
        self.check_body(node, doc_lines)

    def get_full_docstring(self, node):
        """Retrieves the lines of the documentation and runs several checks on it.

        Args:
            node (Any): Function or class definition containing the docstring.

        Returns:
            [str]: List of strings which are the split and stripped docstrings.
        """
        # First line should start with character.
        if node.doc[0] == ' ':
            self.add_message('docstring-starts-with-space',
                             node=node)

        # Strip all the lines and put in a list.
        doc_lines = [line.strip() for line in node.doc.split('\n')]

        # Multiline comment should end with an empty line.
        if len(doc_lines) > 1:
            if doc_lines[-1]:
                self.add_message('last-docstring-line-contains-letters',
                                 node=node)
            if len(doc_lines) == 2:
                self.add_message('make-docstring-one-line',
                                 node=node)
            doc_lines = doc_lines[:-1]

        # Return the lines in a list.
        return doc_lines

    def check_summary(self, node, doc_lines):
        """Retrieves the lines of the documentation and runs several checks on it.

        Args:
            node (Any): Function, class or module, definition containing the docstring.
            doc_lines ([str]): List containing all the lines of the documentation.
        """
        # First line should end with a dot.
        first_line_match = re.match(r'^.*\S\.($|\"\"\"$)', doc_lines[0])
        if not first_line_match:
            self.add_message('first-line-in-docstring-must-end-with-period',
                             node=node)

        # Return if single line.
        if len(doc_lines) == 1:
            return
        # Second line contains commenting.
        elif doc_lines[1]:
            self.add_message('second-docstring-line-must-be-empty',
                             node=node)

    def check_last_line(self, node, doc_lines):
        """Checks whether the last line is not empty.

        Args:
            node (Any): Function, class or module, definition containing the docstring.
            doc_lines ([str]): List containing all the lines of the documentation.
        """
        # Small docstring has other messages.
        if len(doc_lines) < 3:
            return

        # Last line is empty but should not.
        if not doc_lines[-1]:
            self.add_message('docstring-last-line-empty',
                             node=node)

    def check_body(self, node, doc_lines):
        """Checks whether body has its sections correctly spaced and does not contain several white lines.

        Args:
            node (Any): Function, class or module, definition containing the docstring.
            doc_lines ([str]): List containing all the lines of the documentation.
        """
        # Variables to keep track of the current state.
        contains_double_white_line = False
        number_white_lines = 0
        line_index = 0

        # For each line in the docstring.
        for doc_line in doc_lines:
            # Detect double white lines in comments.
            if not doc_line:
                number_white_lines += 1
                if number_white_lines > 1:
                    contains_double_white_line = True
            else:
                number_white_lines = 0

            # Section has to be after a newline.
            section_match = re.match(r'^\s*(\w+):\s*$', doc_line)
            if section_match is not None and line_index > 0:
                # If last line was not empty.
                if doc_lines[line_index - 1]:
                    section_name = section_match.group(1)
                    self.add_message('docstring-section-not-separated',
                                     node=node,
                                     args=section_name)

            line_index += 1

        # Create pylint error when docstring contains two white lines.
        if contains_double_white_line:
            self.add_message('multiple-new-lines-in-docstring',
                             node=node)


def register(linter):
    """Required method to auto register this checker.

    Args:
        linter (pylint.lint.pylinter.PyLinter): Linter to which checks can be added.
    """
    linter.register_checker(DocstringChecker(linter))
