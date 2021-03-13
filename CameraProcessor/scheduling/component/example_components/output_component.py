from typing import Callable


from scheduling.component.component_interface import IComponent


class OutputComponent(IComponent):
    def __init__(self, func):
        self.func = func

    def work(self, obj) -> object:
        output = obj

        self.func(output)
        return None

    def execute_component(self) -> Callable:
        return self.work


class IntermediaryOutputComponent(IComponent):
    def __init__(self, func):
        self.func = func

    def work(self, obj) -> object:
        output = obj

        self.func(output)
        return obj

    def execute_component(self) -> Callable:
        return self.work
