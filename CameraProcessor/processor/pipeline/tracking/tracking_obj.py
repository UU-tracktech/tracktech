"""Contains tracking object class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from processor.pipeline.detection.detection_obj import DetectionObj


class TrackingObj:
    """ Defines the properties of a tracking object (frame with bounding boxes)

    """
    def __init__(self, detection_obj: DetectionObj, tracking_feature_maps):
        self.timestamp = detection_obj.timestamp
        self.frame = detection_obj.frame
        self.frame_nr = detection_obj.frame_nr
        self.tracking_feature_maps = tracking_feature_maps
        self.bounding_boxes = detection_obj.bounding_boxes
        self.tracked_boxes = []
