import pytest
from src.pipeline.detection.bounding_box import BoundingBox


# pylint: disable=attribute-defined-outside-init
class TestBoundingBox:
    """Tests bounding_box.py.

    """

    # Setup
    def setup_method(self):
        """Set ups bounding_box for unit testing.

        """
        self.data = BoundingBox(1, [0, 0, 1, 1], "person", 0.5)
        self.identifier = self.data.identifier
        self.rectangle = self.data.rectangle
        self.feature = None
        self.classification = self.data.classification
        self.certainty = self.data.certainty

    # Testing typechecking
    def test_type_identifier(self):
        """Asserts if value of identifier is of correct type.

        """
        assert isinstance(self.identifier,
                          type(self.identifier))

    def test_type_rectangle(self):
        """Asserts if value of rectangle is of correct type.

        """
        assert isinstance(self.rectangle,
                          type(self.rectangle))

    def test_type_feature(self):
        """Asserts if value of feature is of correct type.

        """
        assert isinstance(self.feature,
                          type(self.feature))

    def test_type_classification(self):
        """Asserts if value of classification is of correct type.

        """
        assert isinstance(self.classification,
                          type(self.classification))

    def test_type_certainty(self):
        """Asserts if value of certainty is of correct type.

        """
        assert isinstance(self.certainty,
                          type(self.certainty))

    # Testing empty fields that can be empty
    def test_empty_identifier(self):
        """Asserts if identifier is not None.

        """
        assert self.identifier is not None

    def test_empty_rectangle(self):
        """Asserts if rectangle is not None.

        """
        assert self.rectangle is not None

    @pytest.mark.skip(reason="feature attribute is currently unused")
    def test_empty_feature(self):
        """Asserts if feature is not None.

        """
        assert self.feature is not None

    def test_empty_classification(self):
        """Asserts if classification is not None.

        """
        assert self.classification is not None

    def test_empty_certainty(self):
        """Asserts if certainty is not None.

        """
        assert self.certainty is not None

    # Testing exceptions
    def test_exception_identifier(self):
        """Asserts if identifier throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.identifier) == 'some invalid value'

    def test_exception_rectangle(self):
        """Asserts if rectangle throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.rectangle) == 'some invalid value'

    def test_exception_feature(self):
        """Asserts if feature throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.feature) == 'some invalid value'

    def test_exception_classification(self):
        """Asserts if classification throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.classification) == 'some invalid  value'

    def test_exception_certainty(self):
        """Asserts if certainty throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.certainty) == 'some invalid value'

    # Testing values
    def test_value_identifier(self):
        """Asserts if value of identifier is correct.

        """
        assert self.identifier == 1

    def test_value_rectangle(self):
        """Asserts if value of rectangle is correct.

        """
        assert self.rectangle == [0, 0, 1, 1]

    def test_value_feature(self):
        """Asserts if value of feature is correct.

        """
        assert self.feature is None

    def test_value_classification(self):
        """Asserts if value of classification is correct.

        """
        assert self.classification == "person"

    def test_value_certainty(self):
        """Asserts if value of certainty is correct.

        """
        assert self.certainty == 0.5

    # Testing form
    def test_length_rectangle(self):
        """Asserts if rectangle is of length 4.

        """
        assert len(self.rectangle) == 4

    def test_range_certainty(self):
        """Asserts if certainty is within range 0...1.

        """
        assert self.certainty <= 1
        assert self.certainty >= 0


if __name__ == '__main__':
    pytest.main(TestBoundingBox)
