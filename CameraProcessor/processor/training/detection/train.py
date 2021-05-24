""" File that runs training using a custom dataset.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os

from tests.conftest import root_path
from processor.utils.config_parser import ConfigParser

if __name__ == '__main__':
    # Instantiate the training mode.
    config_parser = ConfigParser('configs.ini')
    config = config_parser.configs['Training']
    mode = config['mode']
    file = config['file']
    if mode == 'yolov5':
        # Run the training of Yolov5.
        config = config_parser.configs['Training_Yolov5']
        data = config['data']
        cfg = config['cfg']
        weights = config['weights']
        batch_size = config['batch-size']
        hyp = config['hyp']
        path = os.path.join(root_path, 'processor', 'pipeline', 'detection', 'yolov5')
        os.system(f'python "{path}{file}" --data "{path}{data}" --cfg "{path}{cfg}" '
                  f'--weights {weights} --hyp "{path}{hyp}" --batch-size {batch_size}')
    if mode == 'yolor':
        # Run the training of Yolor.
        config = config_parser.configs['Training_Yolor']
        data = config['data']
        cfg = config['cfg']
        img = config['img']
        device = config['device']
        name = config['name']
        weights = config['weights']
        batch_size = config['batch-size']
        hyp = config['hyp']
        epochs = config['epochs']
        path = os.path.join(root_path, 'processor', 'pipeline', 'detection', 'yolor')
        if config['multi-gpu']:
            # Single GPU training.
            os.system(f'python "{path}{file}" --data "{path}{data}" --cfg "{path}{cfg}" '
                      f'--weights {weights} --hyp "{path}{hyp}" --batch-size {batch_size} '
                      f'--img {img} --device "{device}" --name "{name}" --epochs "{epochs}"')
        if not config['multi-gpu']:
            # Multi GPU training.
            os.system(f'python -m torch.distributed.launch --nproc_per_node 2 --master_port 9527 '
                      f'"{path}{file}" --data "{path}{data}" --cfg "{path}{cfg}" '
                      f'--weights {weights} --hyp "{path}{hyp}" --batch-size {batch_size} '
                      f'--img {img} --device "{device}" --name "{name}" --epochs "{epochs}"')
