"""An example wrapper file for scheduling

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from processor.scheduling.scheduler import Scheduler
from processor.scheduling.node.schedule_node import ScheduleNode

from tests.unittests.scheduling.utils.input_component import InputComponent
from tests.unittests.scheduling.utils.multiple_input_component import MultipleInputComponent
from tests.unittests.scheduling.utils.single_output_component import SingleOutputComponent
from tests.unittests.scheduling.utils.output_component import OutputComponent


# pylint: disable=unused-argument
def func(_):
    pass


class ScheduleWrapper:
    def __init__(self):
        self.scheduler = None
        self.schedule_output_node = None
        self.schedule_input_node = None

    def prepare_empty_schedule(self):
        """Prepares a very small schedule

        """
        self.schedule_output_node = self.schedule_input_node = ScheduleNode(1, [], OutputComponent(func))
        self.scheduler = Scheduler(self.schedule_output_node)

    def prepare_big_schedule(self):
        """Prepares a full schedule

        """
        # Last node/layer.
        self.schedule_output_node = ScheduleNode(1, [], OutputComponent(func))

        # Merges layers back together
        layer3_single_output_node = ScheduleNode(1, [(self.schedule_output_node, 0)], SingleOutputComponent())

        # Intermediary layer.
        layer2_multiple_input_node = ScheduleNode(2, [(layer3_single_output_node, 0)], MultipleInputComponent())

        # Intermediary layer.
        layer1_node1 = ScheduleNode(1, [(layer2_multiple_input_node, 0)], InputComponent())
        layer1_node2 = ScheduleNode(1, [(layer2_multiple_input_node, 1)], InputComponent())

        # First node/layer.
        # Node outputs to multiple nodes.
        self.schedule_input_node = ScheduleNode(1, [(layer1_node1, 0), (layer1_node2, 0)], InputComponent())
        self.scheduler = Scheduler(self.schedule_input_node)
