"""Checks the regular single line # comments.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import re

from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker


class CommentChecker(BaseChecker):
    """Checks whether the comment has the correct format.

    The following linting errors get caught:
        comment-should-have-one-space: Comment should start with only one space.
        comment-missing-dot: Comment has to end with a dot.
        comment-starts-with-lowercase: Comment should start with uppercase letter.

    Attributes:
        __implements__ (IRawChecker): Raw checker in order to enumerate through the lines.
        name (str): Name of the checker.
        msgs (dict[str, (str, str, str)]): Dictionary with error codes and pylint messages.
    """

    __implements__ = IRawChecker

    name = 'comment-checker'
    msgs = {
        'C3120': ('Start comment with one space',
                  'comment-should-have-one-space',
                  'Comment is missing a space'
                  ),
        'C3121': ("Comment missing a dot",
                  'comment-missing-dot',
                  'Comment is missing a dot'
                  ),
        'C3122': ("Comment should start with capital letter",
                  'comment-starts-with-lowercase',
                  'Comment is wrongly formatted'
                  ),
        }

    def process_module(self, node):
        """Process a module and checks whether the comments inside are correctly formatted.

        Args:
            node (astroid.scoped_nodes.Module): Module definition containing the raw content of the file
        """
        # Go through each line.
        with node.stream() as stream:
            for (lineno, line) in enumerate(stream):
                # Decode the line and only continue if it is a comment.
                line = line.decode('utf-8').strip()
                if not str(line).startswith('#'):
                    continue

                # Check whether comment is correct format.
                comment_match = re.match(r'#\s[A-Z].*\.', line)
                if comment_match is not None:
                    continue

                # See what is wrong about the comment.
                wrong_spaces_match = re.match(r'#(?:\S|\s\s+).*', line)
                missing_dot_match = re.match(r'#.*[^.]$', line)
                capital_letter_match = re.match(r'#\s\S.*\.', line)

                # Wrong spaces inside the comment.
                if wrong_spaces_match is not None:
                    self.add_message('comment-should-have-one-space',
                                     line=lineno + 1)
                # Comment does not end with a dot.
                if missing_dot_match is not None:
                    self.add_message('comment-missing-dot',
                                     line=lineno + 1)
                # Comment misses the capital letter.
                if capital_letter_match is not None:
                    self.add_message('comment-starts-with-lowercase',
                                     line=lineno + 1)


def register(linter):
    """Required method to auto register this checker.

    Args:
        linter (pylint.lint.pylinter.PyLinter): Linter to which checks can be added.
    """
    linter.register_checker(CommentChecker(linter))
