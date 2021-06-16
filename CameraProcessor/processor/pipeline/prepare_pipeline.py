"""Prepares the objects for the pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import logging

from processor.input.cam_capture import CamCapture
from processor.input.hls_capture import HlsCapture
from processor.input.image_capture import ImageCapture
from processor.input.video_capture import VideoCapture

from processor.utils.create_runners import \
    create_detector, create_tracker, create_reidentifier, DETECTOR_SWITCH, TRACKER_SWITCH, REID_SWITCH

import processor.scheduling.plan.pipeline_plan as pipeline_plan
from processor.scheduling.scheduler import Scheduler


def prepare_objects(configs):
    """Read the configuration information and prepare the objects for the frame stream.

    Args:
        configs (configparser.Configparser): Configuration of the application when preparing the stream.

    Returns:
        ICapture, IDetector, ITracker, IReIdentifier, str: Capture instance, a detector and tracker and a websocket_id.
    """
    # Instantiate the detector, tracker and re-identification.
    detector = prepare_detector(configs)
    tracker = prepare_tracker(configs)
    re_identifier = prepare_reidentifier(configs)

    # Capture and websocket url.
    capture = prepare_capture(configs['Input'])
    websocket_url = configs['Orchestrator']['url']

    return capture, detector, tracker, re_identifier, websocket_url


def prepare_detector(configs):
    """Creates a detection instance specified inside the configs.

    Args:
        configs (configparser.ConfigParser): Configurations containing information about the detection.

    Returns:
        IDetector: Implementation of the detection interface.

    Raises:
        NameError: Whenever the name of the detection is not known.
    """
    # Instantiate the detector.
    logging.info("Instantiating detector...")
    if configs['Main'].get('detector').lower() not in DETECTOR_SWITCH:
        raise NameError(f"Incorrect detector. Detector {configs['Main'].get('detector')} not found.")

    # Detector exists, so it is created.
    return create_detector(configs['Main'].get('detector'),
                           configs
                           )


def prepare_tracker(configs):
    """Creates a tracker instance specified inside the configs.

    Args:
        configs (configparser.ConfigParser): Configurations containing information about the tracker.

    Returns:
        ITracker: Implementation of the tracker interface.

    Raises:
        NameError: When an incorrect tracker is specified
    """
    # Instantiate the tracker.
    logging.info("Instantiating tracker...")
    if configs['Main'].get('tracker').lower() not in TRACKER_SWITCH:
        raise NameError(f"Incorrect tracker. Tracker {configs['Main'].get('tracker')} not found.")

    # Create the tracker, since it exists.
    return create_tracker(configs['Main'].get('tracker'),
                          configs
                          )


def prepare_reidentifier(configs):
    """Creates a re-id instance specified inside the configs.

    Args:
        configs (configparser.ConfigParser): Configurations containing information about the re-id.

    Returns:
        IReIdentifier: Implementation of the re-identification interface.
    """
    # Instantiate the re-identifier.
    logging.info("Instantiating reidentifier...")
    if configs['Main'].get('reid').lower() not in REID_SWITCH:
        raise NameError(f"Incorrect re-identifier. Re-identifier {configs['Main'].get('reid')} not found.")

    # Create re-identifier since it exists.
    return create_reidentifier(configs['Main'].get('reid'),
                               configs
                               )


def prepare_capture(input_config):
    """Prepares the capture of the stream.

    Args:
        input_config (SectionProxy): Configurations of the capture.

    Returns:
        ICapture: Capture implementation.

    Raises:
        NameError: The input type is unknown.
    """
    capture_type = input_config['type'].lower()

    # Switch statement creating the capture.
    if capture_type == 'webcam':
        return CamCapture(int(input_config['webcam_device_nr']))
    if capture_type == 'images':
        return ImageCapture(input_config['images_dir_path'])
    if capture_type == 'video':
        return VideoCapture(input_config['video_file_path'])
    if capture_type == 'hls':
        return HlsCapture(input_config['hls_url'])

    # No cv2.VideoCapture returned.
    raise NameError(f'Input type "{capture_type}" is unknown')


def prepare_scheduler(detector, tracker, re_identifier, on_processed_frame, frame_buffer):
    """Prepare the Scheduler with a valid plan configuration.

    Args:
        detector (IDetector): detector performing the detections on a given frame.
        tracker (ITracker): tracker performing simple tracking of all objects using the detections.
        re_identifier (IReIdentifier): re-identifier performing the re-identification stage.
        on_processed_frame (Function): when the frame got processed. Call this function to handle effects.
        frame_buffer (FrameBuffer): buffer of frames and stage information associated with the frame.

    Returns:
        Scheduler: Scheduler that has been configured with a plan.
    """
    # Get args dict from the used plan.
    plan_args = pipeline_plan.plan_inputs

    # Put configuration into args dict.
    plan_args['detector'] = detector
    plan_args['tracker'] = tracker
    plan_args['re_identifier'] = re_identifier
    plan_args['func'] = on_processed_frame
    plan_args['frame_buffer'] = frame_buffer

    # Apply configuration to plan.
    start_node = pipeline_plan.create_plan(plan_args)

    # Return Scheduler.
    return Scheduler(start_node)
