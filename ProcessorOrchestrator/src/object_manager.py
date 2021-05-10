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
        identifier: An int that serves as the unique identifier to this object.
        feature_map: A json which contains the features of this object, should be sent to all processors.
    """

    def __init__(self):
        """Appends self to objects dictionary upon creation."""

        self.identifier = max(objects.keys(), default=0) + 1
        self.feature_map = {}
        objects[self.identifier] = (self, datetime.now())

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


def start_tracking_timeout_monitoring(timeout, event_loop):
    """Starts a thread which monitors all objects currently being tracked and
    makes sure they are no longer tracked after a given timeout

    Args:
        timeout (int):
            The time in seconds after which a tracking object should no longer be tracked
        event_loop (AbstractEventLoop):
            The event loop that should be used inside the thread
    """
    thread = threading.Thread(target=set_event_loop_and_start_tracking_monitoring_timout, args=(timeout,event_loop,))
    thread.start()


def set_event_loop_and_start_tracking_monitoring_timout(timeout, event_loop):
    """Sets the event loop in this thread and starts the timeout monitoring loop

    Args:
        timeout (int):
            The time in seconds after which a tracking object should no longer be tracked
        event_loop (AbstractEventLoop):
            The event loop that should be used inside the thread

    """
    asyncio.set_event_loop(event_loop)
    monitor_tracking_timeout(timeout)


def monitor_tracking_timeout(timeout):
    """ Checks all objects and deletes those that have and expired lifetime

    Args:
        timeout (int):
            The time in seconds after which a tracking object should no longer be tracked
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
