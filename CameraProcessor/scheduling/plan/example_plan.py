from scheduling.node.schedule_node import ScheduleNode
from scheduling.component.example_components.input_component import InputComponent
from scheduling.component.example_components.output_component import OutputComponent
from scheduling.component.example_components.example_component import ExampleComponent


# Last node/layer.
schedule_output_node = ScheduleNode(1, [], OutputComponent())

# Intermediary layer.
layer2_multiple_input_node = ScheduleNode(2, [(schedule_output_node, 0)], ExampleComponent())

# Intermediary layer.
layer1_node1 = ScheduleNode(1, [(layer2_multiple_input_node, 0)], InputComponent())
layer1_node2 = ScheduleNode(1, [(layer2_multiple_input_node, 1)], InputComponent())

# First node/layer.
# Node outputs to multiple nodes.
schedule_input_node = ScheduleNode(1, [(layer1_node1, 0), (layer1_node2, 0)], InputComponent())
