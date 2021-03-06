"""Defines a scheduler plan for the entire pipeline stage to run.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.node.schedule_node import ScheduleNode

from processor.scheduling.component.func_call_component import FuncCallComponent

# Keys of inputs necessary to initialize the plan.
plan_inputs = {
    'detector': None,
    'tracker': None,
    're_identifier': None,
    'func': None,
    'frame_buffer': None
}

# Keys of globals used by the plan, necessary each iteration.
plan_globals = {
    'frame_obj': None,
    're_id_data': None
}


def create_plan(plan_args):
    """Create a plan using the configuration for the entire pipeline.

    Args:
        plan_args (dict[str, obj]): Dictionary containing every argument based on the name.

    Returns:
        ScheduleNode: the starting node of the plan.
    """
    # Final node executing a function that takes all previous component outputs as input.
    func_node = ScheduleNode(
        4,
        [],
        FuncCallComponent(plan_args['func']),
        {
            'frame_obj': 0
        }
    )

    # Frame buffer node storing frame with all information gathered from re-id stage.
    frame_buffer_node = ScheduleNode(
        2,
        [],
        plan_args['frame_buffer'],
        {
            'frame_obj': 0
        }
    )

    # Node that executes re-identification.
    re_id_node = ScheduleNode(
        3,
        [(frame_buffer_node, 1), (func_node, 3)],
        plan_args['re_identifier'],
        {
            'frame_obj': 0,
            're_id_data': 2
        }
    )

    # Node that executes tracking.
    tracker_node = ScheduleNode(
        3,
        [(func_node, 2), (re_id_node, 1)],
        plan_args['tracker'],
        {
            'frame_obj': 0,
            're_id_data': 2
        }
    )

    # Node that executes detection.
    detection_node = ScheduleNode(
        1,
        [(tracker_node, 1), (func_node, 1)],
        plan_args['detector'],
        {
            'frame_obj': 0
        }
    )

    # Detection node is the starting node of the plan.
    return detection_node
