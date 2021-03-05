from typing import Callable


class IComponent:
    def execute_component(self) -> Callable:
        raise NotImplementedError("Execute has to return a function which the scheduler can run. \n "
                                  "The inputs of this function must contain all inputs to the node.")
