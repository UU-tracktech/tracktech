import re

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers import utils


class DocstringChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'incorrect-docstring'

    msgs = {
        'C1120': ("Incorrect function docstring",
                  'incorrect-docstring',
                  'Emitted when a docstring function has the wrong format'
                  ),
        'C1121': ('Section "Args:" is missing from the docstring',
                  'missing-args-in-docstring',
                  'Emitted when a docstring is missing an "Args:" section when it has arguments'
                  ),
        'C1122': ('Argument "%s" missing from the docstring args',
                  'missing-argument-in-docstring',
                  'Emitted when a docstring is missing an argument'
                  ),
        'C1123': ('Argument "%s" not an argument of the method, did you make a typo?',
                  'wrong-argument-in-docstring',
                  'Emitted when a docstring contains an argument'
                  ),
        'C1124': ('Argument "%s" is in the wrong position. Put it in the docstring section at index %s',
                  'argument-wrong-place-in-docstring',
                  'Emitted when a docstring argument is in the wrong position'
                  ),
        }

    @utils.check_messages('incorrect-docstring',
                          'missing-args-in-docstring',
                          'missing-argument-in-docstring',
                          'wrong-argument-in-docstring',
                          'argument-wrong-place-in-docstring')
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

        arg_list = [arg.name for arg in args]
        arg_dict = {arg.name: False for arg in args}

        contains_arg = False
        arg_index = 0

        for doc_line in node.doc.splitlines():
            if not contains_arg:
                args_match = re.match(r'^\s*Args:\s*$', doc_line)
                if args_match is not None:
                    contains_arg = True
            elif arg_index < len(arg_list):
                arg_match = re.match(r'^\s*([a-z_0-9]+)\s\([a-zA-Z0-9_.\[\]{}]+\):\s.*\.\s*$', doc_line)
                if arg_match is None:
                    # Arg is wrong
                    continue

                argument_name = arg_match.group(1)
                if not arg_dict.__contains__(argument_name):
                    self.add_message('wrong-argument-in-docstring',
                                     node=node,
                                     args=argument_name)
                    continue
                elif arg_list[arg_index] != argument_name:
                    self.add_message('argument-wrong-place-in-docstring',
                                     node=node,
                                     args=(argument_name, arg_index))

                arg_dict[argument_name] = True
                arg_index += 1

        if args and not contains_arg:
            self.add_message('missing-args-in-docstring',
                             node=node)
        elif not all(arg_dict.values()):
            for key in arg_dict.keys():
                if not arg_dict[key]:
                    self.add_message('missing-argument-in-docstring',
                                     node=node,
                                     args=key)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(DocstringChecker(linter))
