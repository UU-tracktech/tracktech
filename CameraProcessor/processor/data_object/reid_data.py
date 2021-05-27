"""Contains re-id data class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class ReidData:
    """This class stores two dictionaries that are useful for re-identification. The first dictionary,
    query_boxes, stores the object_ids belonging to box_ids, if those box_ids contain objects that need
    to be re-identified. The second dictionary, query_features, stores the feature vectors from the cutout of each
    object that we want to re-identify (we call this a query).
    """
    def __init__(self):
        """Initializer for the class.

        """
        # Dictionary that maps from box_id -> object_id
        self.__query_boxes = {}

        # Dictionary that maps from object_id -> feature vector
        self.__query_features = {}

    def add_query_box(self, box_id, object_id):
        """Link the object id to the box id in a dictionary.

        Args:
            box_id (int): The id of the bounding box.
            object_id (int): The id of the queried object.
        """
        self.__query_boxes[box_id] = object_id

    def add_query_feature(self, object_id, feature_vector):
        """Store the feature vector of a queried object in a dictionary

        Args:
            object_id (int): The id of the queried object.
            feature_vector ([float]): the feature vector of the queried object.
        """
        self.__query_features[object_id] = feature_vector

    def remove_query(self, object_id):
        """Removes the items of query_boxes and query_features containing the object_id of a query we no
        long want to re-identify.

        Args:
            object_id (int): The id of the query we no longer wish to re-identify.
        """
        # Delete the feature vector from the object ID
        del self.__query_features[object_id]

        # Delete all box ids that map to the object ID
        for box_id, obj_id in self.__query_boxes.items():
            if obj_id == object_id:
                del self.__query_boxes[box_id]

    def get_object_id_for_box(self, box_id):
        """ Returns the object id for a given box id (possibly None).

        Args:
            box_id (int): id of the box that is being followed.

        Returns:
            (int or None): If the box contains an object that is being followed, return the object_id. Otherwise,
            return None.
        """
        return self.__query_boxes.get(box_id, None)

    def get_queries(self):
        """Get a list of queries (object ids) that are currently being tracked.

        Returns:
            ([int]): The list of object IDs currently being tracked
        """
        return self.__query_features.keys()

    def get_feature_for_query(self, object_id):
        """Returns the feature vector for a given object id. Raises error if the object_id is not in the list.

        Args:
            object_id (int): id of the object

        Returns:
            ([float]): Feature vector for the object
        """
        return self.__query_featuers[object_id]