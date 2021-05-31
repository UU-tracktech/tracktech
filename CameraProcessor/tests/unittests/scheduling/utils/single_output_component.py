"""Contains an example component.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.component_interface import IComponent


class SingleOutputComponent(IComponent):
    """Example component with a work function containing multiple inputs."""
    @staticmethod
    def work(args):
        """Example function with multiple arguments that can be returned by execute_component().

        Args:
            args ([object]): two arguments.

        Returns:
            str: A list of both inputs for the next layer.
        """
        first_arg, second_arg = args
        return first_arg + "," + second_arg + ",merged"

    def execute_component(self):
        """See base class.

        Returns:
            func: work function.
        """
        return self.work
