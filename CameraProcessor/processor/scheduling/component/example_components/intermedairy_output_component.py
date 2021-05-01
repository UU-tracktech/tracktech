"""Example component that points to other components and has output

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from typing import Callable


from processor.scheduling.component.component_interface import IComponent


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
