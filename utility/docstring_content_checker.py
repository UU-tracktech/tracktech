"""Contains a docstring content checker for the pylint that checks modules, classes and functions docstrings.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import re

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class DocstringContentChecker(BaseChecker):
    """Checks the docstrings from several layers.

    The following linting errors get caught:
        unnecessary-args-section: An args section is inside the docstring without parameters.
        missing-args-in-docstring: "Args:" section is missing inside the docstring specification.
        missing-argument-in-docstring: Missing argument in the docstring.
        unknown-argument-in-docstring: An unknown argument was found inside the docstring.
        argument-wrong-place-in-docstring: Argument is at a wrong location inside the docstring.
        wrong-argument-specification-syntax: Argument specification is wrong format.
        sections-in-wrong-order: Sections are not in the correct order.
        unknown-section: Section name was unknown.
        missing-return-type: "Returns:" section has no type specified.
        use-dict-keyword: When there are curly braces used to define a dictionary.
        returns-section-has-multiple-type-definitions: There should only be one type definition inside the returns.

    Attributes:
        __implements__ (IAstroidChecker): Astroid checker interface.
        name (str): Name of the checker.
        ordered_sections ([str]): The order in which sections should be inside the docstring.
        msgs (dict[str, (str, str, str)]): Dictionary with error codes and pylint messages.
    """
    __implements__ = IAstroidChecker

    name = 'incorrect-docstring-content'
    ordered_sections = ['Note', 'Args', 'Attributes', 'Yields', 'Returns', 'Examples', 'Raises']

    msgs = {
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
                  'unknown-argument-in-docstring',
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
        'C1127': (f'Sections in wrong order, must be like {ordered_sections}',
                  'sections-in-wrong-order',
                  'Emitted when docstring sections are in the wrong order'
                  ),
        'C1128': (f'Section: "%s" is unknown, only known sections are: {ordered_sections}',
                  'unknown-section',
                  'Emitted when docstring section is of the wrong type'
                  ),
        'C1129': ('Return type definition is missing',
                  'missing-return-type',
                  'Emitted when docstring Returns section misses a type definition'
                  ),
        'C1130': ('Dictionary types have to be of form dict[keytype, valuetype]',
                  'use-dict-keyword',
                  'Emitted when docstring contains literal dict type'
                  ),
        'C1131': ('Returns section contains type definitions on multiple lines',
                  'returns-section-has-multiple-type-definitions',
                  'Emitted when returns section has multiple type definitions'
                  ),
        }

    def visit_functiondef(self, node):
        """Called for each function inside a python file that pylint processes.

        Args:
            node (astroid.scoped_nodes.FunctionDef): Function definition containing the .doc property.
        """
        # If the function has empty body then return, missing docstring already gets emitted.
        if not node.doc:
            return

        # Discard the 'self' argument.
        args = node.args.args
        if args:
            if args[0].name == 'self':
                args = args[1:]

        # Lint the documentation inside the node.
        self.lint_docstring(node, True, args)

    def visit_classdef(self, node):
        """Called for each class inside the files that pylint processes.

        Args:
            node (astroid.scoped_nodes.ClassDef): Class definition containing the .doc property.
        """
        # If the function has empty body then return, missing docstring already gets emitted.
        if not node.doc:
            return

        self.lint_docstring(node, False, [])

    def lint_docstring(self, node, is_function, args):
        """Lints the docstring for a Class or method, only checking the content.

        Args:
            node (Any): Class or method definition containing the .doc property.
            is_function (bool): Whether it is called for a function.
            args ([astroid.node_classes.AssignName]): List of arguments given to the function
        """
        # Get the lines of the documentation.
        doc_lines = [line.strip() for line in node.doc.split('\n') if len(line.strip()) > 0]
        sections_list = []

        # Index of the current line that is getting linted.
        line_index = 0
        while line_index < len(doc_lines):
            # Match the line for a section.
            doc_line = doc_lines[line_index]
            section_match = re.match(r'^\s*(\w+):\s*$', doc_line)

            # If it is not the start of a section then the line is not linted.
            if section_match is None:
                line_index += 1
                continue

            # Name of the section.
            section_name = section_match.group(1)

            # Check if the section is known.
            if self.ordered_sections.__contains__(section_name):
                sections_list.append(section_name)
            # Create pylint message otherwise.
            else:
                self.add_message('unknown-section',
                                 node=node,
                                 args=section_name)
                line_index += 1
                continue

            # Switch statement for linting of sections.
            if section_name == 'Args':
                # When there is an Args section without there being arguments.
                if not args:
                    self.add_message('unnecessary-args-section',
                                     node=node)
                    line_index += 1
                # Only lint args section if it is a function.
                elif is_function:
                    line_index = self.doc_lint_args_section(node, doc_lines, line_index, args)
            elif section_name == 'Returns' and is_function:
                line_index = self.doc_lint_returns_section(node, doc_lines, line_index)
            else:
                line_index += 1

        # Argument section needs to exist but is missing.
        if args and not sections_list.__contains__('Args'):
            self.add_message('missing-args-in-docstring',
                             node=node)

        # Sections are not the in the correct order.
        ordered_sections_list = sorted(sections_list, key=self.ordered_sections.index)
        if ordered_sections_list != sections_list:
            self.add_message('sections-in-wrong-order',
                             node=node)

    def doc_lint_args_section(self, node, doc_lines, args_section_line_index, args):
        """Lint the "Args:" section of the docstring and enforce types are included.

        Args:
            node (Any): Only function should contain an argument section.
            doc_lines ([str]): Split lines of the documentation.
            args_section_line_index (int): Index where the args section starts.
            args ([astroid.node_classes.AssignName]): Arguments of the function.

        Returns:
            int: Line number of the last line in the Args section.
        """
        # Puts the argument names in both a list and dictionary to enable order and fast lookup.
        arg_list = [arg.name for arg in args]
        arg_dict = {arg.name: False for arg in args}

        # Index of the argument that is being linted and the current line.
        arg_index = 0
        line_index = args_section_line_index + 1

        # The strict an non strict version of an argument with type.
        arg_with_type_regex = r'^\s*([a-z_0-9]+)\s\([\w\d_.\[\]{}]+\):\s.*$'
        loose_arg_with_type_regex = r'^\s*([a-z_0-9]+)\s*\([\w\d_.\[\]{}]+\):.*$'

        # Loop through the argument section until another section is found or the end is reached.
        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            # Stop if next section is found.
            section, _ = self.get_section_match(doc_line)
            if section:
                break

            # Strict argument match.
            arg_match = re.match(arg_with_type_regex, doc_line)

            # See if a less strict match does detect the line.
            if arg_match is None:
                arg_loose_match = re.match(loose_arg_with_type_regex, doc_line)
                # Wrong format of the argument.
                if arg_loose_match is not None:
                    self.add_message('wrong-argument-specification-syntax',
                                     node=node,
                                     args=arg_loose_match.group(1))
                line_index += 1
                continue

            argument_name = arg_match.group(1)
            # Argument does not exist as parameter.
            if not arg_dict.__contains__(argument_name):
                self.add_message('unknown-argument-in-docstring',
                                 node=node,
                                 args=argument_name)
                line_index += 1
                continue
            # Argument is in the wrong position inside the docstring.
            if arg_list[arg_index] != argument_name:
                self.add_message('argument-wrong-place-in-docstring',
                                 node=node,
                                 args=(argument_name, arg_index))

            # Add to dictionary and go to the next line.
            arg_dict[argument_name] = True
            arg_index += 1
            line_index += 1

        # When the "Args:" section is done check whether all keys are specified in the docstring.
        for key in arg_dict.keys():
            if not arg_dict[key]:
                self.add_message('missing-argument-in-docstring',
                                 node=node,
                                 args=key)

        # Return where the section stops.
        return line_index

    def doc_lint_returns_section(self, node, doc_lines, returns_section_line_index):
        """Lint the "Returns:" section inside the docstring and enforces only the first line can contain a type.

        Args:
            node (Any): Function definition that contains the returns section.
            doc_lines ([List]): List of docstring lines.
            returns_section_line_index (int): Line where the returns section starts.

        Returns:
            int: The line index where the returns section stops.
        """
        # Lines and index.
        line_index = returns_section_line_index + 1
        doc_line = doc_lines[line_index]

        # If the first line contains no type.
        if not doc_line.__contains__(':'):
            self.add_message('missing-return-type',
                             node=node)
            return line_index

        # Get the return type.
        return_type = doc_line.split(':')[0]

        # Prevent the use of curly braces.
        if return_type.__contains__('{') or return_type.__contains__('}'):
            self.add_message('use-dict-keyword',
                             node=node)
            return line_index

        line_index += 1
        # Make sure there are no other type definitions inside the section.
        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            # Break when another section is reached.
            section, _ = self.get_section_match(doc_line)
            if section:
                break

            # A double dot indicates another type definition is made.
            if doc_line.__contains__(':'):
                self.add_message('returns-section-has-multiple-type-definitions',
                                 node=node)
                break

            line_index += 1

        # Return the index of the line where the returns section stops.
        return line_index

    @staticmethod
    def get_section_match(line):
        """Checks whether the current line matches a section.

        Args:
            line (str): Line of which to check of whether it starts a section.

        Returns:
            bool, str: Whether a section was found and what the name is of that section.
        """
        section_match = re.match(r'^\s*(\w+):\s*$', line)
        # No section was found.
        if section_match is None:
            return False, ""

        # Section spotted.
        return True, section_match.group(1)


def register(linter):
    """Required method to auto register this checker.

    Args:
        linter (pylint.lint.pylinter.PyLinter): Linter to which checks can be added.
    """
    linter.register_checker(DocstringContentChecker(linter))
