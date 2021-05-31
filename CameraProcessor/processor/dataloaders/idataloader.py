"""Dataloader super class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from PIL import Image


class IDataloader:
    """Dataloader superclass. A dataloader formats annotated data into generic BoundingBox objects."""

    def __init__(self, configs, path_location):
        """Initialize dataloader.

        Args:
            configs (dict): A dictionary of the configs.
            path_location (str): String to select gt or det from the accuracy config.
        """
        accuracy_config = configs['Accuracy']
        self.file_path = accuracy_config[path_location]
        self.image_path = accuracy_config['image_path']
        self.categories = accuracy_config['categories']
        self.filter_config = configs['Filter']
        self.image_dimensions = {}
        nr_frames = int(accuracy_config['nr_frames'])
        # Cannot contain negative amount of frames.
        if nr_frames < 0:
            raise AttributeError('Cannot have negative number of frames')
        self.nr_frames = nr_frames

    def get_image_dimensions(self, image_id, this_image_path):
        """Gets the size of an image based on its name.

        Args:
            image_id (integer): String with the name of the image.
            this_image_path (string): Path to image file.

        Returns:
            image.size (shape): width and height dimensions of the image.
        """
        if image_id in self.image_dimensions:
            return self.image_dimensions[image_id]
        image = Image.open(this_image_path)
        self.image_dimensions[image_id] = image.size
        return image.size

    def parse_file(self):
        """Parses a file into a BoundingBoxes object.

        Raises:
            NotImplementedError.
        """
        raise NotImplementedError('parse file method not implemented')
