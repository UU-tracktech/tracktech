from typing import Callable


from src.scheduling.component.component_interface import IComponent


class InputComponent(IComponent):
    """Example input component.

    Work function must contain one argument,
    because the current scheduler can only pass one argument to the initial node.
    """

    def work(self, obj) -> object:
        """Example function with single argument that can be returned by execute_component().

        Args:
            obj: input object passed through by scheduler.

        Returns:
            Modified object used by the next layer.
        """
        return obj

    def execute_component(self) -> Callable:
        """See base class."""
        return self.work
