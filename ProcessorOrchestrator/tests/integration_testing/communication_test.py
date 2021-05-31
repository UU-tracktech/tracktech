"""Integration testing module that tests the communication functionality of the orchestrator.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import json
import time
import pytest
import requests

from tornado import websocket


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_bad_message_interface():
    """Test if the interface can send a bad message without crashing the server."""

    # Wait a little bit so the test server can start.
    time.sleep(5)

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    interface.write_message("This message is unusable for the orchestrator")


@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_incomplete_message_interface():
    """Test if the interface can send an incomplete message without crashing the server."""

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    interface.write_message(json.dumps({
        "type": "start",
        "cameraId": "processor_1"
    }))


@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_unknown_action_message_interface():
    """Test if the interface can send a message of unknown type without crashing the server."""

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    interface.write_message(json.dumps({
        "type": "unknown"
    }))


@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_unknown_processor_message_interface():
    """Test if the interface can send an incomplete message without crashing the server."""

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    interface.write_message(json.dumps({
        "type": "start",
        "cameraId": "unknown",
        "frameId": 1,
        "boxId": 1
    }))


@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_unknown_object_message_interface():
    """Test if the interface can send an incomplete message without crashing the server."""

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    interface.write_message(json.dumps({
        "type": "stop",
        "objectId": "999"
    }))


@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_bad_message_processor():
    """Test if the processor can send a bad message without crashing the server."""

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    interface.write_message("bad message")


@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_incomplete_message_processor():
    """Test if the processor can send an incomplete message without crashing the server."""

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    interface.write_message(json.dumps({
        "type": "identifier"
    }))


@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_unknown_action_message_processor():
    """Test if the processor can send a message of unknown type without crashing the server."""

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    interface.write_message(json.dumps({
        "type": "unknown"
    }))


@pytest.mark.asyncio
@pytest.mark.timeout(40)
async def test_start_tracking_and_timeout():
    """Test if interface can send a start tracking command that is then send to the correct processor.
    Also test if after a few seconds the object is automatically no longer tracked."""

    processor = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    processor.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_1"
    }))

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    interface.write_message(json.dumps({
        "type": "start",
        "cameraId": "processor_1",
        "frameId": 1,
        "boxId": 1
    }))

    message = await processor.read_message()
    assert assert_start_tracking(message)

    message_2 = await processor.read_message()
    assert assert_stop_tracking(message_2, 1)


def assert_start_tracking(message):
    """Help method to assert if the start tracking message is as expected.

    Args:
        message (json): json message with start tracking command.
    """
    message_json = json.loads(message)
    assert message_json["type"] == "start"
    assert message_json["frameId"] == 1
    assert message_json["boxId"] == 1
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(40)
async def test_start_tracking_with_image_and_timeout():
    """Test if interface can send a start tracking command with only an image
    that is then send to the correct processor.
    Also test if after a few seconds the object is automatically no longer tracked."""

    processor = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    processor.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_1b"
    }))

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    interface.write_message(json.dumps({
        "type": "start",
        "cameraId": "processor_1b",
        "image": "test"
    }))

    message = await processor.read_message()
    assert assert_start_tracking_with_image(message)

    message_2 = await processor.read_message()
    assert assert_stop_tracking(message_2, 1)


def assert_start_tracking_with_image(message):
    """Help method to assert if the start tracking message is as expected, with an image parameter.

    Args:
        message (str): Json string containing the message.

    Returns:
        bool: Whether message has been correct.
    """
    message_json = json.loads(message)
    assert message_json["type"] == "start"
    assert message_json["image"] == "test"
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_feature_map_distribution():
    """Test if a processor can send a feature map and if it is correctly distributed among the processors."""

    processor_1 = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    processor_1.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_2"
    }))

    processor_2 = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    processor_2.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_3"
    }))

    processor_1.write_message(json.dumps({
        "type": "featureMap",
        "objectId": 1,
        "featureMap": {"test": "test"}
    }))

    processor_1_message = await processor_1.read_message()
    processor_2_message = await processor_2.read_message()

    assert assert_feature_map(processor_1_message)
    assert assert_feature_map(processor_2_message)


def assert_feature_map(message):
    """Help method to assert if the received feature map message is as expected.

    Args:
        message (json): json message with bounding boxes.
    """
    message_json = json.loads(message)
    assert message_json["type"] == "featureMap"
    assert message_json["objectId"] == 1
    assert message_json["featureMap"] == {"test": "test"}
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_bounding_boxes_distribution_and_timeline_logging():
    """Test if a processor can send a bounding box message and if it is correctly received by the interface.

    Also test if the timeline is logged properly and the serving handler is available.
    """

    processor = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    processor.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_4"
    }))

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")

    interface.write_message(json.dumps({
        "type": "start",
        "cameraId": "processor_4",
        "frameId": 1,
        "boxId": 1
    }))

    processor.write_message(json.dumps({
        "type": "boundingBoxes",
        "frameId": 1,
        "boxes": [
            {"objectId": 1},
            # This next one isn't tracked so should cause a message at the processor.
            {"objectId": 2},
            {"rect": []}
        ]
    }))

    message = await interface.read_message()
    assert assert_boxes_message(message)

    response = json.loads(requests.get('http://processor-orchestrator-service/timelines?objectId=1').text)
    assert len(list(filter(lambda x: x["processorId"] == "processor_4", response["data"]))) > 0

    processor.close()

    # Stop tracking both objects, as tey are no longer needed.
    interface.write_message(json.dumps({
        "type": "stop",
        "objectId": 1
    }))
    interface.write_message(json.dumps({
        "type": "stop",
        "objectId": 2
    }))


def assert_boxes_message(message):
    """Help method to assert if the received boxes message is as expected.

    Args:
        message (json): json message with bounding boxes.
    """
    message_json = json.loads(message)
    assert message_json["type"] == "boundingBoxes"
    assert message_json["cameraId"] == "processor_4"
    assert message_json["frameId"] == 1
    assert message_json["boxes"] == [
            {"objectId": 1},
            {"objectId": 2},
            {"rect": []}
        ]
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_bad_bounding_boxes_message():
    """Test if sending a bad bounding boxes message does not crash the server."""

    processor = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    processor.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_4"
    }))

    processor.write_message(json.dumps({
        "type": "boundingBoxes",
        "frameId": 1,
        "boxes": "invalid"
    }))


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_incomplete_timeline_data_request():
    """Test if requesting timeline data without objectId parameter gives the correct response."""

    response = requests.get('http://processor-orchestrator-service/timelines').text
    assert response == "Missing 'objectId' query parameter"


@pytest.mark.asyncio
@pytest.mark.timeout(30)
async def test_stop_tracking():
    """Test if an interface can send a stop tracking message and if it is correctly received by the processor."""

    processor = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    await processor.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_5"
    }))

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    await interface.write_message(json.dumps({
        "type": "start",
        "cameraId": "processor_5",
        "frameId": 1,
        "boxId": 1,
    }))
    await interface.write_message(json.dumps({
        "type": "stop",
        "objectId": 1
    }))

    # Read start message first.
    _ = await processor.read_message()
    message = await processor.read_message()
    assert assert_stop_tracking(message, 1)


def assert_stop_tracking(message, object_id):
    """Help method to assert if the stop tracking message is as expected.

    Args:
        message (json): json message containing the stop command.
        object_id (int): integer containing the object id.
    """
    message_json = json.loads(message)
    assert message_json["type"] == "stop"
    assert message_json["objectId"] == object_id
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(30)
async def test_startup_message():
    """Test if a processor gets the currently tracked feature maps."""

    processor_1 = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    await processor_1.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_6"
    }))

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    await interface.write_message(json.dumps({
        "type": "start",
        "cameraId": "processor_6",
        "frameId": 1,
        "boxId": 1,
    }))

    processor_1.write_message(json.dumps({
        "type": "featureMap",
        "objectId": 1,
        "featureMap": {"test": "test"}
    }))

    processor_2 = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    await processor_2.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_7"
    }))

    # Read start message first.
    message = await processor_2.read_message()
    assert assert_feature_map(message)


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_stop_server():
    """Sends message to test server so it can be stopped."""
    socket = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/stop")
    await socket.write_message("stop")
