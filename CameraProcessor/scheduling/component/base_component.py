from typing import Callable


from scheduling.component.component_interface import IComponent


class BaseComponent(IComponent):
    """Base of every component containing only the minimal required functionality."""

    def work(self) -> object:
        """Example function that can be returned by execute_component()."""
        pass

    def execute_component(self) -> Callable:
        """See base class."""
        return self.work
