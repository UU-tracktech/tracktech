"""Component that returns any function.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.component_interface import IComponent


class FuncCallComponent(IComponent):
    """Component that holds a single function that can be run by the Scheduler.
    """

    def __init__(self, func):
        """Inits FuncCallComponent.

        Args:
            func (function): function to pass to scheduler.
        """
        self.__func = func

    def execute_component(self):
        """See base class."""
        return self.__func
