import os
import re
import pytest
from training.pre_annotations import PreAnnotations

example_txt_file = os.path.join(__file__, '../example_pre_annotations.txt')
example_json_file = os.path.join(__file__, '../example_pre_annotations.json')


@pytest.mark.parametrize('nr_frames', [-2, -1, 0, 1, 5])
def test_constructor(nr_frames):
    if nr_frames < 0:
        assert pytest.raises(AttributeError, PreAnnotations, example_txt_file, nr_frames)
        return
    annotations = PreAnnotations(example_txt_file, nr_frames)
    assert annotations.nr_frames == nr_frames
    assert annotations.file_path == example_txt_file
    assert len(annotations.boxes) == nr_frames


def test_text_file_exists():
    assert os.path.exists(example_txt_file)


def test_json_file_exists():
    assert os.path.exists(example_json_file)


def test_text_file_parsing():
    pass
    # parse_text_file


def test_line_parsing():
    pass

# class PreAnnotations:
#     def __init__(self, file_path, nr_frames):
#         self.file_path = file_path
#         if nr_frames < 0:
#             raise AttributeError('Cannot have negative number of frames')
#         self.nr_frames = nr_frames
#         self.boxes = [[] for _ in range(nr_frames)]
#
#     def parse_file(self):
#         is_txt_file = re.search('^.*.txt$', self.file_path)
#         is_json_file = re.search('^.*.json$', self.file_path)
#         if is_txt_file:
#             self.parse_text_file()
#         elif is_json_file:
#             self.parse_json_file()
#         else:
#             raise AttributeError
#
#
#     def parse_text_file(self):
#         global skipped_lines
#         # Read file
#         with open(self.file_path) as file:
#             lines = [line.rstrip('\n') for line in file]
#
#         # Determine delimiter
#         delimiter = ' '
#         if lines[0].__contains__(','):
#             delimiter = ','
#
#         # Extract information from lines
#         for line in lines:
#             (frame_nr, person_id, x, y, w, h) = self.parse_line(line, delimiter)
#             if frame_nr - 1 >= self.nr_frames:
#                 skipped_lines = skipped_lines + 1
#                 continue
#
#             # Create bounding box
#             rectangle = (x, y, x + w, y + h)
#             box = BoundingBox(person_id, rectangle, "UFO", 1)
#             self.boxes[frame_nr - 1].append(box)
#
#         if skipped_lines > 0:
#             logging.info(f'Skipped lines: {skipped_lines}')
#
#
#     # Parse line from file given a delimiter
#     def parse_line(self, line, delimiter):
#         return [int(i) for i in line.split(delimiter)[:5]]
#
#
#     # Parse a JSON file to
#     def parse_json_file(self):
#         json_path = os.path.join(self.dir_path, "path_annots.json")
#         with open(json_path) as json_file:
#             # Every json object
#             data = [x for x in json.load(json_file)]
#             for json_obj in data:
#                 # Extract data from json
#                 first_frame = list(json_obj['boxes'])[0]
#                 x0, y0, x1, y1 = json_obj['boxes'][first_frame]
#                 half_width = int((x1 - x0) / 2)
#                 half_height = int((y1 - y0) / 2)
#                 # Create bounding box
#                 for frame_nr in json_obj['path']:
#                     (x, y) = json_obj['path'][frame_nr]
#                     rectangle = (x - half_width, y - half_height, x + half_width, y + half_height)
#                     box = BoundingBox(1, rectangle, "UFO", 1)
#                     self.boxes[int(frame_nr) - 1].append(box)