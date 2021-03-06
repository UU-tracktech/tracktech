"""Tests the tracking objects.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

Unit testing module that only tests tracking object class.
"""

# Pytest resolves this reference internally.
# Noinspection PyUnresolvedReferences.
from src.objects.object_management import objects
from src.objects.tracking_object import TrackingObject


def test_creating_object_adds_it_to_dict():
    """Tests whether a tracking object which has just been created is also added to the dict of objects."""
    tracking_object = TrackingObject(None)
    assert objects.keys().__contains__(tracking_object.identifier)


def test_deleting_object_removes_it_from_dict():
    """Tests whether calling remove_self on the tracking object actually removes it from the dict of objects."""
    tracking_object = TrackingObject(None)
    tracking_object.remove_self()
    assert not objects.keys().__contains__(tracking_object.identifier)


def test_updating_feature_map_replaces_internal_feature_map():
    """Tests whether feature maps are updated internally when the corresponding function is called."""
    tracking_object = TrackingObject(None)
    tracking_object.update_feature_map({'type': 'testFeatureMap'})
    assert tracking_object.feature_map == {'type': 'testFeatureMap'}


def test_image_properly_set():
    """Test whether the image given in an object constructor is made available."""
    tracking_object = TrackingObject('test')
    assert tracking_object.image == 'test'
