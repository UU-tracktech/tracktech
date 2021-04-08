""" Utility module that implements a time out function and custom __eq__ function to be shared across tests

"""

from async_timeout import timeout


def with_timeout(time):
    """Time out function for testing

    Args:
        time: seconds as integer

    Returns: async timer

    """

    def wrapper(corofunc):
        async def run(*args, **kwargs):
            with timeout(time):
                return await corofunc(*args, **kwargs)
        return run
    return wrapper


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
