"""Main file running the video processing pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class TestClass:
    """Class."""
    def classmethod1(self):
        """Test method without a dot in docstring."""
        return

    def classmethod2(self):
        """Test method with a dot.

        Args:
            self (Sdf): comment without a dot
        """
        return

    def classmethod3(self, param1):
        """SDFSDF."""
        return param1

    def classmethod4(self, param1):
        """SDFSDF.

        Args:
            param1 (Dummy): comment with a .
        """
        return param1

    def classmethod5(self, param1, param2):
        """SDFSDF.

        Args:
            param2 (D): param2.
            param1 (s): param1.
        """
        return param1, param2

    def classmethod6(self, param1, param2):
        """SDFSDF.

        Args:
            param1 (s): param1.
        """
        return param1, param2

    def classmethod7(self, param1):
        """SDFSDF.

        Args:
            param2 (s): non-existing param.
        """
        return param1

    def classmethod8(self, param1, param2):
        """SDFSDF.

        Args:
            param1 (D): param2.
            param2 (s): param1.
        """
        return param1, param2

    def classmethod9(self, param1, param2):
        """SDFSDF.

        Args:
            param1 (D): param2.
            param2 (s): param1.
            param3 (s): dfsdf.
        """
        return param1, param2
