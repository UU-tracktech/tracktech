"""
Module for testing accuracy
"""
import unittest
import os
from processor.training.detection.accuracy import AccuracyObject


class MyTestCase(unittest.TestCase):
    """
    Class for unit testing the accuracy object
    """
    def test_check_gt_with_gt(self):
        """This method test if the gt file is the same as the gt file
        Returns: No returns
        """
        object_to_detect = AccuracyObject(os.path.abspath(__file__ + '/../../../../'), 'test', 'gt/gt.txt')
        object_to_detect.detect('gt/gt.txt')
        self.assertEqual(object_to_detect.results['undefined'].fp, 0)

    def test_false_positives(self):
        """ This method test if there are some false positives if there are less boxes in the gt file
        Returns: No returns
        """
        object_to_detect = AccuracyObject(os.path.abspath(__file__ + '/../../../../'), 'test', 'det/test1.txt')
        object_to_detect.detect('gt/gt.txt')
        self.assertEqual(object_to_detect.results['undefined'].fp, 258)

    def test_false_positives2(self):
        """This method tests if there are less true positives if there are less boundingboxes in the gt.
        Returns: No returns
        """
        object_to_detect = AccuracyObject(os.path.abspath(__file__ + '/../../../../'), 'test', 'gt/gt.txt')
        object_to_detect.detect('det/test1.txt')
        object_to_detect2 = AccuracyObject(os.path.abspath(__file__ + '/../../../../'), 'test', 'gt/gt.txt')
        object_to_detect2.detect('gt/gt.txt')
        self.assertEqual(object_to_detect.results['undefined'].tp < object_to_detect2.results['undefined'].tp, True)
