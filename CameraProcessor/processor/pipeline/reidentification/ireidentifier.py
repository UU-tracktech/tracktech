"""Detection abstract class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class IReIdentifier:
    """Superclass for identifiers.
    """

    def extract_features(self, frame_obj, track_obj):
        """Given a det_obj object, extract the features of it.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            track_obj (BoundingBoxes): BoundingBoxes object that has the bounding boxes of the tracking stage

        Returns:
            float[]: returns the feature vectors of the tracked objects.
        """
        raise NotImplementedError("Extract features function not implemented")

    def similarity(self, query_features, gallery_features):
        """Compute the similarity rate between the feature vectors of the query object and the gallery object.

        Args:
            query_features (numpy.array(float)): The feature vector of the query object.
            gallery_features (numpy.array(float)): The feature vector of a object in the gallery.

        Returns:
            float: returns a numpy array containing the feature values of a det_obj object
        """
        raise NotImplementedError("Similarity function not implemented")
