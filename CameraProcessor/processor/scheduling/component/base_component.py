"""Simplest definition of a component

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from typing import Callable


from processor.scheduling.component.component_interface import IComponent


class BaseComponent(IComponent):
    """Base of every component containing only the minimal required functionality."""

    def work(self) -> object:
        """Example function that can be returned by execute_component()."""

    def execute_component(self) -> Callable:
        """See base class."""
        return self.work
