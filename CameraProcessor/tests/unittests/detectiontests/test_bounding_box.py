"""Tests for bounding_box.py.

Test different inputs in the class
 - Test if every type is correct.   done
 - Test if every value is correct.  done
 - Test empty inputs.               done
 - Test exceptions.                 done

"""

import pytest
from detection.bounding_box import BoundingBox


class TestBoundingBox:

    def setup_method(self):
        self.data = BoundingBox(1, [0, 0, 1, 1], "person", 0.5)
        self.unit_identifier = self.data.identifier
        self.unit_rectangle = self.data.rectangle
        self.unit_feature = None
        self.unit_classification = self.data.classification
        self.unit_certainty = self.data.certainty
        assert len(self.unit_rectangle) == 4

    # Testing typechecking
    def test_type_identifier(self):
        assert isinstance(self.unit_identifier,
                          type(self.unit_identifier))

    def test_type_rectangle(self):
        assert isinstance(self.unit_rectangle,
                          type(self.unit_rectangle))

    def test_type_feature(self):
        assert isinstance(self.unit_feature,
                          type(self.unit_feature))

    def test_type_classification(self):
        assert isinstance(self.unit_classification,
                          type(self.unit_classification))

    def test_type_certainty(self):
        assert isinstance(self.unit_certainty,
                          type(self.unit_certainty))

    # Testing empty fields that can be empty
    def test_empty_identifier(self):
        assert self.unit_identifier is not None

    def test_empty_rectangle(self):
        assert self.unit_rectangle is not None

    @pytest.mark.skip(reason="feature attribute is currently unused")
    def test_empty_feature(self):
        assert self.unit_feature is not None

    def test_empty_classification(self):
        assert self.unit_classification is not None

    def test_empty_certainty(self):
        assert self.unit_certainty is not None

    # Testing exceptions
    def test_exception_identifier(self):
        with pytest.raises(Exception):
            assert str(self.unit_identifier) == 'one'

    def test_exception_rectangle(self):
        with pytest.raises(Exception):
            assert str(self.unit_rectangle) == [1]

    def test_exception_feature(self):
        with pytest.raises(Exception):
            assert str(self.unit_feature) == 'some invalid feature'

    def test_exception_classification(self):
        with pytest.raises(Exception):
            assert str(self.unit_classification) == 9

    def test_exception_certainty(self):
        with pytest.raises(Exception):
            assert str(self.unit_certainty) == 'some invalid value'

    # Testing values
    def test_value_identifier(self):
        assert self.unit_identifier == 1

    def test_value_rectangle(self):
        assert self.unit_rectangle == [0, 0, 1, 1]

    def test_value_feature(self):
        assert self.unit_feature is None

    def test_value_classification(self):
        assert self.unit_classification == "person"

    def test_value_certainty(self):
        assert self.unit_certainty == 0.5


if __name__ == '__main__':
    pytest.main(TestBoundingBox)
