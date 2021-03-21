from detection.dectection_obj import DetectionObj


class TrackingObj:
    def __init__(self, detection_obj: DetectionObj, tracking_feature_maps):
        self.frame = detection_obj.frame
        self.frame_nr = detection_obj.frame_nr
        self.tracking_feature_maps = tracking_feature_maps
        self.bounding_boxes = detection_obj.bounding_box
        self.tracked_boxes = []
