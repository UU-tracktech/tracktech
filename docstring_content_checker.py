import re

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers import utils


class DocstringContentChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'incorrect-docstring-content'

    msgs = {
        'C1120': ("Incorrect function docstring",
                  'incorrect-docstring',
                  'Emitted when a docstring function has the wrong format'
                  ),
        'C1121': ("Args section should not be there",
                  'unnecessary-args-section',
                  'Emitted when a docstring has "Args:" section without arguments'
                  ),
        'C1122': ('Section "Args:" is missing from the docstring',
                  'missing-args-in-docstring',
                  'Emitted when a docstring is missing an "Args:" section when it has arguments'
                  ),
        'C1123': ('Argument "%s" missing from the docstring args',
                  'missing-argument-in-docstring',
                  'Emitted when a docstring is missing an argument'
                  ),
        'C1124': ('Argument "%s" not an argument of the method, did you make a typo?',
                  'wrong-argument-in-docstring',
                  'Emitted when a docstring contains an argument'
                  ),
        'C1125': ('Argument "%s" is in the wrong position. Put it in the docstring section at index %s',
                  'argument-wrong-place-in-docstring',
                  'Emitted when a docstring argument is in the wrong position'
                  ),
        'C1126': ('Argument "%s" has wrong specification, must be in form "<argument-name> (<argument-type>): "',
                  'wrong-argument-specification-syntax',
                  'Emitted when a docstring argument is in the wrong position'
                  ),
        }

    @utils.check_messages('incorrect-docstring',
                          'unnecessary-args-section',
                          'missing-args-in-docstring',
                          'missing-argument-in-docstring',
                          'wrong-argument-in-docstring',
                          'argument-wrong-place-in-docstring',
                          'wrong-argument-specification-syntax')
    def visit_functiondef(self, node):
        """
            Checks for presence of return statement at the end of a function
            "return" or "return None" are useless because None is the default
            return type if they are missing
        """
        # if the function has empty body then return, missing docstring already gets emitted
        if not node.doc:
            return

        args = node.args.args
        if args:
            if args[0].name == 'self':
                args = args[1:]

        doc_lines = [line.strip() for line in node.doc.splitlines() if len(line.strip()) > 0]
        sections_list = []

        line_index = 0
        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            section_match = re.match(r'^\s*(\w+):\s*$', doc_line)

            if section_match is None:
                line_index += 1
                continue

            section_name = section_match.group(1)
            sections_list.append(section_name)

            if section_name == 'Args':
                if not args:
                    self.add_message('unnecessary-args-section',
                                     node=node)
                else:
                    line_index = self.doc_lint_args_section(doc_lines, line_index, node, args)
            # elif section_name == 'Raises':
            #     line_index = self.doc_lint_raises_section(doc_lines, line_index, node)
            # elif section_name == 'Returns':
            #     line_index = self.doc_lint_returns_section(doc_lines, line_index, node)

            line_index += 1

        # Argument section needs to exist
        if args and not sections_list.__contains__('Args'):
            self.add_message('missing-args-in-docstring',
                             node=node)

    def doc_lint_args_section(self, doc_lines, args_section_line_index, node, args):
        arg_list = [arg.name for arg in args]
        arg_dict = {arg.name: False for arg in args}

        arg_index = 0
        line_index = args_section_line_index + 1

        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            section, _ = self.get_section_match(doc_line)
            if section:
                break

            arg_match = re.match(r'^\s*([a-z_0-9]+)\s\([\w\d_.\[\]{}]+\):\s.*$', doc_line)

            # See if a less strict match does detect the line
            if arg_match is None:
                arg_loose_match = re.match(r'^\s*([a-z_0-9]+)\s*\([\w\d_.\[\]{}]+\):.*$', doc_line)
                if arg_loose_match is not None:
                    self.add_message('wrong-argument-specification-syntax',
                                     node=node,
                                     args=arg_loose_match.group(1))
                line_index += 1
                continue

            argument_name = arg_match.group(1)
            if not arg_dict.__contains__(argument_name):
                self.add_message('wrong-argument-in-docstring',
                                 node=node,
                                 args=argument_name)
                line_index += 1
                continue
            elif arg_list[arg_index] != argument_name:
                self.add_message('argument-wrong-place-in-docstring',
                                 node=node,
                                 args=(argument_name, arg_index))

            arg_dict[argument_name] = True
            arg_index += 1
            line_index += 1

        if not all(arg_dict.values()):
            for key in arg_dict.keys():
                if not arg_dict[key]:
                    self.add_message('missing-argument-in-docstring',
                                     node=node,
                                     args=key)

        return line_index

    def doc_lint_returns_section(self, doc_lines, returns_section_line_index, node):
        line_index = returns_section_line_index + 1

        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            section, _ = self.get_section_match(doc_line)
            if section:
                break

            arg_match = re.match(r'^\s*([a-z_0-9]+)\s\([\w\d_.\[\]{}]+\):\s.*$', doc_line)

        return line_index

    @staticmethod
    def get_section_match(line):
        section_match = re.match(r'^\s*(\w+):\s*$', line)
        if section_match is None:
            return False, None
        return True, section_match.group(1)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(DocstringContentChecker(linter))
