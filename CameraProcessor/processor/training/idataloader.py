from processor.utils.config_parser import ConfigParser


class IDataloader:
    def __init__(self, categories, file_path, nr_frames, image_path=''):
        self.file_path = file_path
        self.image_path = image_path
        self.categories = categories
        # Cannot contain negative amount of frames.
        if nr_frames < 0:
            raise AttributeError('Cannot have negative number of frames')
        self.nr_frames = nr_frames

        config_parser = ConfigParser('configs.ini')
        configs = config_parser.configs
        self.filter_config = configs['Filter']

    def get_image_size(self, image_id):
        """Gets the size of an image based on its name.

        Args:
            image_id: String with the name of the image.

        Returns: width, height (integers).

        """
        raise NotImplementedError('get image size method not implemented')

    def parse_file(self):
        """Parses a file into a BoundingBoxes object.

        Returns: a BoundingBoxes object.

        """
        raise NotImplementedError('parse file method not implemented')
