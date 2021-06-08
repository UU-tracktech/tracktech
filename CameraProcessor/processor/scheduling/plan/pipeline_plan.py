"""Defines a scheduler plan for the entire pipeline stage to run.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.node.schedule_node import ScheduleNode

from processor.scheduling.component.pass_component import PassComponent
from processor.scheduling.component.func_call_component import FuncCallComponent

# Arguments needed to configure.
args = {
    'detector': None,
    'tracker': None,
    'func': None
}


def create_plan(plan_args):
    """Create a plan using the configuration for the entire pipeline.

    Args:
        plan_args (dict[str, obj]): Dictionary containing every argument based on name.

    Returns:
        ScheduleNode: the starting node of the plan.
    """
    # Final node executing a function that takes all previous component outputs as input.
    func_node = ScheduleNode(
        3,
        [],
        FuncCallComponent(plan_args['func'])
    )

    # Node that executes tracking based.
    tracker_node = ScheduleNode(
        2,
        [(func_node, 2)],
        plan_args['tracker']
    )

    # Node that executes detection.
    detection_node = ScheduleNode(
        1,
        [(tracker_node, 1), (func_node, 1)],
        plan_args['detector']
    )

    # Input node that passes the input to all outputs as is.
    input_node = ScheduleNode(
        1,
        [(detection_node, 0), (tracker_node, 0), (func_node, 0)],
        PassComponent()
    )

    return input_node
