"""Example component that points to other components and has output.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.i_component import IComponent


class OutputComponent(IComponent):
    """Example output component without next layers.

    Contains a function to handle the output that falls outside the scheduler.

    Attributes:
        func (Function): function to handle outputs send outside the schedulers graph.
        out (object): contains output, only here for example_plan.py to retrieve output.
    """

    def __init__(self, func):
        """Inits IntermediaryOutputComponent with output handling function.

        Args:
            func (Function): function to handle outputs send outside the schedulers graph.
        """
        self.func = func

        self.out = None

    def work(self, obj):
        """Example function with single argument that can be returned by execute_component().

        Outputs to object outside of scheduler and there is no next layer to pass objects to.

        Args:
            obj (object): Any argument can get used by the work function.

        Returns:
            object: output of function that processed self.out.
        """
        self.out = obj

        return self.func(self.out)

    def execute_component(self):
        """See base class."""
        return self.work
