from typing import Callable


class IComponent:
    """Component interface enforcing the implementation of execute_component()."""

    def execute_component(self) -> Callable:
        """Function used by INode to execute the component.

        Specifies the function that used to perform an iteration using the component.
        Function contains all inputs from input nodes as separate arguments (1 argument per input node).

        Returns:
            A function that hasn't been applied containing all inputs as separate arguments.

        Raises:
            NotImplementedError: occurs when this method is not overridden to ensure this function is defined.
        """
        raise NotImplementedError("Execute has to return a function which the scheduler can run. \n "
                                  "The inputs of this function must contain all inputs to the node.")
