from src.object_manager import TrackingObject, objects


def test_creating_object_adds_it_to_dict():
    tracking_object: TrackingObject = TrackingObject()
    assert objects.keys().__contains__(tracking_object.identifier)


def test_deleting_object_removes_it_from_dict():
    tracking_object: TrackingObject = TrackingObject()
    tracking_object.remove_self()
    assert not objects.keys().__contains__(tracking_object.identifier)


def test_updating_feature_map_replaces_internal_feature_map():
    tracking_object: TrackingObject = TrackingObject()
    tracking_object.update_feature_map({"type": "testFeatureMap"})
    assert tracking_object.feature_map == {"type": "testFeatureMap"}
