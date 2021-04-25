"""Contains frame buffer class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from collections import deque


class FrameBuffer:
    """Class that handles frame buffering logic and holds the buffer

    """

    def __init__(self):
        """

        """
        self.buffer_size = 50
        self.buffer = deque()

    def clean_up(self) -> None:
        """Removes buffer items over the maximum size

        TODO: add functionality to work with timestamp instead of buffer size
        """
        while len(self.buffer) >= self.buffer_size:
            self.buffer.pop()

    def add(self, track_obj: dict) -> None:
        """Add a tracking object to the buffer

        Args:
            track_obj: Tracking object in python dict format

        """
        self.buffer.appendleft(track_obj)

    def search(self, timestamp, bbox_id):
        """Searches in the buffer for the frame with given timestamp and bounding box id, then returns
        a boundingbox of the object and list of frames since the last appearance of that box

        Args:
            timestamp: timestamp of the frame we're looking in
            bbox_id: id of the tracked object we want to look for

        Returns: unpacked tuple of last spotted boundingbox of that id, and list of frames since last appearance,
        including that of given bounding_box:
            bounding_box, [frames]

        """

        stack = []
        rect = []
        iterator = len(self.buffer)

        # Find the first occurrence of the searched for timestamp, with corresponding bounding box
        # Iterates from first to last added item, aka from earliest timestamp to most recent
        for track_obj in reversed(self.buffer):
            # Iterate in reverse so we can continue from that index during the next loop
            iterator -= 1

            # If we found the corresponding timestamp, save the frame
            if track_obj["frameId"] == timestamp:
                stack = [track_obj["frame"]]

                # Look for the bounding box id and save bounding box itself
                for box in track_obj["boxes"]:
                    if box["boxId"] == bbox_id:
                        rect = box["rect"]
                        # Break the loop
                        break
                # Break the outer loop
                break

        # Create reversed iterator over buffer
        for track_obj_id in reversed(range(0, iterator)):
            track_obj = self.buffer[track_obj_id]

            # Does a slow as balls O(n) search over the entire list to see if the searched for tracked object occurs
            # TODO: Maybe change the collection type of bounding boxes so we can search in O(1)
            for box in track_obj["boxes"]:
                if box["boxId"] == bbox_id:
                    rect = box["rect"]
                    # Clear stack list since we found a more recent appearance of the tracked object
                    stack = []
                    break

            # Append the frame to the stack list
            stack.append(track_obj["frame"])

        return rect, stack
