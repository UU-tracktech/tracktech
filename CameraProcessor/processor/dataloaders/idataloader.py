"""Dataloader super class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle


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

    def parse_boxes(self, annotations, delimiter):
        """Parses bounding boxes.

        Args:
            annotations ([(str)]): Annotations tuples in a list.

        Returns:
            bounding_boxes_list ([BoundingBox]): List of BoundingBox objects.
        """
        bounding_boxes_list = []
        current_boxes = []
        previous_image_id = -1
        # Extract information from lines.
        for annotation in annotations:
            (image_id, person_id, pos_x0, pos_y0, pos_x1, pos_y1, certainty, classification,
             object_id) = self.parse_line(annotation, delimiter)
            if not previous_image_id == image_id or previous_image_id == -1:
                bounding_boxes_list.append(BoundingBoxes(current_boxes, previous_image_id))
                current_boxes = []
                previous_image_id = image_id
            bbox = self.parse_box(person_id, pos_x0, pos_y0, pos_x1,
                                  pos_y1, certainty, classification, object_id)
            current_boxes.append(bbox)
        return bounding_boxes_list

    def parse_box(self, identifier, pos_x, pos_y, pos_x2, pos_y2, certainty=None, classification=None, object_id=None):
        bbox = BoundingBox(classification=classification,
                           rectangle=Rectangle(x1=pos_x,
                                               y1=pos_y,
                                               x2=pos_x2,
                                               y2=pos_y2),
                           identifier=identifier,
                           certainty=certainty,
                           object_id=object_id
                           )
        return bbox

    def get_image_dimensions(self, image_id):
        """Gets the size of an image based on its name.

        Args:
            image_id (integer): String with the name of the image.

        Returns:
            (int,int): width and height dimensions of the image.
        """
        raise NotImplementedError('Get image dimensions not implemented')

    def parse_file(self):
        """Parses a file into a BoundingBoxes object.

        Raises:
            NotImplementedError: When the loader is not implemented.
        """
        raise NotImplementedError('parse file method not implemented')

    def parse_line(self, line, delimiter):
        raise NotImplementedError('parse line method not implemented')
