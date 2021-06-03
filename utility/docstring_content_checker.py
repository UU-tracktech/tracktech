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
        section-wrong-format: Section should follow by spaces
        missing-return-type: "Returns:" section has no type specified.
        use-dict-keyword: When there are curly braces used to define a dictionary.
        returns-section-has-multiple-type-definitions: There should only be one type definition inside the returns.
        enclose-type-in-parenthesis: The type should be enclosed with parenthesis.
        type-not-defined: Type of argument or attribute is missing.

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
        'C1126': ('Argument "%s" has wrong specification, "<argument-name> (<argument-type>): " must be the form',
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
        'C1129': ('Section: "%s" is not formatted correctly, should be "<section-name>:\\n"',
                  'section-wrong-format',
                  'Emitted when docstring section has the wrong format'
                  ),
        'C1130': ('Return type definition is missing',
                  'missing-return-type',
                  'Emitted when docstring Returns section misses a type definition'
                  ),
        'C1131': ('Dictionary types have to be of form dict[keytype, valuetype], not "%s"',
                  'use-dict-keyword',
                  'Emitted when docstring contains literal dict type'
                  ),
        'C1132': ('Returns section contains type definitions on multiple lines',
                  'returns-section-has-multiple-type-definitions',
                  'Emitted when returns section has multiple type definitions'
                  ),
        'C1133': ('Enclose type "%s" in parenthesis',
                  'enclose-type-in-parenthesis',
                  'Emitted when type is not enclosed in parenthesis'
                  ),
        'C1134': ('Type of "%s" is not defined inside section "%s"',
                  'type-not-defined',
                  'Emitted when type is not defined'
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

        # Discard the 'self' and '_' argument.
        args = [arg.name for arg in node.args.args if arg.name != 'self' and arg.name != '_']

        if node.args.kwarg is not None:
            args.append("**" + node.args.kwarg)

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
            args ([str]): List of argument names given to the function
        """
        # Get the lines of the documentation.
        doc_lines = [line.strip() for line in node.doc.split('\n') if len(line.strip()) > 0]
        sections_list = []

        # Index of the current line that is getting linted.
        line_index = 0
        while line_index < len(doc_lines):
            # Match the line for a section.
            doc_line = doc_lines[line_index]

            section, section_name = self.match_section(node, doc_line)
            if not section:
                line_index += 1
                continue

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

            # Lint function section.
            if is_function:
                line_index = self.lint_function_section(node, doc_lines, section_name, line_index, args)
            # Lint class section.
            else:
                line_index = self.lint_class_section(node, doc_lines, section_name, line_index)

        # Argument section needs to exist but is missing.
        if any(args) and not sections_list.__contains__('Args'):
            self.add_message('missing-args-in-docstring',
                             node=node)

        # Sections are not the in the correct order.
        ordered_sections_list = sorted(sections_list, key=self.ordered_sections.index)
        if ordered_sections_list != sections_list:
            self.add_message('sections-in-wrong-order',
                             node=node)

    def lint_function_section(self, node, doc_lines, section_name, line_index, args):
        """Lint any section of the function docstring.

        Args:
            node (Any): Function definition inside a astriod node.
            doc_lines ([str]): Split lines of the documentation.
            section_name (str): Name of the section to be checked.
            line_index (int): Index where the section starts.
            args ([str]): Argument names of the function.

        Returns:
            int: Line number of the last line in the section.
        """
        # Switch statement for linting of sections.
        if section_name == 'Args' and not args:
            # When there is an Args section without there being arguments.
            self.add_message('unnecessary-args-section',
                             node=node)
            line_index += 1
        elif section_name == 'Args' and args:
            line_index = self.doc_lint_args_section(node, doc_lines, line_index, args)
        elif section_name == 'Returns':
            line_index = self.doc_lint_returns_section(node, doc_lines, line_index)
        elif section_name == 'Raises':
            line_index = self.doc_lint_raises_section(doc_lines, line_index)
        else:
            line_index += 1

        return line_index

    def lint_class_section(self, node, doc_lines, section_name, line_index):
        """Lint any section of the class docstring.

        Args:
            node (Any): Class definition inside a astriod node.
            doc_lines ([str]): Split lines of the documentation.
            section_name (str): Name of the section to be checked.
            line_index (int): Index where the args section starts.

        Returns:
            int: Line number of the last line in the section.
        """
        # Switch statement for linting of sections.
        if section_name == 'Attributes':
            # When there is an Attributes section.
            line_index = self.doc_lint_attribute_section(node, doc_lines, line_index)
        else:
            line_index += 1

        return line_index

    def doc_lint_args_section(self, node, doc_lines, args_section_line_index, args):
        """Lint the "Args:" section of the docstring and enforce types are included.

        Args:
            node (Any): Only function should contain an argument section.
            doc_lines ([str]): Split lines of the documentation.
            args_section_line_index (int): Index where the args section starts.
            args ([str]): Arguments of the function.

        Returns:
            int: Line number of the last line in the Args section.
        """
        # Puts the argument names in a dictionary to enable order and fast lookup.
        arg_dict = {arg: False for arg in args}

        # Index of the argument that is being linted and the current line.
        arg_index = 0
        line_index = args_section_line_index + 1

        # Loop through the argument section until another section is found or the end is reached.
        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            # Stop if next section is found.
            section, _ = self.match_section(node, doc_line)
            if section:
                break

            arg, arg_name, _ = self.match_type_definition(node, doc_line, "Args")

            if not arg:
                line_index += 1
                continue

            # Argument does not exist as parameter.
            if not arg_dict.__contains__(arg_name):
                self.add_message('unknown-argument-in-docstring',
                                 node=node,
                                 args=arg_name)
                line_index += 1
                continue
            # Argument is in the wrong position inside the docstring.
            if args[arg_index] != arg_name:
                self.add_message('argument-wrong-place-in-docstring',
                                 node=node,
                                 args=(arg_name, arg_index))

            # Add to dictionary and go to the next line.
            arg_dict[arg_name] = True
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

    def doc_lint_attribute_section(self, node, doc_lines, attribute_section_line_index):
        """Lint the "Args:" section of the docstring and enforce types are included.

        Args:
            node (Any): Only function should contain an argument section.
            doc_lines ([str]): Split lines of the documentation.
            attribute_section_line_index (int): Index where the section starts.

        Returns:
            int: Line number of the last line in the Attributes section.
        """
        # Content starts one line after section start.
        line_index = attribute_section_line_index + 1

        # Loop through the argument section until another section is found or the end is reached.
        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            # Stop if next section is found.
            section, _ = self.match_section(node, doc_line)
            if section:
                break

            # Ensure each attribute has a type defined.
            self.match_type_definition(node, doc_line, "Attributes")
            line_index += 1

        return line_index

    def doc_lint_returns_section(self, node, doc_lines, returns_section_line_index):
        """Lint the "Returns:" section inside the docstring and enforces only the first line can contain a type.

        Args:
            node (Any): Function definition that contains the returns section.
            doc_lines ([str]): List of docstring lines.
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

        # Get the return type and check for curly braces.
        return_type = doc_line.split(':')[0]
        self.check_type_definition(node, return_type, False)

        line_index += 1
        # Make sure there are no other type definitions inside the section.
        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            # Break when another section is reached.
            section, _ = self.match_section(node, doc_line)
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

    def doc_lint_raises_section(self, doc_lines, raises_section_line_index):
        """Lint the raises section inside a function.

        Args:
            doc_lines ([str]): List of docstring lines.
            raises_section_line_index (int): Line where the Raises section starts.

        Returns:
            int: The line index where the Raises section stops.
        """
        # Lines and index.
        line_index = raises_section_line_index + 1

        # Parse the raises lines.
        while line_index < len(doc_lines):
            doc_line = doc_lines[line_index]

            # Break when another section is reached in the exact format.
            section, _ = self.match_strict_section(doc_line)
            if section:
                break

            line_index += 1

        # Return the index of the line where the returns section stops.
        return line_index

    def match_type_definition(self, node, line, section_name):
        """Checks whether the current line matches a section.

        Args:
            node (Any): Node the pylint message is connected to when linting error is found.
            line (str): Line of which to check of whether it contains a type definition.
            section_name (str): Name of the section.

        Returns:
            bool, str, str: Whether a section was found and what the name and type of the argument is.
        """
        # No type definition inside this line.
        if not line.__contains__(':'):
            return False, "", ""

        # Strict argument match.
        arg_match = re.match(r'^\s*([*a-z_0-9]+)\s\(([^:{}]+)\):.*$', line)

        # Return match immediately when correctly formatted.
        if arg_match is not None:
            return True, arg_match.group(1), arg_match.group(2)

        # Type is not defined.
        arg_definition = line.split(':')[0]
        type_definition = arg_definition.split()
        if len(type_definition) == 1:
            self.add_message('type-not-defined',
                             node=node,
                             args=(type_definition[0], section_name))
            return True, type_definition[0], ""

        # Check the type definition with parenthesis.
        arg_name = type_definition[0]
        type_definition = " ".join(type_definition[1:])
        self.check_type_definition(node, type_definition, True)

        # Wrong format of the argument.
        self.add_message('wrong-argument-specification-syntax',
                         node=node,
                         args=arg_name)

        return True, arg_name, type_definition

    def match_strict_section(self, line):
        """A stricter version of self.match_section. That only returns true when the section was exactly matched.

        Args:
            line (str): Line to check whether it defines a section.

        Returns:
            bool, str: Whether section was found and its name.
        """
        section_match = re.match(r'^\s*(\w+):\s*$', line)
        # Section was found, also return name.
        if section_match is not None:
            return True, section_match.group(1)

        # Section was not found in exact format.
        return False, ''

    def match_section(self, node, line):
        """Checks whether the current line matches a section.

        Args:
            node (Any): Node the pylint message is connected to when linting error is found.
            line (str): Line of which to check of whether it starts a section.

        Returns:
            bool, str: Whether a section was found and what the name is of that section.
        """
        section_match = re.match(r'^\s*(\w+):\s*$', line)
        # Section was found, also return name.
        if section_match is not None:
            return True, section_match.group(1)

        # Section contains additional characters after the ':'.
        single_line_section_match = re.match(r'^\s*(\w+):.*$', line)
        if single_line_section_match is not None:
            section_name = single_line_section_match.group(1)
            self.add_message('section-wrong-format',
                             node=node,
                             args=section_name)
            return False, ''

        # More information was given after the section name.
        incorrect_section_match = re.match(r'^\s*((\w+).*):.*$', line)

        if incorrect_section_match is None:
            return False, ''

        # Section name is unknown to the linter.
        section_name = incorrect_section_match.group(2)
        for section in self.ordered_sections:
            if section.startswith(section_name):
                self.add_message('unknown-section',
                                 node=node,
                                 args=incorrect_section_match.group(1))
                break

        # No section match.
        return False, ''

    def check_type_definition(self, node, type_str, enclosing_parenthesis):
        """Check the type definitions inside a section.

        Args:
            node (Any): Node to connect message to.
            type_str (str): Type definition inside docstring
            enclosing_parenthesis (bool): Whether to enclose with parenthesis.
        """
        # Print message when type contains curly braces.
        if type_str.__contains__('{') or type_str.__contains__('}'):
            self.add_message('use-dict-keyword',
                             node=node,
                             args=type_str)

        if not enclosing_parenthesis:
            return

        # Print message when type definition has not been enclosed.
        if not type_str.startswith('(') or not type_str.endswith(')'):
            self.add_message('enclose-type-in-parenthesis',
                             node=node,
                             args=type_str)


def register(linter):
    """Required method to auto register this checker.

    Args:
        linter (pylint.lint.pylinter.PyLinter): Linter to which checks can be added.
    """
    linter.register_checker(DocstringContentChecker(linter))
