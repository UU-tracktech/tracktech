"""Contains an example component.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.i_component import IComponent


class MultipleInputComponent(IComponent):
    """Example component with a work function containing multiple inputs."""

    @staticmethod
    def work(first_arg, second_arg):
        """Example function with multiple arguments that can be returned by execute_component().

        Args:
            first_arg (str): example argument.
            second_arg (str): another example argument.

        Returns:
            [str]: A list of both inputs for the next layer.
        """
        first_arg = first_arg.__add__("'first_arg')
        second_arg = second_arg.__add__(',second_arg')
        return [first_arg, second_arg]

    def execute_component(self):
        """Interface function to execute the component.

        Returns:
            func: Work function to call when component is run.
        """
        return self.work
