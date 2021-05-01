""" Utility module that implements a time out function and custom __eq__ function to be shared across tests

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

PC_URL = 'ws://processor-orchestrator-service/processor'
IF_URL = 'ws://processor-orchestrator-service/client'


def __eq__(self, other):
    """Custom equalize function

    Args:
        self: first object to compare
        other: second object to compare

    Returns: bool

    """
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False
