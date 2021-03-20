import React, { useState, useCallback, useMemo, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

export const WebSocket = () => {
    //Public API that will echo messages sent to it back to the client
    const [socketUrl, setSocketUrl] = useState('wss://echo.websocket.org'); //echo server

    const {
        sendMessage,
        lastMessage,
        readyState,
    } = useWebSocket(socketUrl);

    const messageHistory = useRef([lastMessage]);

    messageHistory.current = useMemo(() =>
        messageHistory.current.concat(lastMessage),[lastMessage]);

    //test functions
    const testClickChangeSocketUrl = useCallback(() =>
        setSocketUrl('ws://tracktech.ml:50010/client'), []); //portainer server

    const testClickSendMessage = useCallback((cameraID) => (event) =>
        sendMessage('{"type":"test", "cameraId":' + cameraID + '}'), []);

    //connection status of web socket
    const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting',
        [ReadyState.OPEN]: 'Open',
        [ReadyState.CLOSING]: 'Closing',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    }[readyState];


    //function for start tracking target 'bodID' on camera 'cameraID' in frame 'frameID'
    const handleStart = useCallback((cameraID, boxID, frameID) => (event) =>
        sendMessage(
            '{"type":"start", "cameraId":"' + cameraID + '", "boxId":"' + boxID + '", "frameId":"' + frameID + '"}'),
        []);

    //function for stop tracking target 'objectID'
    const handleStop = useCallback((objectID) => (event) =>
        sendMessage(
            '{"type":"stop", "objectId":"' + objectID + '"}'),
        []);

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
    );
};
export default WebSocket;