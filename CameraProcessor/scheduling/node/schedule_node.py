from typing import Callable, Any
import numpy as np


from scheduling.component.component_interface import IComponent


class INode:
    def reset(self) -> None:
        raise NotImplementedError("Function to prepare the node for the next iteration, "
                                  "should also call on children/out nodes if applicable")

    def executable(self) -> bool:
        raise NotImplementedError("Function to indicate if the node can be run isn't implemented")

    def execute(self, notify: Callable[[list[Any]], None]) -> None:
        raise NotImplementedError("Function should execute the associated internal component")

    def assign(self, arg: object, arg_nr: int) -> None:
        raise NotImplementedError("Function to assign an input to a node as argument not implemented")


class ScheduleNode(INode):
    def __init__(self, input_count: int, out_nodes: [(INode, int)], component: IComponent):
        self.input_count = input_count
        self.out_nodes = out_nodes
        self.component = component

        self.needed_args = self.input_count
        self.arguments = np.empty(self.needed_args, dtype=object)

    def reset(self) -> None:
        self.needed_args = self.input_count

        # Keeping the numpy array and only emptying would be preferred
        self.arguments = np.empty(self.needed_args, dtype=object)

    def executable(self) -> bool:
        return self.needed_args <= 0

    def execute(self, notify: Callable[[list[INode]], None]) -> None:
        if self.executable():
            raise Exception("Can't call function without the function's arguments being complete")

        out = self.component.execute_component()(*self.arguments)

        ready_nodes: list[INode] = []

        for (node, arg_nr) in self.out_nodes:
            node.assign(out, arg_nr)

            if node.executable():
                ready_nodes.append(node)

        notify(self, ready_nodes)

    def assign(self, arg: object, arg_nr: int) -> None:
        if len(self.arguments) < arg_nr:
            raise IndexError(f"Index too large {arg_nr} for arguments array with size {len(self.arguments)}")

        if self.arguments[arg_nr] is None:
            self.arguments[arg_nr] = arg

            self.needed_args -= 1
        else:
            raise Exception("Argument should only be provided once by the scheduler, "
                            "this indicates unnecessary execution by the scheduler")
