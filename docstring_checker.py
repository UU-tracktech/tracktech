import re

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers import utils


class DocstringChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'incorrect-docstring'

    msgs = {
        'C1220': ('Last line should be \"\"\"',
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
        'C1223': ('First line of docstring should end with a dot',
                  'first-line-in-docstring-must-end-with-dot',
                  'Emitted when a docstring first line has no dot'
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
        }

    @utils.check_messages('last-docstring-line-contains-letters',
                          'multiple-new-lines-in-docstring',
                          'docstring-section-not-separated',
                          'first-line-in-docstring-must-end-with-dot',
                          'make-docstring-one-line',
                          'second-docstring-line-must-be-empty',
                          'docstring-last-line-empty')
    def visit_functiondef(self, node):
        """
            Checks for presence of return statement at the end of a function
            "return" or "return None" are useless because None is the default
            return type if they are missing
        """
        # if the function has empty body then return, missing docstring already gets emitted
        if not node.doc:
            return

        doc_lines = [line.strip() for line in node.doc.splitlines()]

        if len(doc_lines) > 1:
            if doc_lines[-1]:
                self.add_message('last-docstring-line-contains-letters',
                                 node=node)
            doc_lines = doc_lines[:-1]

        contains_double_white_line = False
        number_white_lines = 0

        self.check_summary(node, doc_lines)
        self.check_last_line(node, doc_lines)

        line_index = 0

        for doc_line in doc_lines:
            # Prevent double lines in comments
            if not doc_line:
                number_white_lines += 1
                if number_white_lines > 1:
                    contains_double_white_line = True
            else:
                number_white_lines = 0

            # Section has to be after a newline
            section_match = re.match(r'^\s*(\w+):\s*$', doc_line)
            if section_match is not None and line_index > 0:
                if doc_lines[line_index - 1]:
                    section_name = section_match.group(1)
                    self.add_message('docstring-section-not-separated',
                                     node=node,
                                     args=section_name)

            line_index += 1

        # There should never be two white lines
        if contains_double_white_line:
            self.add_message('multiple-new-lines-in-docstring',
                             node=node)

    def check_summary(self, node, docstring_lines):
        first_line_match = re.match(r'^.*\.\s*$', docstring_lines[0])
        if not first_line_match:
            self.add_message('first-line-in-docstring-must-end-with-dot',
                             node=node)

        if len(docstring_lines) == 1:
            return
        elif len(docstring_lines) == 2 and not docstring_lines[1]:
            self.add_message('make-docstring-one-line',
                             node=node)
        elif docstring_lines[1]:
            self.add_message('second-docstring-line-must-be-empty',
                             node=node)

    def check_last_line(self, node, docstring_lines):
        # Small docstring has other messages
        if len(docstring_lines) < 3:
            return

        # Last line is empty but should not
        if not docstring_lines[-1]:
            self.add_message('docstring-last-line-empty',
                             node=node)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(DocstringChecker(linter))
