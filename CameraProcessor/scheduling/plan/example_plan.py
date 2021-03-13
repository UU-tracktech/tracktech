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

if __name__ == '__main__':
    from scheduling.scheduler import Scheduler

    scheduler = Scheduler(schedule_input_node)
    scheduler.schedule_graph("test")

    curr_node = schedule_input_node
    while len(curr_node.out_nodes) > 0:
        curr_node = curr_node.out_nodes[0][0]
    print(curr_node.component.out)
