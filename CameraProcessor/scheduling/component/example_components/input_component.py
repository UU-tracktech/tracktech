from typing import Callable


from scheduling.component.component_interface import IComponent


class InputComponent(IComponent):
    def work(self, obj) -> object:
        return obj

    def execute_component(self) -> Callable:
        return self.work
