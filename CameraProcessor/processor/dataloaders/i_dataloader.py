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

    def __init__(self, configs):
        """Initialize dataloader.

        Args:
            configs (dict): A dictionary of the configs.
        """
        accuracy_config = configs['Accuracy']
        self.categories = accuracy_config['categories']
        self.filter_config = configs['Filter']
        self.current_boxes = []
        self.previous_image_id = -1
        nr_frames = int(accuracy_config['nr_frames'])
        # Cannot contain negative amount of frames.
        if nr_frames < 0:
            raise AttributeError('Cannot have negative number of frames')
        self.nr_frames = nr_frames

    def parse_boxes(self, annotations):
        """Parses bounding boxes.

        Args:
            annotations ([(str)]): Annotations tuples in a list.

        Returns:
            bounding_boxes_list ([BoundingBox]): List of BoundingBox objects.
        """
        bounding_boxes_list = []
        # Extract information from lines.
        for annotation in annotations:
            parsed_line = self.parse_line(annotation)
            for parsed_entity in parsed_line:
                (image_id, person_id, pos_x0, pos_y0, pos_x1, pos_y1, certainty, classification,
                 object_id) = parsed_entity
                bounding_boxes_list = self.append_box(bounding_boxes_list, image_id, person_id, pos_x0, pos_y0, pos_x1,
                                                      pos_y1, certainty, classification,
                                                      object_id)

        return bounding_boxes_list

    def append_box(self,
                   bounding_boxes_list, image_id, person_id,
                   pos_x0, pos_y0, pos_x1, pos_y1,
                   certainty, classification, object_id):
        """Appends boxes.

        Args:
            bounding_boxes_list ([BoundingBox]): Bounding box object.
            image_id (int): ID of image.
            person_id (int): ID of person
            pos_x0 (int): Top-left x value.
            pos_y0 (int): Top-left y vclue.
            pos_x1 (int): Bottom-right x value.
            pos_y1 (int): Bottom-right y value.
            certainty (float): Certainnty.
            classification (string): Classification.
            object_id (int): ID of object.

        Returns:
            bounding_boxes_list ([BoundingBox]): List of BoundingBoxes.
        """
        if not self.previous_image_id == image_id or self.previous_image_id == -1:
            bounding_boxes_list.append(BoundingBoxes(self.current_boxes, self.previous_image_id))
            self.current_boxes = []
            self.previous_image_id = image_id
        bbox = self.parse_box(person_id, pos_x0, pos_y0, pos_x1,
                              pos_y1, certainty, classification, object_id)
        self.current_boxes.append(bbox)
        return bounding_boxes_list

    @staticmethod
    def parse_box(identifier, pos_x, pos_y, pos_x2, pos_y2, certainty=None, classification=None, object_id=None):
        """Parses a box.

        Args:
            identifier (int): ID.
            pos_x (float): Top-left x value.
            pos_y (flaot): Top-left y value.
            pos_x2 (float): Bottum-right x value.
            pos_y2 (float): Bottom-right y value.
            certainty (float): Certainty.
            classification (string): Classification.
            object_id (int): ID of object.

        Returns:
            bbox (BoundingBox): Bounding box object.
        """
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

        Raises:
            NotImplementedError.
        """
        raise NotImplementedError('Get image dimensions not implemented')

    def parse_line(self, line):
        """Base functions of parse_line.

        Args:
            line (line): Line.

        Raises:
            NotImplementedError.
        """
        raise NotImplementedError('Parse line not implemented')

    def parse_file(self):
        """Parses an annotations file.

        Returns:
            bounding_boxes_list (list): List of bounding boxes.
        """
        annotations = self.get_annotations()
        bounding_boxes_list = self.parse_boxes(annotations)
        return bounding_boxes_list

    def get_annotations(self):
        """Reads the annotations from a file.

                Returns:
                    annotations ([(str)]): Annotations tuples in a list.
                """
        raise NotImplementedError('get annotations not implemented')
