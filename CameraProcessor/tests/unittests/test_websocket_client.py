import pytest
import json
from processor.websocket_client import WebsocketClient


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
        self.ws_client = WebsocketClient("")
        self.start_json = '{"type": "start", "objectId": 1, "frameId": 1, "boxId": 1}'
        self.stop_json = '{"type": "stop", "objectId": 1}'
        self.feature_map_json = '{"type": "featureMap", "objectId": 1, "featureMap": []}'
        self.message_object_start_tracking = json.loads(self.start_json)
        self.message_object_stop_tracking = json.loads(self.stop_json)
        self.message_object_update_feature_map = json.loads(self.feature_map_json)
        self.message_object_start_tracking_string = self.start_json
        self.message_object_stop_tracking_string = self.stop_json
        self.message_object_update_feature_map_string = self.feature_map_json
        self.start_tracking = self.ws_client.start_tracking(self.message_object_start_tracking)
        self.stop_tracking = self.ws_client.stop_tracking(self.message_object_stop_tracking)
        self.update_feature_map = self.ws_client.update_feature_map(self.message_object_update_feature_map)
        self.connect = self.ws_client.connect
        self.write_message = self.ws_client._write_message("test")

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
        json_temp_start = self.ws_client._on_message(self.message_object_start_tracking_string)
        assert json_temp_start.__eq__(self.message_object_start_tracking)

    def test_read_msg_stop_tracking(self):
        """Checks if read_msg correctly parses stop tracking message

        """
        json_temp_stop = self.ws_client._on_message(self.message_object_stop_tracking_string)
        assert json_temp_stop.__eq__(self.message_object_stop_tracking)

    def test_read_msg_update_feature_map(self):
        """Checks if read_msg correctly parses update feature map message

        """
        json_temp_feature_map = self.ws_client._on_message(self.message_object_update_feature_map_string)
        assert json_temp_feature_map.__eq__(self.message_object_update_feature_map)

    def test_read_msg_type_error_exception(self):
        """Checks if read_msg raises exception with invalid input

        """
        with pytest.raises(Exception):
            assert self.ws_client._on_message('"invalidJson": "yes"')

    def test_read_msg_key_error_exception(self):
        """Checks if read_msg raises exception with missing value in input

        """
        with pytest.raises(Exception):
            assert self.ws_client._on_message('{"type": "start", "objectId": 1, "frameId": 1}')

    def test_unparsed_json_input_start_tracking(self):
        """Checks if start_tracking raises exception with is parsed JSON

        """
        with pytest.raises(Exception):
            assert self.ws_client.start_tracking(self.start_json)

    def test_parsed_json_input_start_tracking(self):
        """Checks if start_tracking raises exception with is parsed JSON

        """
        self.ws_client.start_tracking(self.message_object_start_tracking)

    def test_parsed_json_input_stop_tracking(self):
        """Checks if start_tracking raises exception with is parsed JSON

        """
        self.ws_client.stop_tracking(self.message_object_stop_tracking)

    def test_parsed_json_input_feature_map(self):
        """Checks if start_tracking raises exception with in parsed JSON

        """
        self.ws_client.update_feature_map(self.message_object_update_feature_map)


if __name__ == '__main__':
    pytest.main(TestWebsocketClient)
