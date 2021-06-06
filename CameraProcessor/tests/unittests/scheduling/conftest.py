"""Fixtures for scheduling tester.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from tests.unittests.scheduling.utils.input_component import InputComponent
from processor.scheduling.node.schedule_node import ScheduleNode


@pytest.fixture(params=[
    ScheduleNode(0, [], InputComponent(), {}),
    ScheduleNode(1, [()], InputComponent(), {}),
    ScheduleNode(2, [(), ()], InputComponent(), {})
])
def example_schedule_node(request):
    """Several examples of schedule nodes.

    Args:
        request ([ScheduleNode]): different implementations of a schedule node.

    Returns:
        ScheduleNode: A schedule node containing an input component.
    """
    return request.param
