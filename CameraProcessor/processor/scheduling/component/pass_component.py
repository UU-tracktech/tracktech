"""Component that takes an input and passes it on to the next layer(s).

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.i_component import IComponent


class PassComponent(IComponent):
    """Component that passes each object it is given as input to the next stage as output."""

    def pass_input(self, passed_input):
        """Instantly passes input as output.

        Args:
            passed_input (object): Any input that is passed to the component.
        """
        return passed_input

    def execute_component(self):
        """See base class."""
        return self.pass_input
