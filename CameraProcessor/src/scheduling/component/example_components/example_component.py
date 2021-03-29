from typing import Callable


from src.scheduling.component.component_interface import IComponent


class ExampleComponent(IComponent):
    """Example component with a work function containing multiple inputs."""

    def work(self, first_arg, second_arg) -> object:
        """Example function with multiple arguments that can be returned by execute_component().

        Args:
            first_arg: example argument.
            second_arg: another example argument.

        Returns:
            A list of both inputs for the next layer.
        """
        return [first_arg, second_arg]

    def execute_component(self) -> Callable:
        """See base class."""
        return self.work
