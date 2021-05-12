""" File that runs training using a custom dataset.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os

from tests.conftest import root_path

if __name__ == '__main__':
    path = os.path.join(root_path, 'processor', 'pipeline', 'detection', 'yolov5')
    os.system(f'python "{path}/train.py" --data "{path}/data/coco128.yaml" --cfg "{path}/models/yolov5s.yaml" '
              f'--weights \'\' --hyp "{path}/data/hyp.scratch.yaml" --batch-size 4')
