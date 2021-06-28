"""Datawriter implementation for not writing anything.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.data_writer.i_data_writer import IDataWriter


class FakeDataWriter(IDataWriter):
    """Class that mimics the behaviour of a data writer, but does not write anything."""
    def __init__(self):
        """Init method for a fake data writer object."""
        super().__init__()

    def write(self, bounding_boxes, shape):
        """Empty write method."""
        pass

    def close(self):
        """Empty close method."""
        pass
