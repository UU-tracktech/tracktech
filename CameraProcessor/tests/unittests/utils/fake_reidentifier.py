"""Mock re-identifier for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from processor.pipeline.reidentification.ireidentifier import IReIdentifier


class FakeReIdentifier(IReIdentifier):
    """A fake re-identifier that implements the same methods but just mocks some functionality
    """
    def extract_features(self, frame_obj, track_obj):
        """ Mocks feature extraction method

        Returns:
            float[]: An empty vector
        """

        return []

    # pylint: disable=unnecessary-pass
    def re_identify(self, frame_obj, track_obj, re_id_data):
        """ Mocks re_identify function
        """
        pass
