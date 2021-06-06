"""Tests Rectangle by checking properties.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
from processor.data_object.rectangle import Rectangle


# pylint: disable=attribute-defined-outside-init,no-member
class TestRectangle:
    """Testing Rectangle.

    Attributes:
        data (Rectangle): Example rectangle.
        tlx1 (float): Top left corner x coordinate.
        tly1 (float): Top left corner y coordinate.
        brx2 (float): Bottom right corner x coordinate.
        brx2 (float): Bottom right corner y coordinate.
    """
    def setup_method(self):
        """Setup method."""
        self.data = Rectangle(0, 0.1, 0.9, 1)
        self.tlx1 = self.data.x1
        self.tly1 = self.data.y1
        self.brx2 = self.data.x2
        self.bry2 = self.data.y2

    def test_coordinate_values(self):
        """Tests coordinate values."""
        assert all([self.tlx1 == 0,
                    self.tly1 == 0.1,
                    self.brx2 == 0.9,
                    self.bry2 == 1])

    def test_init(self):
        """Tests entire Rectangle object."""
        assert self.data == Rectangle(0, 0.1, 0.9, 1)
        assert self.data != Rectangle(0, 0.1, 0.5, 1)
        assert Rectangle(self.tlx1, self.tly1, self.brx2, self.bry2) == Rectangle(0, 0.1, 0.9, 1)

    def test_invalid_rectangle_values(self):
        """Tests whether an error is raised when the values in the rectangle are invalid."""
        with pytest.raises(ValueError):
            Rectangle(-0.1, 0, 0, 0)
        with pytest.raises(ValueError):
            Rectangle(0, -0.1, 0, 0)
        with pytest.raises(ValueError):
            Rectangle(0, 0, 1.1, 0)
        with pytest.raises(ValueError):
            Rectangle(0, 0, 0, 1.1)

    def test_invalid_rectangle_coordinate_order(self):
        """Tests whether an error is raised when the values in the rectangle are in invalid order.

        Tests whether x1 is always greater than x1 and tests whether y0 is always greater than y1.
        """
        with pytest.raises(ValueError):
            Rectangle(0.5, 0.5, 0.1, 0.5)
        with pytest.raises(ValueError):
            Rectangle(0.5, 0.5, 0.5, 0.1)
        with pytest.raises(ValueError):
            Rectangle(0.5, 0.5, 0.1, 0.1)


if __name__ == '__main__':
    pytest.main(TestRectangle)
