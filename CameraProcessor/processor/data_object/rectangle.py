"""Rectangle containing bottom right and top left coords.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class Rectangle:
    """Rectangle class containing bottom right and top left corner points."""
    def __init__(self, x1, y1, x2, y2):
        """Inits rectangle with bottom right and top left coords.

        Args:
            x1 (float): normalized top-left X.
            y1 (float): normalized top-left Y.
            x2 (float): normalized bottom-right X.
            y2 (float): normalized bottom-right Y.
        """
        # Rounding for float precision errors errors.
        if round(x1, 2) > round(x2, 2):
            raise ValueError(f'x1 {x1} should be smaller than or equal to x2 {x2}')
        if round(y1, 2) > round(y2, 2):
            raise ValueError(f'y1 {y1} should be smaller than or equal to y2 {y2}')

        if round(x1, 2) < 0 or round(y1, 2) < 0:
            raise ValueError(f'x1 {x1} and y1 {y1} should be greater than or equal to 0')
        if round(x2, 2) > 1 or round(y2, 2) > 1:
            raise ValueError(f'x2 {x2} and y2 {y2} should be smaller than or equal to 1')

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

    @property
    def x1(self):
        """Getter for top-left X coordinate of rectangle.

        Returns:
            (float): normalized right most X.
        """
        return self.__x1

    @property
    def y1(self):
        """Getter for top-left Y coordinate of rectangle.

        Returns:
            (float): normalized bottom most Y.
        """
        return self.__y1

    @property
    def x2(self):
        """Getter for bottom-right X coordinate of rectangle.

        Returns:
            (float): normalized left most X.
        """
        return self.__x2

    @property
    def y2(self):
        """Getter for bottom-right Y coordinate of rectangle.

        Returns:
            (float): normalized top most Y.
        """
        return self.__y2

    def __eq__(self, other):
        """Checks whether the two rectangles are equal.

        Args:
            other (Rectangle): Other rectangle to compare with.

        Returns:
            bool: Whether self and other are the same.
        """
        return all([self.x1 == other.x1, self.x2 == other.x2, self.y1 == other.y1, self.y2 == other.y2])

    def __repr__(self):
        """Converts the rectangle object to a string.

        Returns:
            str: String representation of a Rectangle.
        """
        return f'Rectangle(x1:{self.__x1:.3f} y1:{self.__y1:.3f} x2:{self.__x2:.3f} y2:{self.__y2:.3f})'
