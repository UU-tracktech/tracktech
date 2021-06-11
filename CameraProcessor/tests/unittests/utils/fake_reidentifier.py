"""Mock re-identifier for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.pipeline.reidentification.ireidentifier import IReIdentifier
from processor.data_object.bounding_boxes import BoundingBoxes

class FakeReIdentifier(IReIdentifier):
    """A fake re-identifier that implements the same methods but just mocks some functionality."""

    def extract_features(self, frame_obj, bbox):
        """Mocks feature extraction method.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            bbox (BoundingBox): BoundingBox object that stores the bounding box from which we want to extract features.

        Returns:
            [float]: An empty vector.
        """
        return []

    def re_identify(self, frame_obj, track_obj, re_id_data):
        """Mocks re_identify function.

        Args:
            frame_obj (FrameObj):  frame object storing OpenCV frame and timestamp.
            track_obj (BoundingBoxes): List of bounding boxes from tracking stage.
                list has to be of the same length as the list of bounding boxes in the track_obj, and ordered in the
                same way (feature vector i belongs to box i).
            re_id_data (ReidData): Data class containing data about tracked subjects.

        Returns:
            BoundingBoxes: object containing all re-id tracked boxes (bounding boxes where re-id is performed).
        """
        return BoundingBoxes([])
