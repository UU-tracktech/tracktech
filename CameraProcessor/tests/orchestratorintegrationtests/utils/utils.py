""" Utility module that implements a time out function and custom __eq__ function to be shared across tests

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
