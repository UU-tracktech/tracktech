"""File that runs training using a custom dataset.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os

import torchreid

from tests.conftest import root_path
from processor.utils.config_parser import ConfigParser

if __name__ == '__main__':
    # Instantiate the training mode.
    config_parser = ConfigParser('configs.ini', True)
    config = config_parser.configs['Training']
    mode = config['mode_reid']
    file = config['file']
    if mode == "torch":
        # Run the training of TorchReid.
        # Instantiate the training.
        config_parser = ConfigParser('configs.ini', True)
        config = config_parser.configs['Training_Torchreid']

        # Sets data location an properties.
        datamanager = torchreid.data.ImageDataManager(
            root=config['root'],
            sources=config['sources'],
            targets=config['targets'],
            height=int(config['height']),
            width=int(config['width']),
            batch_size_train=int(config['batch_size_train']),
            batch_size_test=int(config['batch_size_test']),
            transforms=['random_flip', 'random_crop']
        )

        # Selects the model.
        model = torchreid.models.build_model(
            name=config['model'],
            num_classes=datamanager.num_train_pids,
            loss='softmax',
            pretrained=True
        )

        # Uses CUDA.
        model = model.cuda()

        # Selects the optimizer to use.
        optimizer = torchreid.optim.build_optimizer(
            model,
            optim='adam',
            lr=0.0003
        )

        # Selects the scheduler to use.
        scheduler = torchreid.optim.build_lr_scheduler(
            optimizer,
            lr_scheduler='single_step',
            stepsize=20
        )

        # Selects the engine to use.
        engine = torchreid.engine.ImageSoftmaxEngine(
            datamanager,
            model,
            optimizer=optimizer,
            scheduler=scheduler,
            label_smooth=True
        )

        # Runs the training.
        engine.run(
            save_dir=config['save_dir'],
            max_epoch=int(config['max_epoch']),
            eval_freq=int(config['eval_freq']),
            print_freq=int(config['print_freq']),
            test_only=False
        )
    if mode == "fast":
        # Run the training of FastReid.
        # Instantiate the training.
        config_parser = ConfigParser('configs.ini', True)
        config = config_parser.configs['Training_Fastreid']
        path = os.path.join(root_path, 'processor', 'pipeline', 'reidentification', 'fastreid')
        file = '/train_net.py'
        num_gpus = config['num_gpus']
        config_file = config['config_file']
        model_device = config['model_device']
        device_number = config['device_number']
        # Start training.
        os.chdir(path)
        if model_device == 'cpu':
            os.system(f'python "{path}/tools/train_net.py" --config-file "{path}{config_file}" '
                      f'MODEL.DEVICE {model_device}')
        else:
            os.system(f'python "{path}/tools/train_net.py" --config-file "{path}{config_file}" '
                      f'MODEL.DEVICE {model_device}:{device_number}')
