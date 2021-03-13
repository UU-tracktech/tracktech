from typing import Callable


from scheduling.component.component_interface import IComponent


class OutputComponent(IComponent):
    """Example output component without next layers.

    Contains a function to handle the output that falls outside of the scheduler.

    Arguments:
        func: function to handle outputs send outside of the schedulers graph.
        out: contains output, only here for example_plan.py to retrieve output.
    """

    def __init__(self, func):
        """Inits IntermediaryOutputComponent with output handling function.

        Args:
            func: function to handle outputs send outside of the schedulers graph.
        """
        self.func = func

        self.out = None

    def work(self, obj) -> object:
        """Example function with single argument that can be returned by execute_component().

        Outputs to object outside of scheduler and there is no next layer to pass objects to.
        """
        self.out = obj

        self.func(self.out)
        return None

    def execute_component(self) -> Callable:
        """See base class."""
        return self.work


class IntermediaryOutputComponent(IComponent):
    """Example output component with next layers.

    Contains a function to handle the output that falls outside of the scheduler.

    Arguments:
        func: function to handle outputs send outside of the schedulers graph.
    """

    def __init__(self, func):
        """Inits IntermediaryOutputComponent with output handling function.

        Args:
            func: function to handle outputs send outside of the schedulers graph.
        """
        self.func = func

    def work(self, obj) -> object:
        """Example function with single argument that can be returned by execute_component().

        Args:
            obj: example object.

        Returns:
            Possibly modified object used by the next layer.
        """
        output = obj

        self.func(output)
        return obj

    def execute_component(self) -> Callable:
        """See base class."""
        return self.work
