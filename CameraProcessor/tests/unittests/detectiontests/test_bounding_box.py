'''Tests for bounding_box.py

Test different inputs in the class
 - Test if every type is correct.   done
 - Test if every value is correct.  not done
 - Test empty inputs.               done
 - Test exceptions.                 not done

'''


import unittest
from detection.bounding_box import BoundingBox

class BoundingBox(BoundingBox):
    def contains_identifier(self):
        self.identifier = 1
    def contains_rectangle(self):
        self.rectangle = [0,0,1,1]
    def contains_feature(self):
        self.feature = None
    def contains_classification(self):
        self.classification = "person"
    def contains_certainty(self):
        self.certainty = 0.5

    def empty_classification(self):
        self.classification = None


class TestBoundingBox(unittest.TestCase):
    # Testing typechecking
    def test_type_identifier(self):
        self.assertIsInstance(BoundingBox.contains_identifier(self),
                              type(BoundingBox.contains_identifier(self)),
                              'Tested identifier is not of type identifier.')
    def test_type_rectangle(self):
        self.assertIsInstance(BoundingBox.contains_rectangle(self),
                              type(BoundingBox.contains_rectangle(self)),
                              'Tested rectangle is not of type rectangle.')
    def test_type_feature(self):
        self.assertIsInstance(BoundingBox.contains_feature(self),
                              type(BoundingBox.contains_feature(self)),
                              'Tested feature is not of type feature.')
    def test_type_classification(self):
        self.assertIsInstance(BoundingBox.contains_classification(self),
                              type(BoundingBox.contains_classification(self)),
                              'Tested classification is not of type classification.')
    def test_type_certainty(self):
        self.assertIsInstance(BoundingBox.contains_certainty(self),
                              type(BoundingBox.contains_certainty(self)),
                              'Tested certainty is not of type certainty')
    # Testing empty fields that can be empty
    def test_empty_classification(self):
        self.assertIsNone(BoundingBox.empty_classification(self),
                          'Classification is not empty.')



if __name__ == '__main__':
    unittest.main()
