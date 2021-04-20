"""Tests the scheduler node class which implements the INode interface

"""
import pytest
from processor.scheduling.node.schedule_node import ScheduleNode
from tests.unittests.scheduling.utils.input_component import InputComponent


# pylint: disable=attribute-defined-outside-init
class TestScheduleNode:
    """Tests Scheduler node behavior
    """
    def test_schedule_node_constructor(self, example_schedule_node):
        """Tests the constructor of the node

        Args:
            example_schedule_node (INode): Example node
        """
        assert example_schedule_node.input_count == example_schedule_node.needed_args
        assert len(example_schedule_node.arguments) == example_schedule_node.input_count
        assert example_schedule_node.component

    def test_node_assign(self):
        """Tests the functionality of INode: reset().

        """
        schedule_node = ScheduleNode(3, [(), ()], InputComponent())
        assert all([not arg for arg in schedule_node.arguments])
        schedule_node.assign('val', 2)
        assert schedule_node.arguments[2] == 'val'

    def test_node_reset(self):
        """Tests the functionality of INode: executable().

        """
        schedule_node = ScheduleNode(3, [(), ()], InputComponent())
        schedule_node.assign('val', 2)
        schedule_node.reset()
        assert all([not arg for arg in schedule_node.arguments])

    def test_node_executable(self, example_schedule_node):
        """Whether the node is executable is correctly

        Args:
            example_schedule_node (INode): Example node and see whether it can be executed straight away
        """
        executable = example_schedule_node.input_count <= 0
        assert executable == example_schedule_node.executable()

    def test_fill_node_arguments(self):
        """Fill arguments of nodes and see if it becomes executable

        """
        schedule_node = ScheduleNode(3, [(), ()], InputComponent())
        assert not schedule_node.executable()
        schedule_node.assign('val', 0)
        schedule_node.assign('val', 1)
        schedule_node.assign('val', 2)
        assert schedule_node.executable()

    def test_override_argument_raises_error(self):
        """Tests the functionality of INode: execute().

        """
        schedule_node = ScheduleNode(3, [], InputComponent())
        schedule_node.assign('val', 2)
        assert pytest.raises(Exception, schedule_node.assign, 'val', 2)

    def test_argument_out_of_range(self):
        """Assigned argument out of range raises exception

        """
        schedule_node = ScheduleNode(1, [], InputComponent())
        assert pytest.raises(IndexError, schedule_node.assign, 'val', 2)


if __name__ == '__main__':
    pytest.main(TestScheduleNode)
