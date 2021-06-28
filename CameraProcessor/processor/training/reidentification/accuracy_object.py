"""File containing the accuracy class for re-id.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import sys
import time

import gdown
import torch
import torch.nn as nn
import torchreid

from processor.utils.config_parser import ConfigParser
from processor.pipeline.reidentification.torchreid.scripts.default_config import get_default_config, optimizer_kwargs, \
    engine_run_kwargs, lr_scheduler_kwargs, imagedata_kwargs, videodata_kwargs
from processor.pipeline.reidentification.torchreid.torchreid.utils import set_random_seed, Logger, collect_env_info, \
    load_pretrained_weights, compute_model_complexity, check_isfile, resume_from_checkpoint


class AccuracyObject:
    """Re-id accuracy class for torchreid."""

    def __init__(self, config_parser_func):
        """Initializes the configurations.

        Args:
            config_parser_func (ConfigParser): Config parser to use.
        """
        configs = config_parser_func.configs["TorchReid"]
        # The path where the model weight file should be located.
        self.weights_path = os.path.join(configs['weights_dir_path'], configs['model_name'] + '.pth')
        check_weights(configs, self.weights_path, 'osnet_x1_0')

        cfg = get_default_config()
        self.adjust_cfg(cfg)
        cfg.use_gpu = torch.cuda.is_available()
        set_random_seed(cfg.train.seed)
        check_cfg(cfg)
        self.cfg = cfg

    def adjust_cfg(self, cfg):
        """Makes adjustments to the config for evaluating.

        Args:
            cfg (CfgNode): Config.
        """
        # Dataset configs.
        cfg.data.type = 'image'
        cfg.data.sources = ['market1501']
        cfg.data.targets = ['market1501']
        cfg.data.root = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'data/annotated')
        cfg.data.split_id = 0  # split index.

        # Evaluation configs.
        cfg.test.dist_metric = 'euclidean'  # distance metric, ['euclidean', 'cosine'].
        cfg.test.ranks = [1, 5, 10, 20]  # cmc ranks
        cfg.test.evaluate = True

        # Model configs.
        cfg.model.name = 'osnet_x1_0'
        cfg.model.load_weights = self.weights_path

    def run_eval(self):
        """Runs the evaluation of torchreid on Market1501."""
        log_name = 'evaluation.log'
        log_name += time.strftime('-%Y-%m-%d-%H-%M-%S')
        sys.stdout = Logger(os.path.join(self.cfg.data.save_dir, log_name))

        print('Show configuration\n{}\n'.format(self.cfg))
        print('Collecting env info ...')
        print('** System info **\n{}\n'.format(collect_env_info()))

        if self.cfg.use_gpu:
            torch.backends.cudnn.benchmark = True

        datamanager = build_datamanager(self.cfg)

        print('Building model: {}'.format(self.cfg.model.name))
        model = torchreid.models.build_model(
            name=self.cfg.model.name,
            num_classes=datamanager.num_train_pids,
            loss=self.cfg.loss.name,
            pretrained=self.cfg.model.pretrained,
            use_gpu=self.cfg.use_gpu
        )
        num_params, flops = compute_model_complexity(
            model, (1, 3, self.cfg.data.height, self.cfg.data.width)
        )
        print('Model complexity: params={:,} flops={:,}'.format(num_params, flops))

        if self.cfg.model.load_weights and check_isfile(self.cfg.model.load_weights):
            load_pretrained_weights(model, self.cfg.model.load_weights)

        if self.cfg.use_gpu:
            model = nn.DataParallel(model).cuda()

        optimizer = torchreid.optim.build_optimizer(model, **optimizer_kwargs(self.cfg))
        scheduler = torchreid.optim.build_lr_scheduler(
            optimizer, **lr_scheduler_kwargs(self.cfg)
        )

        if self.cfg.model.resume and check_isfile(self.cfg.model.resume):
            self.cfg.train.start_epoch = resume_from_checkpoint(
                self.cfg.model.resume, model, optimizer=optimizer, scheduler=scheduler
            )

        print(
            'Building {}-engine for {}-reid'.format(self.cfg.loss.name, self.cfg.data.type)
        )
        engine = build_engine(self.cfg, datamanager, model, optimizer, scheduler)
        engine.run(**engine_run_kwargs(self.cfg))


def check_weights(config_file, weights_path_str, weights_name):
    """Checks if the weight files are downloaded.

    Args:
        config_file (dict): Config to use.
        weights_path_str (str): Path to weights file .
        weights_name (str): Mame of weights file.
    """
    # Download the weights if it's not in the directory.
    if not os.path.exists(config_file['weights_dir_path']):
        os.mkdir(config_file['weights_dir_path'])

    if not os.path.exists(weights_path_str):
        if weights_name == 'osnet_x1_0':
            url = 'https://drive.google.com/u/0/uc?id=1vduhq5DpN2q1g4fYEZfPI17MJeh9qyrA&export=download'
        elif weights_name == 'market_sbs_R101-ibn':
            url = 'https://github.com/JDAI-CV/fast-reid/releases/download/v0.1.1/market_sbs_R101-ibn.pth'
        else:
            raise ValueError("Wrong weights name for reid accuracy.")
        gdown.download(url, weights_path_str, quiet=False)


def check_cfg(cfg):
    """Checks the cfg for some sort of error.

    Args:
        cfg (CfgNode): Config.
    """
    if cfg.loss.name == 'triplet' and cfg.loss.triplet.weight_x == 0:
        assert cfg.train.fixbase_epoch == 0, \
            'The output of classifier is not included in the computational graph'


def build_datamanager(cfg):
    """Builds a data manager, which in this case is always an image data manager anyway.

    Args:
        cfg (CfgNode): Config.

    Returns:
        kwargs (kwargs): Keyword arguments.
    """
    if cfg.data.type == 'image':
        return torchreid.data.ImageDataManager(**imagedata_kwargs(cfg))
    return torchreid.data.VideoDataManager(**videodata_kwargs(cfg))


def build_engine(cfg, datamanager, model, optimizer, scheduler):
    """Builds the engine for accuracy.

    Args:
        cfg (CfgNode): Config.
        datamanager (torch.DataManager): Datamanager to use.
        model (torch.model): Model.
        optimizer (torch.optimizer): Optimizer.
        scheduler (torch._LRScheduler): Scheduler.

    Returns:
        Engine (torch.Engine): Engine.
    """
    if cfg.data.type == 'image':
        if cfg.loss.name == 'softmax':
            engine = torchreid.engine.ImageSoftmaxEngine(
                datamanager,
                model,
                optimizer=optimizer,
                scheduler=scheduler,
                use_gpu=cfg.use_gpu,
                label_smooth=cfg.loss.softmax.label_smooth
            )

        else:
            engine = torchreid.engine.ImageTripletEngine(
                datamanager,
                model,
                optimizer=optimizer,
                margin=cfg.loss.triplet.margin,
                weight_t=cfg.loss.triplet.weight_t,
                weight_x=cfg.loss.triplet.weight_x,
                scheduler=scheduler,
                use_gpu=cfg.use_gpu,
                label_smooth=cfg.loss.softmax.label_smooth
            )

    else:
        if cfg.loss.name == 'softmax':
            engine = torchreid.engine.VideoSoftmaxEngine(
                datamanager,
                model,
                optimizer=optimizer,
                scheduler=scheduler,
                use_gpu=cfg.use_gpu,
                label_smooth=cfg.loss.softmax.label_smooth,
                pooling_method=cfg.video.pooling_method
            )

        else:
            engine = torchreid.engine.VideoTripletEngine(
                datamanager,
                model,
                optimizer=optimizer,
                margin=cfg.loss.triplet.margin,
                weight_t=cfg.loss.triplet.weight_t,
                weight_x=cfg.loss.triplet.weight_x,
                scheduler=scheduler,
                use_gpu=cfg.use_gpu,
                label_smooth=cfg.loss.softmax.label_smooth
            )

    return engine


if __name__ == '__main__':
    config_parser = ConfigParser('configs.ini', True)
    if config_parser.configs["Accuracy"]["reid"] == 'torchreid':
        accuracy_object = AccuracyObject(config_parser)
        accuracy_object.run_eval()
    elif config_parser.configs["Accuracy"]["reid"] == 'fastreid':
        # Grab the weight path from config.
        raise NotImplementedError("Due to filepath issues, fastreid evaluation can not be run via accuraccy object. "
                                  "Please run evaluation from the command line as specified in the README.")
    else:
        raise ValueError("Incorrect re-id algorithm specified in Accuracy config.")
