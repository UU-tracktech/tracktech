"""Use a schedule wrapper to create a schedule and easily test some properties.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from tests.unittests.scheduling.utils.schedule_wrapper import ScheduleWrapper


class TestScheduler:
    """Tests functionality of scheduler class with different Schedules."""
    def test_empty_scheduler_constructor(self):
        """Tests the constructor initialization of an empty scheduler."""
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_empty_schedule()
        scheduler = schedule_wrapper.scheduler

        # Assert scheduler node initialization properties.
        assert scheduler.start_node == schedule_wrapper.schedule_input_node

    def test_big_scheduler_constructor(self):
        """Tests the constructor when a big schedule is created."""
        # Create a big schedule.
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_big_schedule()
        scheduler = schedule_wrapper.scheduler

        # Test properties.
        assert scheduler.start_node == schedule_wrapper.schedule_input_node

    def test_small_schedule_graph(self):
        """Tests whether a schedule only containing an output node gives correct output."""
        # Create an empty schedule.
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_empty_schedule()
        scheduler = schedule_wrapper.scheduler

        # Executes schedule.
        scheduler.schedule_graph(["small"], {})

        # No stage inside the schedule modified the string.
        assert schedule_wrapper.schedule_output_node.component.out == "small"

    def test_schedule_graph(self):
        """Tests the functionality of schedule_graph().

        Inside schedule_graph the schedule is executed
        See exact schedule ran in schedule_wrapper.py
        Each node adds to the string.
        """
        # Creates big schedule.
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_big_schedule()
        scheduler = schedule_wrapper.scheduler

        # Initialize graph with a simple string.
        scheduler.schedule_graph(['big'], {})

        assert schedule_wrapper.schedule_output_node.component.out == \
               'big,start,start,first_arg,big,start,start,second_arg,merged'

    def test_non_executable_graph(self):
        """Test whether an non-executable graph indeed raises an exception."""
        # Creates invalid schedule.
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_invalid_schedule()
        scheduler = schedule_wrapper.scheduler

        # Not yet executable since not all arguments are filled.
        assert pytest.raises(Exception, scheduler.schedule_graph, 'invalid')

    def test_notify(self):
        """Tests the functionality of notify()."""
        # Create big schedule.
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_big_schedule()
        scheduler = schedule_wrapper.scheduler

        # Notify scheduler with nodes.
        scheduler.notify([schedule_wrapper.schedule_input_node, schedule_wrapper.schedule_output_node])

        # Asserts two nodes are added to the queue.
        assert scheduler.queue_size == 2

    def test_push(self):
        """Tests the functionality of push()."""
        # Creates a small schedule.
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_empty_schedule()
        scheduler = schedule_wrapper.scheduler

        # Push node to the scheduler.
        scheduler.push(schedule_wrapper.schedule_input_node)

        # Node is on the scheduler queue.
        assert scheduler.queue_size == 1

    def test_push_removes_duplicates(self):
        """Tests whether duplicates are not pushed to the queue."""
        # Create schedule.
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_empty_schedule()
        scheduler = schedule_wrapper.scheduler

        # Push same node twice to scheduler.
        scheduler.push(schedule_wrapper.schedule_input_node)
        scheduler.push(schedule_wrapper.schedule_input_node)

        # Duplicate is not inside the queue and set.
        assert scheduler.queue_size == 1

    def test_global_schedule_graph(self):
        """Test the functionality of globals that can be used by all nodes in a readonly manner."""
        # Create scheduler.
        schedule_wrapper = ScheduleWrapper()
        schedule_wrapper.prepare_global_schedule()
        scheduler = schedule_wrapper.scheduler

        global_readonly = schedule_wrapper.global_readonly
        global_readonly['global_var'] = 'global'

        scheduler.schedule_graph([], global_readonly)

        assert schedule_wrapper.schedule_output_node.component.out == 'global,start'


if __name__ == '__main__':
    pytest.main(TestScheduler)
