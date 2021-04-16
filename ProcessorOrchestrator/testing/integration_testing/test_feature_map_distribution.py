import asyncio
import json
import time
import pytest

from tornado import websocket

@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_start_tracking():
    """Test connecting to websocket

    """
    processor_complete = [False]
    processor = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor",
                                          on_message_callback=lambda message:
                                          assert_start_tracking(message, processor_complete))
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

    assert assert_completed(processor_complete[0])


def assert_start_tracking(message, completed):
    message_json = json.loads(message)
    assert message_json["type"] is "start"
    assert message_json["frameId"] is 1
    assert message_json["boxId"] is 1
    completed[0] = True


def assert_completed(test):
    while not test:
        time.sleep(0.5)
    return True


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_websocket_construction():
    """Test connecting to websocket

    """

    processor_1_finished = [False]
    processor_1 = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor",
                                          on_message_callback=lambda message:
                                          assert_feature_map(message, processor_1_finished))
    processor_1.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_1"
    }))

    processor_2_finished = [False]
    processor_2 = \
        await websocket.websocket_connect("ws://processor-orchestrator-service/processor",
                                          on_message_callback=lambda message:
                                          assert_feature_map(message, processor_2_finished))
    processor_2.write_message(json.dumps({
        "type": "identifier",
        "id": "processor_2"
    }))

    processor_1.write_message(json.dumps({
        "type": "featureMap",
        "objectId": 1,
        "featureMap": {}
    }))

    assert assert_completed(processor_1_finished[0])
    assert assert_completed(processor_2_finished[0])


def assert_feature_map(message, complete):
    message_json = json.loads(message)
    assert message_json["type"] is "featureMap"
    assert message_json["objectId"] is 12
    assert message_json["featureMap"] is "{test}"
    complete[0] = True
