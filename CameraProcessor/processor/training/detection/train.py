""" File that runs training using a custom dataset.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os

from tests.conftest import root_path
from processor.utils.config_parser import ConfigParser

if __name__ == '__main__':
    config_parser = ConfigParser('configs.ini')
    config = config_parser.configs['Training']
    file = config['file']
    data = config['data']
    cfg = config['cfg']
    weights = config['weights']
    batch_size = config['batch-size']
    hyp = config['hyp']

    path = os.path.join(root_path, 'processor', 'pipeline', 'detection', 'yolov5')
    os.system(f'python "{path}{file}" --data "{path}{data}" --cfg "{path}{cfg}" '
              f'--weights {weights} --hyp "{path}{hyp}" --batch-size {batch_size}')
