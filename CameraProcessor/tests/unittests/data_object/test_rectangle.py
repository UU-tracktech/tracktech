"""Tests frame object by checking properties and whether drawing changes something

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest
from processor.data_object.rectangle import Rectangle


# pylint: disable=attribute-defined-outside-init,no-member
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


class TestRectangle:
    """Testing Rectangle."""

    def setup_method(self):
        """Setup method."""
        self.data = Rectangle(0, 0, 1, 1)
        self.x1 = self.data.get_x1()
        self.y1 = self.data.get_y1()
        self.x2 = self.data.get_x2()
        self.y2 = self.data.get_y2()

    def test_x1_value(self):
        """Tests x1 value."""
        assert self.x1 == 0

    def test_y1_value(self):
        """Tests y1 value."""
        assert self.y1 == 0

    def test_x2_value(self):
        """Tests x2 value."""
        assert self.x2 == 1

    def test_y2_value(self):
        """Tests y2 value."""
        assert self.y2 == 1

    def test_rectrangle(self):
        """Tests entire Rectangle object."""
        assert self.data.__eq__(Rectangle(0, 0, 1, 1))
        assert Rectangle(self.x1, self.y1, self.x2, self.y2).__eq__(Rectangle(0, 0, 1, 1))


if __name__ == '__main__':
    pytest.main(TestRectangle)