"""Tests the dataloader interface.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from tests.conftest import get_test_configs
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.dataloaders.i_dataloader import IDataloader


# pylint: disable=attribute-defined-outside-init
class TestIDataloader:
    """Tests the dataloader interface.

    Attributes:
        dataloader (IDataloader): Dataloader interface to test.
    """

    def setup_method(self):
        """Setup method."""
        configs = get_test_configs()
        self.dataloader = IDataloader(configs)

    def test_init(self):
        """Tests the init."""
        configs = get_test_configs()
        accuracy_config = configs['Accuracy']

        # Check whether properties are set correctly.
        assert self.dataloader.categories == accuracy_config['categories']
        assert self.dataloader.filter_config == configs['Filter']
        assert self.dataloader.nr_frames == int(accuracy_config['nr_frames'])

    def test_invalid_init(self):
        """Negative number of frames should raise an exception."""
        configs = get_test_configs()
        configs['Accuracy']['nr_frames'] = '-1'
        with pytest.raises(AttributeError):
            IDataloader(configs)

    def test_parse_boxes(self):
        """Parse_boxes raises NotImplementedError since parse_line is not implemented in interface."""
        with pytest.raises(NotImplementedError):
            self.dataloader.parse_boxes([(None, None, None, None, None, None, None, None, None)])

    def test_append_box(self, bboxes, bounding_boxes_object_list):
        """Tests the append_box function.

        Args:
            bboxes (BoundingBoxes): BoundingBoxes object.
            bounding_boxes_object_list ([BoundingBoxes]): BoundingBoxes object.
        """
        image_id = bboxes.image_id
        bbox = bboxes.bounding_boxes[0]
        expected_result = bounding_boxes_object_list + [BoundingBoxes([bbox], image_id)]

        returned_box_list = self.dataloader.append_box(bounding_boxes_object_list, bbox)
        assert returned_box_list == expected_result

    def test_append_box_empty_dict(self, bboxes):
        """Tests the append_box function when the bounding_boxes_object_list is empty.

        Args:
            bboxes (BoundingBoxes): BoundingBoxes object.
        """
        image_id = bboxes.image_id
        bbox = bboxes.bounding_boxes[0]
        expected_box_dict = {image_id: BoundingBoxes([bbox], image_id)}
        returned_box_dict = self.dataloader.append_box({}, bbox)
        assert expected_box_dict == returned_box_dict

    def test_append_box_same_id(self, bboxes, bounding_boxes_object_list):
        """Tests the append_box function.

        Args:
            bboxes (BoundingBoxes): BoundingBoxes object.
            bounding_boxes_object_list ([BoundingBoxes]): BoundingBoxes object.
        """
        bounding_boxes_object_list.reverse()

        image_id = bboxes.image_id
        bbox = bboxes.bounding_boxes[0]

        expected_box_list = bounding_boxes_object_list.copy()
        expected_box_list[-1].bounding_boxes.append(bbox)
        returned_box_list = self.dataloader.append_box(bounding_boxes_object_list, bbox)
        assert expected_box_list == returned_box_list

    def test_parse_box(self, bbox):
        """Tests the pares_box function.

        Args:
            bbox (BoundingBox): BoundingBox object.
        """
        constructed_bbox = self.dataloader.parse_box(bbox)
        assert constructed_bbox == bbox

    def test_get_image_dimensions(self):
        """Tests the get_image_dimensions function."""
        with pytest.raises(NotImplementedError):
            self.dataloader.get_image_dimensions(1)

    def test_parse_line(self):
        """Tests the parse_line function."""
        with pytest.raises(NotImplementedError):
            self.dataloader.parse_line('')

    def test_parse_file(self):
        """Tests parsing of file."""
        assert pytest.raises(NotImplementedError, self.dataloader.parse_file)

    def test_get_annotations(self):
        """Tests the get_annotations function."""
        with pytest.raises(NotImplementedError):
            self.dataloader.get_annotations()
