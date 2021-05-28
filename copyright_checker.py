from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker


class CopyrightChecker(BaseChecker):
    """ Check the first line for copyright notice"""

    __implements__ = IRawChecker

    name = 'custom_copy'
    msgs = {'W9902': ('Include copyright in file',
                      'file-no-copyright',
                      ('Your file has no copyright')),
            }
    options = ()

    def process_module(self, node):
        """process a module
        the module's content is accessible via node.stream() function
        """
        contains_copyright = False
        copyright_statement = [
            b'This program has been developed by students from the bachelor Computer Science at\r\n',
            b'Utrecht University within the Software Project course.\r\n',
            b'\xc2\xa9 Copyright Utrecht University (Department of Information and Computing Sciences)\r\n'
        ]
        current_copyright_line = 0
        number_quotes = 0

        with node.stream() as stream:
            for (lineno, line) in enumerate(stream):
                # Break when there are two triple quotes passed already
                if str(line).__contains__('"""'):
                    number_quotes += 1
                if number_quotes > 2:
                    break

                # Check consequent lines on copyright string
                if current_copyright_line == 0 and line == copyright_statement[0]:
                    current_copyright_line = 1
                elif current_copyright_line == 1 and line == copyright_statement[1]:
                    current_copyright_line = 2
                elif current_copyright_line == 2 and line == copyright_statement[2]:
                    contains_copyright = True
                    break
                elif current_copyright_line > 0:
                    break

            # File does not contain copyright notice
            if not contains_copyright:
                self.add_message('file-no-copyright',
                                 line=0)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(CopyrightChecker(linter))
