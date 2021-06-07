"""An example wrapper file for scheduling.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from tests.unittests.scheduling.utils.input_component import InputComponent
from tests.unittests.scheduling.utils.multiple_input_component import MultipleInputComponent
from tests.unittests.scheduling.utils.single_output_component import SingleOutputComponent
from tests.unittests.scheduling.utils.output_component import OutputComponent

from processor.scheduling.scheduler import Scheduler
from processor.scheduling.node.schedule_node import ScheduleNode


# pylint: disable=unused-argument
def func(_):
    """An empty function for testing purposes, to be passed to Output Components."""


class ScheduleWrapper:
    """A schedule wrapper for testing purposes, contains.

    Attributes:
        scheduler (Scheduler): Scheduler on which the test is run.
        schedule_input_node (ScheduleNode): First node of the schedule.
        schedule_output_node (ScheduleNode): Last node of the schedule.
    """
    def __init__(self):
        """Create the wrapper and define some helper attributes."""
        self.scheduler = None
        self.schedule_input_node = None
        self.schedule_output_node = None
        self.global_readonly = None

    def prepare_invalid_schedule(self):
        """Prepare an invalid schedule."""
        self.schedule_output_node = self.schedule_input_node = ScheduleNode(3, [(), ()], OutputComponent(func), {})
        self.scheduler = Scheduler(self.schedule_output_node)
        self.global_readonly = {}

    def prepare_empty_schedule(self):
        """Prepares a very small schedule."""
        self.schedule_output_node = self.schedule_input_node = ScheduleNode(1, [], OutputComponent(func), {})
        self.scheduler = Scheduler(self.schedule_output_node)
        self.global_readonly = {}

    def prepare_big_schedule(self):
        """Prepares a full schedule."""
        # Last node/layer.
        self.schedule_output_node = ScheduleNode(1, [], OutputComponent(func), {})

        # Merges layers back together.
        layer3_single_output_node = ScheduleNode(1, [(self.schedule_output_node, 0)], SingleOutputComponent(), {})

        # Intermediary layer.
        layer2_multiple_input_node = ScheduleNode(2, [(layer3_single_output_node, 0)], MultipleInputComponent(), {})

        # Intermediary layer.
        layer1_node1 = ScheduleNode(1, [(layer2_multiple_input_node, 0)], InputComponent(), {})
        layer1_node2 = ScheduleNode(1, [(layer2_multiple_input_node, 1)], InputComponent(), {})

        # First node/layer.
        # Node outputs to multiple nodes.
        self.schedule_input_node = ScheduleNode(1, [(layer1_node1, 0), (layer1_node2, 0)], InputComponent(), {})
        self.scheduler = Scheduler(self.schedule_input_node)
        self.global_readonly = {}

    def prepare_global_schedule(self):
        """Prepares schedule using globals functionality."""
        global_var_name = 'global_var'

        # Final node executing a function that takes all previous component outputs as input.
        self.schedule_output_node = ScheduleNode(
            1,
            [],
            OutputComponent(func),
            {}
        )

        # Node that executes detection.
        self.schedule_input_node = ScheduleNode(
            1,
            [(self.schedule_output_node, 0)],
            InputComponent(),
            {
                global_var_name: 0
            }
        )

        self.scheduler = Scheduler(self.schedule_input_node)

        self.global_readonly = {
            global_var_name: None
        }
