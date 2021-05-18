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
            x1 (float): normalized left most X.
            y1 (float): normalized top most Y.
            x2 (float): normalized right most X.
            y2 (float): normalized bottom most Y.
        """
        if x1 > x2:
            raise ValueError(f'x1 {x1} should be smaller than or equal to x2 {x2}')
        if y1 > y2:
            raise ValueError(f'y1 {y1} should be smaller than or equal to y2 {y2}')

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

    def get_x1(self):
        """Getter for right X coord of rectangle.

        Returns:
            (float): normalized right most X.
        """
        return self.__x1

    def get_y1(self):
        """Getter for bottom Y coord of rectangle.

        Returns:
            (float): normalized bottom most Y.
        """
        return self.__y1

    def get_x2(self):
        """Getter for left X coord of rectangle.

        Returns:
            (float): normalized left most X.
        """
        return self.__x2

    def get_y2(self):
        """Getter for top Y coord of rectangle.

        Returns:
            (float): normalized top most Y.
        """
        return self.__y2
