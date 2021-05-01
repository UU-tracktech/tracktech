"""Defines node class for scheduler with its connections to other nodes

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from typing import Callable, Any, List
import numpy as np
from processor.scheduling.component.component_interface import IComponent


class INode:
    """Node interface enforcing the implementation of functions needed
    by the scheduler and schedule node.

    Enforces the implementation of reset(), executable(), execute(notify), and assign(arg, arg_nr).
    """

    def reset(self) -> None:
        """Reset the node for the next iteration.

        Raises:
            NotImplementedError: occurs when this method is not overridden
            to ensure this function is defined.
        """
        raise NotImplementedError("Function to prepare the node for the next iteration, "
                                  "should also call on children/out nodes if applicable")

    def executable(self) -> bool:
        """Checks if the node is executable in its current state.

        Returns:
            Boolean indicating whether the node is ready to run or not.

        Raises:
            NotImplementedError: occurs when this method is not overridden
            to ensure this function is defined.
        """
        raise NotImplementedError("Function to indicate if the node can be run isn't implemented")

    def execute(self, notify: Callable[[List[Any]], None]) -> None:
        """Execute the component and pass output to next layer.

        Executes the component with the previously provided arguments.
        Pass the output of the component to nodes in the next layer.
        Notify the scheduler of nodes that can now be executed
        since the contained component has been run.

        Args:
            notify: function to pass nodes to that can be executed after the component was executed.

        Raises:
            NotImplementedError: occurs when this method is not overridden
            to ensure this function is defined.
        """
        raise NotImplementedError("Function should execute the associated internal component")

    def assign(self, arg: object, arg_nr: int) -> None:
        """Store argument for later component execution.

        Args:
            arg: argument to store for when the component is executed.
            arg_nr: index at which the argument is stored in the arguments array.

        Raises:
            NotImplementedError: occurs when this method is not overridden
            to ensure this function is defined.
        """
        raise NotImplementedError("Function to assign an input to a node"
                                  "as argument not implemented")
