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

from src.objects.connections import processors


def start_tracking_timeout_monitoring(timeout, event_loop):
    """Starts a thread, which monitors all objects currently being tracked and removes them after the timeout.

    Args:
        timeout (int):
            The time in seconds after which a tracking object should no longer be tracked.
        event_loop (AbstractEventLoop):
            The event loop that should be used inside the thread.
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

    # Check if all objects are not yet expired.
    for tracking_object in objects.values():
        if tracking_object[1] < timeout_border:
            for processor in processors.values():
                processor.send_message(json.dumps({
                    'type': 'stop',
                    'objectId': tracking_object[0].identifier
                }))
            delete_list.append(tracking_object[0])

    for tracking_object in delete_list:
        tracking_object.remove_self()

    # Sleep so that checking only happens once every second.
    time.sleep(1)

    # Check again.
    monitor_tracking_timeout(timeout)


objects = dict()
"""Dictionary, which matches an object identifier to.

type: Dict[str, (TrackingObject, Optional[int])]
"""

objectHistory = list()
"""List containing the ids of objects that have been tracked.

type: List[int]
"""
