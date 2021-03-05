import cv2


class DetectionObj:
    def __init__(self, timestamp, frame, frame_nr):
        self.timestamp = timestamp
        self.frame = frame
        self.frame_nr = frame_nr
        self.bounding_box = []

    def draw_rectangles(self):
        red = (255, 0, 0)
        for bounding_box in self.bounding_box:
            self.frame = cv2.rectangle(self.frame,
                                       tuple(bounding_box.rectangle[:2]),
                                       tuple(bounding_box.rectangle[2:]),
                                       red,
                                       2)
