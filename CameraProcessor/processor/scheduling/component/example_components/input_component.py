"""Component that gets input from previous stage.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


from processor.scheduling.component.component_interface import IComponent


class InputComponent(IComponent):
    """Example input component.

    Work function must contain one argument,
    because the current scheduler can only pass one argument to the initial node.
    """

    @staticmethod
    def work(obj):
        """Example function with single argument that can be returned by execute_component().

        Args:
            obj (object): Input object passed through by scheduler.

        Returns:
            object: Modified object used by the next layer.
        """
        return obj

    def execute_component(self):
        """See base class."""
        return self.work
