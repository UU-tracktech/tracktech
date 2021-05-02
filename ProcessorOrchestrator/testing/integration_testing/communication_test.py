"""Integration testing module that tests the communication functionality of the orchestrator."""

import json
import time
import pytest

from tornado import websocket


@pytest.mark.asyncio
@pytest.mark.timeout(20)
async def test_start_tracking():
    """Test if interface can send a start tracking command that is then send to the correct processor."""

    # Wait a little bit so the test server can start
    time.sleep(5)
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


def assert_start_tracking(message):
    """Help method to assert if the start tracking message is as expected"""
    message_json = json.loads(message)
    assert message_json["type"] == "start"
    assert message_json["frameId"] == 1
    assert message_json["boxId"] == 1
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_feature_map_distribution():
    """Test if a processor can send a feature map and if it is correctly distributed among the processors"""

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
    """Help method to assert if the received feature map message is as expected"""
    message_json = json.loads(message)
    assert message_json["type"] == "featureMap"
    assert message_json["objectId"] == 1
    assert message_json["featureMap"] == {"test": "test"}
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_bounding_boxes_distribution():
    """Test if a processor can send a bounding box message and if it is correctly received by the interface"""

    processor = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    processor.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_4"
    }))

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")

    processor.write_message(json.dumps({
        "type": "boundingBoxes",
        "frameId": 1,
        "boxes": {
            "box1": {},
            "box2": {}
        }
    }))

    message = await interface.read_message()
    assert assert_boxes_message(message)


def assert_boxes_message(message):
    """Help method to assert if the received boxes message is as expected"""
    message_json = json.loads(message)
    assert message_json["type"] == "boundingBoxes"
    assert message_json["cameraId"] == "processor_4"
    assert message_json["frameId"] == 1
    assert message_json["boxes"] == {
            "box1": {},
            "box2": {}
        }
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(30)
async def test_stop_tracking():
    """Test if an interface can send a stop tracking message and if it is correctly received by the processor"""

    processor = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor")
    await processor.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_5"
    }))

    interface = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/client")
    await interface.write_message(json.dumps({
        "type": "stop",
        "objectId": 1
    }))

    message = await processor.read_message()
    assert assert_stop_tracking(message)


def assert_stop_tracking(message):
    """Help method to assert if the stop tracking message is as expected"""
    message_json = json.loads(message)
    assert message_json["type"] == "stop"
    assert message_json["objectId"] == 1
    return True

@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_stop_server():
    """Sends message to test server so it can be stopped."""
    socket = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/stop")
    await socket.write_message("stop")
