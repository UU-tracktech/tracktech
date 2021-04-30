"""Contains frame buffer class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from collections import deque
from typing import List
from math import floor


class FrameBuffer:
    """Class that handles frame buffering logic and holds the buffer

    """

    def __init__(self):
        """Set buffer size and initialize deque

        """
        self.__buffer_size = 50
        self.__buffer = deque()

    def clean_up(self):
        """Removes buffer items over the maximum size

        TODO: add functionality to work with timestamp instead of buffer size
        """
        while len(self.__buffer) >= self.__buffer_size:
            self.__buffer.pop()

    def add(self, track_obj):
        """Add a tracking object to the buffer

        Args:
            track_obj (dict): Tracking object in python dict format

        """
        self.__buffer.appendleft(track_obj)

    def search(self, bbox_id):
        """Searches in the buffer for the last frame that the bounding box with given id occurred, then returns
        the list of frames since then AND the bounding box of the given box id.

        Args:
            bbox_id (integer): id of the tracked object we want to look for

        Returns:
            [integer], [numpy.ndarray]: unpacked tuple of last spotted boundingbox rectangle of that id, and list
            of frames since last appearance, including that of given bounding_box

        """

        stack = []
        rect = []

        for track_obj in self.__buffer:
            index = self.binary_search(track_obj["boxes"], "boxId", bbox_id)
            stack.append(track_obj["frame"])
            if index is not None:
                rect = track_obj["boxes"][index]["rect"]
                break

        return rect, stack

    def binary_search(self, search_list: List, key: str, value):
        """Searches a *SORTED* list for a certain value occurrence in O(lg n)

        Returns:
            integer: the index of the searched for value

        """
        left = 0
        right = len(search_list) - 1
        while left <= right:
            middle = floor((left + right) / 2)
            if search_list[middle][key] < value:
                left = middle + 1
            elif search_list[middle][key] > value:
                right = middle - 1
            else:
                return middle
        return None

    @property
    def buffer(self):
        """Property for the buffer, used for testing

        """
        return self.__buffer
