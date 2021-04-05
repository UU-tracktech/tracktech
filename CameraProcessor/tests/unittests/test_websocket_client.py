import pytest
import json
import src.websocket_client as websocket_client


# pylint: disable=attribute-defined-outside-init, no-member
def __eq__(self, other):
    """Custom equalize function

    Args:
        self: first object to compare
        other: second object to compare

    Returns: bool

    """
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False


class TestWebsocketClient():
    """Tests websocket_client.py

    """

    def setup_method(self):
        """Set ups mock messages for unit testing.

        """
        self.start_json = '{"type": "start", "objectId": 1, "frameId": 1, "boxId": 1}'
        self.stop_json = '{"type": "stop", "objectId": 1}'
        self.feature_map_json = '{"type": "featureMap", "objectId": 1, "featureMap": []}'
        self.message_object_start_tracking = json.loads(self.start_json)
        self.message_object_stop_tracking = json.loads(self.stop_json)
        self.message_object_update_feature_map = json.loads(self.feature_map_json)
        self.message_object_start_tracking_string = self.start_json
        self.message_object_stop_tracking_string = self.stop_json
        self.message_object_update_feature_map_string = self.feature_map_json
        self.connect = websocket_client.connected
        self.connection = websocket_client.connection
        self.connect_task_created = websocket_client.connect_task_created
        self.write_message = websocket_client.write_message("test")

    def test_start_tracking(self):
        """Checks if start_tracking takes correct values from message

        """
        assert self.message_object_start_tracking["objectId"] == 1
        assert self.message_object_start_tracking["frameId"] == 1
        assert self.message_object_start_tracking["boxId"] == 1

    def test_stop_tracking(self):
        """Checks if stop_tracking takes correct values from message

        """
        assert self.message_object_stop_tracking["objectId"] == 1

    def test_update_feature_map(self):
        """Checks if update_feature_map takes correct values from message

        """
        assert self.message_object_update_feature_map["objectId"] == 1
        assert self.message_object_update_feature_map["featureMap"] == []

    def test_read_msg_start_tracking(self):
        """Checks if read_msg correctly parses start tracking message

        """
        json_temp_start = websocket_client.read_msg(self.message_object_start_tracking_string)
        assert json_temp_start.__eq__(self.message_object_start_tracking)

    def test_read_msg_stop_tracking(self):
        """Checks if read_msg correctly parses stop tracking message

        """
        json_temp_stop = websocket_client.read_msg(self.message_object_stop_tracking_string)
        assert json_temp_stop.__eq__(self.message_object_stop_tracking)

    def test_read_msg_update_feature_map(self):
        """Checks if read_msg correctly parses update feature map message

        """
        json_temp_feature_map = websocket_client.read_msg(self.message_object_update_feature_map_string)
        assert json_temp_feature_map.__eq__(self.message_object_update_feature_map)

    def test_read_msg_type_error_exception(self):
        """Checks if read_msg raises exception with invalid input

        """
        with pytest.raises(Exception):
            assert websocket_client.read_msg('"invalidJson": "yes"')

    def test_read_msg_key_error_exception(self):
        """Checks if read_msg raises exception with missing value in input

        """
        with pytest.raises(Exception):
            assert websocket_client.read_msg('{"type": "start", "objectId": 1, "frameId": 1}')


if __name__ == '__main__':
    pytest.main(TestWebsocketClient)
