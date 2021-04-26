# python train.py --data coco.yaml --cfg yolov5s.yaml --weights '' --batch-size 64
import os
import sys
import argparse
import configparser
from absl import app
import runpy
import subprocess

import processor.pipeline.detection.train as train

curr_dir = os.path.dirname(os.path.abspath(__file__))


def main(_argv):
    train_dir = '/pipeline/detection/yolov5/'
    configs = configparser.ConfigParser(allow_no_value=True)
    configs.read('../configs.ini')
    params = configs['Training']
    data = params['data']
    cfg = params['cfg']
    weights = params['weights']
    batch_size = params['batch-size']
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pipeline', 'detection', 'yolov5', 'train.py')
    print(path)
    # subprocess.call([path, '--data', data, '--cfg', cfg, '--weights', weights, '--batch-size', batch_size])
    sys.argv = (['', '--data', data, '--cfg', cfg, '--weights', weights, '--batch-size', batch_size])
    runpy.run_path(path, run_name='__main__')


if __name__ == '__main__':
    app.run(main)