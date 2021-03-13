from typing import Callable


from scheduling.component.component_interface import IComponent


class ExampleComponent(IComponent):
    def work(self, first_arg, second_arg) -> object:
        return [first_arg, second_arg]

    def execute_component(self) -> Callable:
        return self.work
