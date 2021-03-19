import json
import os
from detection.bounding_box import BoundingBox


class Annotations:
    def __init__(self, path, nr_frames):
        self.dir_path = path
        self.nr_frames = nr_frames
        self.boxes = [[] for _ in range(nr_frames)]
        self.parse_file()

    def parse_file(self):
        lines = []
        file_path = os.path.join(self.dir_path, "gt.txt")
        with open(file_path) as file:
            lines = [line.rstrip('\n') for line in file]

        for line in lines:
            int_list = [int(i) for i in line.split()]
            (frame_nr, person_id, x, y, w, h, _, _, _, _, _) = int_list
            rectangle = (x, y, x+w, y+h)
            box = BoundingBox(person_id, rectangle, "UFO", 1)
            self.boxes[frame_nr - 1].append(box)

    def parse_json(self):
        json_path = os.path.join(self.dir_path, "path_annots.json")
        with open(json_path) as json_file:
            data = [x for x in json.load(json_file)]
            for json_obj in data:
                first_frame = list(json_obj['boxes'])[0]
                x0, y0, x1, y1 = json_obj['boxes'][first_frame]
                half_width = int((x1 - x0) / 2)
                half_height = int((y1 - y0) / 2)
                for frame_nr in json_obj['path']:
                    (x, y) = json_obj['path'][frame_nr]
                    rectangle = (x - half_width, y - half_height, x + half_width, y + half_height)
                    box = BoundingBox(1, rectangle, "UFO", 1)
                    self.boxes[int(frame_nr) - 1].append(box)
