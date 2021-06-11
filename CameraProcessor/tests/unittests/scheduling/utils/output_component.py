"""Contains an example component.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.component_interface import IComponent


class OutputComponent(IComponent):
    """Example output component without next layers.

    Contains a function to handle the output that falls outside the scheduler.

    Attributes:
        func (func): Function to handle outputs send outside the schedulers graph.
        out (object): Contains output, only here for example_plan.py to retrieve output.
    """

    def __init__(self, func):
        """Inits IntermediaryOutputComponent with output handling function.

        Args:
            func (func): function to handle outputs send outside the schedulers graph.
        """
        self.func = func
        self.out = None

    def work(self, obj):
        """Example function with single argument that can be returned by execute_component().

        Outputs to object outside of scheduler and there is no next layer to pass objects to.

        Args:
            obj (object): Any object passed to function.

        Returns:
            object: The resulting object from component function.
        """
        self.out = obj

        return self.func(self.out)

    def execute_component(self):
        """See base class.

        Returns:
            func: Work function to call when component is ran.
        """
        return self.work
