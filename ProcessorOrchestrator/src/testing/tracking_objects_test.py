"""Contains testing methods for the tracking object class"""
from src.object_manager import TrackingObject, objects


def test_creating_object_adds_it_to_dict():
    """Test if a tracking object which has just been created appends itself to the dict of all objects"""
    tracking_object: TrackingObject = TrackingObject()
    assert objects.keys().__contains__(tracking_object.identifier)


def test_deleting_object_removes_it_from_dict():
    """Test whether calling remove on a tracking object actually removes it from the dict of all objects"""
    tracking_object: TrackingObject = TrackingObject()
    tracking_object.remove_self()
    assert not objects.keys().__contains__(tracking_object.identifier)


def test_updating_feature_map_replaces_internal_feature_map():
    """Test whether calling the update_feature_map function actually updates the internal
    feature map of the object"""
    tracking_object: TrackingObject = TrackingObject()
    tracking_object.update_feature_map({"type": "testFeatureMap"})
    assert tracking_object.feature_map == {"type": "testFeatureMap"}
