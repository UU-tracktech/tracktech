"""File containing a runner to test the accuracy of a tracker provided the tracks are written in the MOT format.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.utils.config_parser import ConfigParser
import sys
import os
import argparse
from subprocess import call


def main(configs):
    """Method for running the tracking accuracy

    """
    folder_prefix = "../../../"
    accuracy_section = configs['Accuracy']
    det_folder = os.path.realpath(os.path.join(folder_prefix, accuracy_section['det_folder']))
    gt_folder = os.path.realpath(os.path.join(folder_prefix, accuracy_section['gt_folder']))
    benchmark = 'MOT20'
    metric = 'CLEAR'
    parallel = 'False'
    parser_config = {"--METRICS": metric,
                     "--USE_PARALLEL": parallel,
                     "--BENCHMARK": benchmark,
                     "--GT_FOLDER": gt_folder,
                     "--TRACKERS_FOLDER": det_folder}
    script_path = os.path.realpath('../../../processor/training/tracking/trackeval_master/scripts/run_mot_challenge.py')
    cmd = f"""python {script_path} --USE_PARALLEL {parallel} --METRICS {metric} --BENCHMARK {benchmark} --GT_FOLDER {gt_folder} --TRACKERS_FOLDER {det_folder}"""
    os.system(cmd)


if __name__ == '__main__':
    config_parser = ConfigParser('configs.ini', True)
    main(config_parser.configs)
