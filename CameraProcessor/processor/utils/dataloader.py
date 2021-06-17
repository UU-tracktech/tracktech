"""Class with utils functions regarding the dataloader.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.dataloaders.coco_dataloader import CocoDataloader
from processor.dataloaders.json_dataloader import JsonDataloader
from processor.dataloaders.mot_dataloader import MotDataloader


def get_dataloader(configs, annotation_format):
    """Get a dataloader based on format.

    Args:
        annotation_format (str): Dataloader format to select.
        configs (Dict): Configuration parser, which contains the information required to make a dataloader.

    Returns:
        dataloader (IDataloader): The dataloader to use for parsing annotations.

    Raises:
        ValueError: Dataloader name is unrecognised.
    """
    if annotation_format == 'COCO':
        dataloader = CocoDataloader(configs)
    elif annotation_format == 'JSON':
        dataloader = JsonDataloader(configs)
    elif annotation_format == 'MOT':
        dataloader = MotDataloader(configs)
    else:
        raise ValueError("This is not a valid dataloader")
    return dataloader
