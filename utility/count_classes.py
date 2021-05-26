"""This file contains functionality to detect files that contain more than one class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import pathlib
import re

paths_to_ignore = ['.git', 'CameraProcessor/processor/pipeline/detection/yolov5',
                   'CameraProcessor/processor/pipeline/detection/yolov4deepsort', '/app/.git',
                   '/app/processor/pipeline/detection/yolov5', '/app/processor/pipeline/detection/yolov4deepsort',
                   'venv', 'CameraProcessor/processor/pipeline/tracking/sort/']


def get_files_too_many_classes():
    """Print the absolute paths of files with too many classes to the console."""
    skip = False
    for path in pathlib.Path(os.path.join(os.getcwd()), '..').rglob('*.py'):
        amount_of_classes = 0
        for ignore_path in paths_to_ignore:
            if ignore_path in str(path.absolute()).replace('\\\\', '/').replace('\\', '/'):
                skip = True
        if skip:
            skip = False
            continue
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                x = re.findall('^class.+:', line)
                amount_of_classes += len(x)
        if amount_of_classes >= 2:
            print('Files with too many classes: ' + str(path.absolute()))


if __name__ == '__main__':
    get_files_too_many_classes()
