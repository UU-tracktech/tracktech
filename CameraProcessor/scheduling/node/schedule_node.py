from typing import Callable, Any
import numpy as np


from scheduling.component.component_interface import IComponent


class INode:
    """Node interface enforcing the implementation of functions needed by the scheduler and schedule node.

    Enforces the implementation of reset(), executable(), execute(notify), and assign(arg, arg_nr).
    """

    def executable(self) -> bool:
        """Checks if the node is executable in its current state.

        Returns:
            Boolean indicating whether the node is ready to run or not.

        Raises:
            NotImplementedError: occurs when this method is not overridden to ensure this function is defined.
        """
        raise NotImplementedError("Function to indicate if the node can be run isn't implemented")

    def execute(self, notify: Callable[[list[Any]], None]) -> None:
        """Execute the component and pass output to next layer.

        Executes the component with the previously provided arguments.
        Pass the output of the component to nodes in the next layer.
        Notify the scheduler of nodes that can now be executed since the contained component has been run.

        Args:
            notify: function to pass nodes to that can be executed after the component was executed.

        Raises:
            NotImplementedError: occurs when this method is not overridden to ensure this function is defined.
        """
        raise NotImplementedError("Function should execute the associated internal component")

    def assign(self, arg: object, arg_nr: int) -> None:
        """Store argument for later component execution.

        Args:
            arg: argument to store for when the component is executed.
            arg_nr: index at which the argument is stored in the arguments array.

        Raises:
            NotImplementedError: occurs when this method is not overridden to ensure this function is defined.
        """
        raise NotImplementedError("Function to assign an input to a node as argument not implemented")


class ScheduleNode(INode):
    """Schedule node used by scheduler to schedule and ensure a minimum required order of execution.

    Arguments:
        input_count: total amount of arguments necessary to execute the component.
        out_nodes: tuples of nodes in the next layer together with argument index to push argument to.
        component: component to execute once the scheduler calls the node (all needed arguments should be ready).
        needed_args: amount of arguments still needed to execute the component.
        arguments: array of all arguments provided so far.
    """

    def __init__(self, input_count: int, out_nodes: [(INode, int)], component: IComponent):
        """Inits ScheduleNode with information about the next layer and the component to execute.

        Args:
            input_count: total amount of arguments necessary to execute the component.
            out_nodes: tuples of nodes in the next layer together with argument index to push argument to.
            component: component to execute once the scheduler calls the node (all needed arguments should be ready).
        """
        self.input_count = input_count
        self.out_nodes = out_nodes
        self.component = component

        self.needed_args = self.input_count
        self.arguments = np.empty(self.needed_args, dtype=object)

    def reset(self) -> None:
        """Resets the node for the next iteration.

        Empties arguments array and resets amount of needed arguments.
        """
        self.needed_args = self.input_count

        # Keeping the numpy array and only emptying would be preferred
        self.arguments = np.empty(self.needed_args, dtype=object)

    def executable(self) -> bool:
        """Checks whether all arguments needed for execution are provided.

        Returns:
            true if all arguments have been provided, false otherwise.
        """
        return self.needed_args <= 0

    def execute(self, notify: Callable[[list[INode]], None]) -> None:
        """Execute the component and pass output to next layer.

        Executes the component with the previously provided arguments in the arguments array.
        Throws error if node isn't executable.
        Pass the output of the component to nodes in the next layer by looping over all nodes in the next layer.
        Notify the scheduler of nodes that can now be executed since the contained component has been run.
        Reset the node.

        Args:
            notify: function to pass nodes to that can be executed after the component was executed.

        Raises:
            Exception: node is not ready to execute.
        """
        if not self.executable():
            raise Exception("Can't call function without the function's arguments being complete")

        # Fold arguments into components work function and receive component output.
        out = self.component.execute_component()(*self.arguments)

        ready_nodes: list[INode] = []

        # Assign output of component to all nodes in the next layer.
        for (node, arg_nr) in self.out_nodes:
            node.assign(out, arg_nr)

            # Check if node is ready after previous assign was performed.
            if node.executable():
                ready_nodes.append(node)

        # Notify the scheduler of all nodes that can now be executed.
        notify(ready_nodes)

        # Reset node state for next iteration.
        self.reset()

    def assign(self, arg: object, arg_nr: int) -> None:
        """Store argument for later component execution in the arguments array.

        Args:
            arg: argument to store for when the component is executed.
            arg_nr: index at which the argument is stored in the arguments array.

        Raises:
            IndexError: wrong index for the argument was given.
            Exception: argument is provided twice, existing argument would be overwritten.
        """
        if len(self.arguments) <= arg_nr:
            raise IndexError(f"Index {arg_nr} too large for arguments array with size {len(self.arguments)}")

        # Ensure previously supplied argument isn't overwritten.
        if self.arguments[arg_nr] is None:
            self.arguments[arg_nr] = arg

            self.needed_args -= 1
        else:
            raise Exception("Argument should only be provided once by the scheduler, "
                            "this indicates unnecessary execution by the scheduler")
