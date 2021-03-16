from typing import Callable


from scheduling.component.component_interface import IComponent


class ScheduleInputComponent(IComponent):
    def work(self, obj) -> object:
        return obj

    def execute_component(self) -> Callable:
        return self.work


class ScheduleOutputComponent(IComponent):
    def __init__(self):
        self.out = None

    def work(self, obj) -> object:
        self.out = obj
        return None

    def execute_component(self) -> Callable:
        return self.work

    def get_out(self) -> object:
        out_obj = self.out
        self.out = None
        return out_obj


class ExampleComponent(IComponent):
    def work(self, first_arg, second_arg) -> object:
        return [first_arg, second_arg]

    def execute_component(self) -> Callable:
        return self.work
