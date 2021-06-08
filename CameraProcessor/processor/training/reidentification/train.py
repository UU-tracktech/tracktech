"""File that runs training using a custom dataset.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import torchreid

from processor.utils.config_parser import ConfigParser


if __name__ == '__main__':
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
