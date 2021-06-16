"""IComponent class that enforces certain methods to be implemented.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class IComponent:
    """The component interface enforcing the implementation of execute_component()."""

    def execute_component(self):
        """Function used by INode to execute the component.

        Specifies the function that used to perform an iteration using the component.
        Function contains all inputs from input nodes as separate arguments
        (1 argument per input node).

        Returns:
           func: A function that hasn't been applied containing all inputs as separate arguments.

        Raises:
            NotImplementedError: occurs when this method is not overridden to ensure this function is defined.
        """
        raise NotImplementedError("Execute has to return a function, which"
                                  "the scheduler can run. \n "
                                  "The inputs of this function must contain"
                                  "all inputs to the node.")
