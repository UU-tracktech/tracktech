"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class ITracker:
    """Tracker interface.
    """
    def track(self, track_obj):
        """Performs tracking stage using the tracking object.

        Args:
            track_obj (TrackingObj): tracking object to perform tracking stage with.
        """
        raise NotImplementedError('Tracking stage not implemented')
