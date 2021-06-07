"""Tracking object component and dict to manage objects.

This file contains a class for tracking objects. Creating an object will automatically add it to a dictionary, which
it removes itself from upon removal.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import asyncio
import json
import threading
import time
from datetime import datetime, timedelta

import src.logger as logger
from src.connections import processors


class TrackingObject:
    """Abstract representation of objects that are tracked in the processors.

    Attributes:
        identifier (int): Serves as the unique identifier to this object.
        image (string): Serialised string containing the cutout image of this object.
        feature_map (json): Contains the features of this object, should be sent to all processors.
    """

    def __init__(self, image):
        """Appends self to objects dictionary upon creation.

        Args:
            image (string):
                Serialised string containing the cutout image of this object.
        """

        self.identifier = max(objectHistory, default=0) + 1
        self.image = image
        self.feature_map = {}
        objects[self.identifier] = (self, datetime.now())
        objectHistory.append(self.identifier)

    def update_feature_map(self, feature_map):
        """Updates feature map of this object.

        Args:
            feature_map (json):
                json containing the features that should become the new feature map on this object.
        """
        self.feature_map = feature_map
        logger.log(f"updated feature map of object {self.identifier}")

    def remove_self(self):
        """Removes self from objects dict."""
        del objects[self.identifier]

    def log_spotting(self, processor_id):
        """Writes a spotting of this object to a log file.

        Args:
            processor_id (int): Identifier of the processor
        """
        file = open(f"tracking_timelines/tracking_logs_{self.identifier}.txt", "a")
        file.write(json.dumps({
            "timeStamp": datetime.now().strftime("%Y/%m/%d | %H:%M:%S"),
            "processorId": processor_id
        }))
        file.write(",\n")
        file.close()


def start_tracking_timeout_monitoring(timeout, event_loop):
    """Starts a thread which monitors all objects currently being tracked and removes them after the timeout.

    Args:
        timeout (int):
            The time in seconds after which a tracking object should no longer be tracked
        event_loop (AbstractEventLoop):
            The event loop that should be used inside the thread
    """
    thread = threading.Thread(target=set_event_loop_and_start_tracking_monitoring_timout, args=(timeout, event_loop,))
    thread.start()


def set_event_loop_and_start_tracking_monitoring_timout(timeout, event_loop):
    """Sets the event loop in this thread and starts the timeout monitoring loop.

    Args:
        timeout (int):
            The time in seconds after which a tracking object should no longer be tracked.
        event_loop (AbstractEventLoop):
            The event loop that should be used inside the thread.
    """
    asyncio.set_event_loop(event_loop)
    monitor_tracking_timeout(timeout)


def monitor_tracking_timeout(timeout):
    """Checks all objects and deletes those that have and expired lifetime.

    Args:
        timeout (int):
            The time in seconds after which a tracking object should no longer be tracked.
    """
    timeout_border = datetime.now() - timedelta(seconds=timeout)
    delete_list = list()

    for tracking_object in objects.values():
        if tracking_object[1] < timeout_border:
            for processor in processors.values():
                processor.send_message(json.dumps({
                    "type": "stop",
                    "objectId": tracking_object[0].identifier
                }))
            delete_list.append(tracking_object[0])

    for tracking_object in delete_list:
        tracking_object.remove_self()

    time.sleep(1)

    monitor_tracking_timeout(timeout)


objects = dict()
"""Dictionary which matches an object identifier to.

type: Dict[str, (TrackingObject, Optional[int])]
"""

objectHistory = list()
"""List containing the ids of objects that have been tracked.

type: List[int]
"""
