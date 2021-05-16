"""String matches file names with class names.
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

This file contains functionality to detect files that contain more than one class.
"""
import os
import pathlib
import re
from absl import app

paths_to_ignore = ['.git', 'CameraProcessor/processor/pipeline/detection/yolov5',
                   'CameraProcessor/processor/pipeline/detection/yolov4deepsort', '/app/.git',
                   '/app/processor/pipeline/detection/yolov5', '/app/processor/pipeline/detection/yolov4deepsort',
                   'venv', 'CameraProcessor/processor/pipeline/tracking/sort/']


def match_filenames_classes(_):
    """Print the absolute paths of files with too many classes to the console."""
    skip = False
    for path in pathlib.Path(os.path.join(os.getcwd()), '..').rglob('*.py'):
        for ignore_path in paths_to_ignore:
            if ignore_path in str(path.absolute()).replace('\\\\', '/').replace('\\', '/'):
                skip = True
        # Checks the if the file should be skipped.
        if skip:
            skip = False
            continue
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Retrieves and parses the class names with the file names.
                x = re.findall('^class.+:', line)
                class_string = str(x)[8:].split('(')[0].split(':')[0].lower()
                file_name = str(path)[:-3].split('\\')[-1].split('/')[-1].replace('_', '')
                # Prints the files with multiple classes.
                if class_string != file_name and len(class_string) > 0:
                    print('File with non-matching class names: ' + str(path.absolute()) + '\n' + file_name +
                          ' does not string match ' + class_string)


if __name__ == '__main__':
    try:
        app.run(match_filenames_classes)
    except SystemExit:
        pass
