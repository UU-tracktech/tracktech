from typing import Callable


from scheduling.component.component_interface import IComponent


class BaseComponent(IComponent):
    """
    This is the least
    """
    def work(self) -> object:
        """

        """
        pass

    def execute_component(self) -> Callable:
        return self.work
