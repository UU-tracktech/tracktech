import React, { useState, useCallback, useMemo, useRef } from 'react'
import useWebSocket, { ReadyState } from 'react-use-websocket'
import React, { useState, useCallback, useMemo, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import Queue from '../Datastructures/Queue'

export const WebSocket = (q2) => {
    //Public API that will echo messages sent to it back to the client
    const [socketUrl, setSocketUrl] = useState('wss://echo.websocket.org') //echo server

    const {
        sendMessage,
        sendJsonMessage,
        lastMessage,
        lastJsonMessage,
        readyState,
        getWebSocket
    } = useWebSocket(socketUrl, {
        onOpen: () => console.log("Connection opened"),
        shouldReconnect: () => true, //try to reconnect when connection is lost
        onError: () => console.log("Error with socket connection"),
        onMessage: () => JSONTest(lastJsonMessage),
        onClose: () => console.log("Connection closed")
    })

    const messageHistory = useRef([lastMessage])

    messageHistory.current = useMemo(() =>
        messageHistory.current.concat(lastMessage),[lastMessage])

    console.log("length of the current history");
    console.log(messageHistory.current.length);

    console.log("length of the current history");
    console.log(messageHistory.current.length);

    //test functions
    const testClickChangeSocketUrl = useCallback(() =>
        setSocketUrl('wss://tracktech.ml:50010/client'), []) //portainer server

    const testClickSendMessage = useCallback((cameraID) => () =>
        sendMessage('{"type":"test", "cameraId":' + cameraID + '}'), [])

    //connection status of web socket
    const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting',
        [ReadyState.OPEN]: 'Open',
        [ReadyState.CLOSING]: 'Closing',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    }[readyState]


    //function for start tracking target 'bodID' on camera 'cameraID' in frame 'frameID'
    const handleStart = useCallback((cameraID, boxID, frameID) => () =>
        sendMessage(
            '{"type":"start", "cameraId":"' + cameraID + '", "boxId":"' + boxID + '", "frameId":"' + frameID + '"}'),
        [])

    //function for stop tracking target 'objectID'
    const handleStop = useCallback((objectID) => () =>
        sendMessage(
            '{"type":"stop", "objectId":"' + objectID + '"}'),
        [])

    //converts JSON input into usable object
    //the returned boundingBoxJSON is an object with the data from the JSON
    //For example boundingBoxJSON.type returns the type of the JSON
    function parseMessage (input) {
        const processInput = input.substring(1, input.length-1).replace(/['" ]+/g,'')
        console.log(processInput.split(',')[0])
        return  {
            type: JSON.stringify(processInput.split(',')[0].split(':')[1]),
            cameraID: JSON.stringify(processInput.split(',')[1].split(':')[1]),
            frameId: JSON.stringify(processInput.split(',')[2].split(':')[1]),
            boxes: [JSON.stringify(processInput.split(',')[3].split(':')[1])]
        }
    }

    //test function to print input
    function JSONTest (input) {
        if(input != null) {
            console.log("type of JSON is: " + parseMessage(JSON.stringify(input)).type);
            console.log("cameraID of JSON is: " + parseMessage(JSON.stringify(input)).cameraID);
            console.log("frameID of JSON is: " + parseMessage(JSON.stringify(input)).frameId);
            console.log("boxes of JSON is: " + parseMessage(JSON.stringify(input)).boxes);
            q.push(parseMessage(JSON.stringify(input)).type)
            console.log(q.length)
            q2.enqueue(parseMessage(JSON.stringify(input)).type)
            console.log("size of q2 is: " + q2.size())
            //q2.push(parseMessage(JSON.stringify(input)).type)
        }
    }

    function pushToQueue(){

    }

    return (
        <div>
            <button
                onClick={testClickChangeSocketUrl}
            >
                Change Socket Url
            </button>
            <button
                onClick={testClickSendMessage(69)}
                disabled={readyState !== ReadyState.OPEN}
            >
                Send test json
            </button>
            <button
                onClick={handleStart(1, 1, 1)}
                disabled={readyState !== ReadyState.OPEN}
            >
                Send start json
            </button>
            <button
                onClick={handleStop(1)}
                disabled={readyState !== ReadyState.OPEN}
            >
                Send stop json
            </button>
            <span>The WebSocket is currently {connectionStatus}</span>
            {lastMessage ? <span>Last message: {lastMessage.data}</span> : null}
            <ul>
                {messageHistory.current
                    .map((message, idx) => <span key={idx}>{message?.['data']}</span>)}
            </ul>
        </div>
    )
}
export default WebSocket