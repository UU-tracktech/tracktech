import json
import re
import logging
from src.pipeline.detection.bounding_box import BoundingBox


class PreAnnotations:
    def __init__(self, file_path: str, nr_frames: int):
        """Constructor for the preAnnotations object.

        Creates list of lists, for each frame it contains a list of bounding boxes.

        Args:
            file_path (str): Path to the file containing the annotations.
            nr_frames (int): The amount of frames of which annotated data will get extracted.

        Raises:
            When number of frames is negative it raises an error.
        """
        self.file_path = file_path
        self.skipped_lines = 0
        # Cannot contain negative frames.
        if nr_frames < 0:
            raise AttributeError('Cannot have negative number of frames')
        self.nr_frames = nr_frames
        # Foreach frame create a list.
        self.boxes = [[] for _ in range(nr_frames)]
        self.skipped_lines = 0

    def parse_file(self) -> None:
        """Parses file containing annotations.

        Raises:
            Exception is raised when the file type does not have a handler.
        """
        is_txt_file = re.search('^.*.txt$', self.file_path)
        is_json_file = re.search('^.*.json$', self.file_path)
        # Switch statement
        if is_txt_file:
            self.parse_text_file()
        elif is_json_file:
            self.parse_json_file()
        else:
            raise NotImplementedError('No implementation exists for this file type')

    def parse_text_file(self) -> None:
        """Parses text file containing annotations

        Reads file line by line and puts it inside a bounding box object
        """
        # Read file
        with open(self.file_path) as file:
            lines = [line.rstrip('\n') for line in file]

        # Determine delimiter automatically
        delimiter = ' '
        if lines[0].__contains__(','):
            delimiter = ','

        # Extract information from lines
        for line in lines:
            (frame_nr, person_id, pos_x, pos_y, pos_w, pos_h) = self.parse_line(line, delimiter)
            if frame_nr - 1 >= self.nr_frames:
                self.skipped_lines = self.skipped_lines + 1
                continue

            # Create bounding box
            rectangle = [pos_x, pos_y, pos_x + pos_w, pos_y + pos_h]
            box = BoundingBox(person_id, rectangle, "UFO", 1)
            self.boxes[frame_nr - 1].append(box)

        # Logs when lines skipped
        if self.skipped_lines > 0:
            logging.info(f'Skipped lines: {self.skipped_lines}')

    @staticmethod
    def parse_line(line: str, delimiter: str) -> [int]:
        """Parse line from file given a delimiter.

        First 6 values are
        "<frameID>,<objectID>,<x1>,<y1>,<x2>,<y2>,.. jibberish"

        Args:
            line (str): line in file.
            delimiter (str): delimiter values in line are separated with.

        Returns:
            Integer values of line parsed and put inside string.
        """
        return [int(i) for i in line.split(delimiter)[:6]]

    def parse_json_file(self) -> None:
        """Parses JSON file
        """
        # Open file
        with open(self.file_path) as json_file:
            # Every json object
            data = [json.load(json_file)]
            for json_obj in data:
                self.parse_json_object(json_obj)

    def parse_json_object(self, json_object: json) -> None:
        """Extracts data from json object and puts them in class.

        JSON object (subject) has a path containing coordinates for each frame.
        Looping goes through each path and adds box for each frame.

        Args:
            json_object: A single json object.
        """
        first_frame = list(json_object[0]['boxes'])[0]
        # A rectangle
        pos_x0, pos_y0, pos_x1, pos_y1 = json_object[0]['boxes'][first_frame]
        half_width = int((pos_x1 - pos_x0) / 2)
        half_height = int((pos_y1 - pos_y0) / 2)
        # Add bounding box for each frame
        for frame_nr in json_object[0]['path']:
            # Skips frame when it does exceed list length
            if int(frame_nr) >= self.nr_frames:
                self.skipped_lines = self.skipped_lines + 1
                continue

            # Create bounding box for a frame
            (pos_x, pos_y) = json_object[0]['path'][frame_nr]
            rectangle = [pos_x - half_width, pos_y - half_height,
                         pos_x + half_width, pos_y + half_height]
            box = BoundingBox(1, rectangle, 'UFO', 1)
            # Append to list
            self.boxes[int(frame_nr) - 1].append(box)
