"""Tests for bounding_box.py.

Test different inputs in the class
 - Test if every type is correct.
 - Test empty inputs.
 - Test if every value is correct.
 - Test exceptions.
 - Test if inputs are valid form.

"""

import pytest
from detection.bounding_box import BoundingBox


class TestBoundingBox:

    # Setup
    def setup_method(self):
        self.data = BoundingBox(1, [0, 0, 1, 1], "person", 0.5)
        self.identifier = self.data.identifier
        self.rectangle = self.data.rectangle
        self.feature = None
        self.classification = self.data.classification
        self.certainty = self.data.certainty

    # Testing typechecking
    def test_type_identifier(self):
        assert isinstance(self.identifier,
                          type(self.identifier))

    def test_type_rectangle(self):
        assert isinstance(self.rectangle,
                          type(self.rectangle))

    def test_type_feature(self):
        assert isinstance(self.feature,
                          type(self.feature))

    def test_type_classification(self):
        assert isinstance(self.classification,
                          type(self.classification))

    def test_type_certainty(self):
        assert isinstance(self.certainty,
                          type(self.certainty))

    # Testing empty fields that can be empty
    def test_empty_identifier(self):
        assert self.identifier is not None

    def test_empty_rectangle(self):
        assert self.rectangle is not None

    @pytest.mark.skip(reason="feature attribute is currently unused")
    def test_empty_feature(self):
        assert self.feature is not None

    def test_empty_classification(self):
        assert self.classification is not None

    def test_empty_certainty(self):
        assert self.certainty is not None

    # Testing exceptions
    def test_exception_identifier(self):
        with pytest.raises(Exception):
            assert str(self.identifier) == 'some invalid value'

    def test_exception_rectangle(self):
        with pytest.raises(Exception):
            assert str(self.rectangle) == 'some invalid value'

    def test_exception_feature(self):
        with pytest.raises(Exception):
            assert str(self.feature) == 'some invalid value'

    def test_exception_classification(self):
        with pytest.raises(Exception):
            assert str(self.classification) == 'some invalid  value'

    def test_exception_certainty(self):
        with pytest.raises(Exception):
            assert str(self.certainty) == 'some invalid value'

    # Testing values
    def test_value_identifier(self):
        assert self.identifier == 1

    def test_value_rectangle(self):
        assert self.rectangle == [0, 0, 1, 1]

    def test_value_feature(self):
        assert self.feature is None

    def test_value_classification(self):
        assert self.classification == "person"

    def test_value_certainty(self):
        assert self.certainty == 0.5

    # Testing form
    def test_length_rectangle(self):
        assert len(self.rectangle) == 4

    def test_range_certainty(self):
        assert self.certainty <= 1
        assert self.certainty >= 0


if __name__ == '__main__':
    pytest.main(TestBoundingBox)
