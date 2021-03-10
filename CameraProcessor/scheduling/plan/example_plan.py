from scheduling.node.schedule_node import ScheduleNode
from scheduling.component.example_components import ScheduleInputComponent, ScheduleOutputComponent, ExampleComponent


schedule_output_node = ScheduleNode(1, [], ScheduleOutputComponent())

layer2_multiple_input_node = ScheduleNode(2, [(schedule_output_node, 0)], ExampleComponent())

layer1_node1 = ScheduleNode(1, [(layer2_multiple_input_node, 0)], ScheduleInputComponent())

layer1_node2 = ScheduleNode(1, [(layer2_multiple_input_node, 1)], ScheduleInputComponent())

schedule_input_node = ScheduleNode(1, [(layer1_node1, 0), (layer1_node2, 0)], ScheduleInputComponent())
