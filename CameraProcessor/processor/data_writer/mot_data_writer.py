"""Datawriter implementation for MOT.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.data_writer.i_data_writer import IDataWriter
from processor.utils.text import boxes_to_txt
import os


class MotDataWriter(IDataWriter):
    """DataWriter implementation for MOT"""
    def __init__(self, det_destination):
        """Initializing the MOT data writer"""
        super().__init__()
        self.to_write = []
        destination_file = os.path.realpath(det_destination + '.txt')
        self.file = open(destination_file, 'w')

    def write(self, bounding_boxes, shape):
        """Method for saving the data to write later.

        Args:
            bounding_boxes (BoundingBoxes): An object containing the bounding boxes that need to be written.
            shape (int, int): A tuple containing the width and height of the frames.
        """
        # Writing can only be done at the end, because MOT data needs to be sorted at the end.
        image_id = bounding_boxes.image_id
        for bounding_box in bounding_boxes:
            tracked_boxes_string = boxes_to_txt([bounding_box], shape, image_id)
            self.to_write.append((bounding_box.identifier, image_id, tracked_boxes_string))

    def close(self):
        """Method for writing the information in the object to the file and to close the file."""
        # Sorting the detections on object_id according to the MOT standards
        self.to_write.sort(key=lambda e: e[:2])
        track_write_list = [x[2] for x in self.to_write]

        # Removing trailing \n
        track_write_list[len(track_write_list) - 1] = track_write_list[len(track_write_list) - 1].rstrip("\n")

        # Writing info to the file and then closing it
        try:
            self.file.writelines(track_write_list)
            self.file.close()
        except RuntimeError as run_error:
            print(f'Cannot write to the file with following exception: {run_error}')
