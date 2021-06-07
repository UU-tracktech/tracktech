"""Dataloader super class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json

from processor.dataloaders.idataloader import IDataloader


class JSONDataloader(IDataloader):
    """JSON Dataloader, formats MOT Data."""

    def get_annotations(self):
        """Reads the annotations from a file.

        Returns:
            annotations ([(str)]): Annotations tuples in a list.
        """
        # Read file.
        with open(self.file_path) as file:
            lines = [line.rstrip('\n') for line in file]
        return lines

    def get_image_dimensions(self, image_id):
        return 1, 1

    def parse_line(self, line):
        annotations = []
        json_line = json.loads(line)
        image_id = json_line['imageId']
        boxes = json_line['boxes']
        for box in boxes:
            person_id = box['boxId']
            certainty = box['certainty']
            object_type = box['objectType']
            x_left_top = box['rect'][0]
            y_left_top = box['rect'][1]
            x_right_bottom = box['rect'][2]
            y_right_bottom = box['rect'][3]
            annotations.append((image_id, person_id, x_left_top, y_left_top, x_right_bottom, y_right_bottom, certainty,
                                object_type, None))
        return annotations
