"""Contains an example component.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class InputComponent:
    """Test input component.

    Work function must contain one argument,
    because the current scheduler can only pass one argument to the initial node.
    """
    @staticmethod
    def work(obj):
        """Example function with single argument that can be returned by execute_component().

        Args:
            obj (str): input object passed through by the scheduler.

        Returns:
            str: The modified object used by the next layer.
        """
        obj = obj.__add__(',start')
        return obj

    def execute_component(self):
        """Interface function to execute the component.

        Returns:
            func: Work function to call when component is run.
        """
        return self.work
