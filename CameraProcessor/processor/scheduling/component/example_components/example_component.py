"""An example component.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


from processor.scheduling.component.i_component import IComponent


class ExampleComponent(IComponent):
    """Example component with a work function containing multiple inputs."""

    @staticmethod
    def work(first_arg, second_arg):
        """Example function with multiple arguments that can be returned by execute_component().

        Args:
            first_arg (obj): Example argument that gets appended to list.
            second_arg (obj): Example argument that gets appended to list.

        Returns:
            [object]: A list of both inputs for the next layer.
        """
        return [first_arg, second_arg]

    def execute_component(self):
        """See base class."""
        return self.work
