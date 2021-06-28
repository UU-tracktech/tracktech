"""File containing a runner to test the accuracy of a tracker provided the tracks are written in the MOT format.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os
from processor.utils.config_parser import ConfigParser
from processor.training.tracking.trackeval_master.scripts.run_mot_challenge import main as mot_challenge


def main(configs):
    """Method for running the tracking accuracy.

    Args:
        configs (ConfigParser): containing the configs of the program.
    """
    folder_prefix = "../../../"
    runner_section = configs['Runner']
    det_folder = os.path.realpath(os.path.join(folder_prefix, runner_section['runs_path'], runner_section['data_set']))
    gt_folder = os.path.realpath(os.path.join(folder_prefix,
                                              runner_section['data_path'],
                                              runner_section['data_set'],
                                              'train'))
    benchmark = configs['Tracking_Accuracy']['benchmark']
    metric = 'CLEAR'
    parallel = 'False'
    config = {"METRICS": metric,
              "USE_PARALLEL": parallel,
              "BENCHMARK": benchmark,
              "GT_FOLDER": gt_folder,
              "TRACKERS_FOLDER": det_folder,
              'SKIP_SPLIT_FOL': 'True'}
    mot_challenge(config)


if __name__ == '__main__':
    config_parser = ConfigParser('configs.ini', True)
    main(config_parser.configs)
