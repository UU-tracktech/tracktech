"""Tests the scheduler node class, which implements the INode interface.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from tests.unittests.scheduling.utils.input_component import InputComponent
from processor.scheduling.node.schedule_node import ScheduleNode


class TestScheduleNode:
    """Tests Scheduler node behavior."""
    def test_schedule_node_constructor(self, example_schedule_node):
        """Tests the constructor of the node.

        Args:
            example_schedule_node (INode): Example node.
        """
        assert example_schedule_node.component

    def test_node_executable(self, example_schedule_node):
        """Checks whether the node is executable is correctly.

        Args:
            example_schedule_node (INode): Example node and see whether it can be executed straight away.
        """
        executable = example_schedule_node.input_count <= 0
        assert executable == example_schedule_node.executable()

    def test_non_executable_node(self):
        """Not executable node should raise an exception."""
        schedule_node = ScheduleNode(3, [(), ()], InputComponent(), {})
        assert pytest.raises(Exception, schedule_node.execute, print)

    def test_fill_node_arguments(self):
        """Fill arguments of nodes and see if it becomes executable."""
        schedule_node = ScheduleNode(3, [(), ()], InputComponent(), {})
        assert not schedule_node.executable()
        schedule_node.assign('val', 0)
        schedule_node.assign('val', 1)
        schedule_node.assign('val', 2)
        assert schedule_node.executable()

    def test_override_argument_raises_error(self):
        """Tests the functionality of INode: execute()."""
        schedule_node = ScheduleNode(3, [], InputComponent(), {})
        schedule_node.assign('val', 2)
        assert pytest.raises(Exception, schedule_node.assign, 'val', 2)

    def test_argument_out_of_range(self):
        """Assigned argument out of range raises exception."""
        schedule_node = ScheduleNode(1, [], InputComponent(), {})
        assert pytest.raises(IndexError, schedule_node.assign, 'val', 2)


if __name__ == '__main__':
    pytest.main(TestScheduleNode)
