/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { ReactNode, useContext } from 'react'

import {
  OrchestratorMessage,
  SetUsesImagesMessage,
  AuthenticateOrchestratorMessage
} from 'classes/orchestratorMessage'
import {
  BoxesClientMessage,
  NewObjectClientMessage,
  StopClientMessage
} from 'classes/clientMessage'
import { Box } from 'classes/box'
import { authContext } from 'components/authContext'

/** The various states the websocket can be in. */
export type connectionState =
  | 'NONE'
  | 'CONNECTING'
  | 'OPEN'
  | 'CLOSING'
  | 'CLOSED'
  | 'ERROR'

/** Type containing all the arguments needed to create a context with a websocket. */
export type websocketArgs = {
  setSocket: (url: string) => void
  send: (message: OrchestratorMessage) => void
  addListener: (
    id: string,
    callback: (boxes: Box[], frameId: number) => void
  ) => number
  removeListener: (listener: number) => void
  connectionState: connectionState
  objects: NewObjectClientMessage[]
}

/** The context which can be used by other components to send/receive messages. */
export const websocketContext = React.createContext<websocketArgs>({
  setSocket: (url: string) => alert(JSON.stringify(url)),
  send: (message: OrchestratorMessage) => alert(JSON.stringify(message)),
  addListener: (_: string, _2: (boxes: Box[], frameId: number) => void) => 0,
  removeListener: (listener: number) => alert(`removing ${listener}`),
  connectionState: 'NONE',
  objects: []
})

/** Listeners can listen for incoming messages and handle contents using the callback. */
type Listener = {
  id: string
  listener: number
  callback: (boxes: Box[], frameId: number) => void
}

/** Properties for a websocket provider, only requires react children. */
type WebsocketProviderProps = {
  children: ReactNode
}

/**
 * Context provider for a websocket connection with the processor orchestrator.
 * @param props Properties containing children.
 * @returns The children wrapped with a websocket context provider.
 */
export function WebsocketProvider(props: WebsocketProviderProps) {
  /** State keeping track of what state the websocket is in. */
  const [connectionState, setConnectionState] = React.useState<connectionState>(
    'NONE'
  )

  // State keeping track of objects that were added.
  const [objects, setObjects] = React.useState<NewObjectClientMessage[]>([])

  // Get current authentication data.
  const { token } = useContext(authContext)

  const socketRef = React.useRef<WebSocket>()
  const listenersRef = React.useRef<Listener[]>([])
  const listenerRef = React.useRef<number>(0)

  /**
   * Creates a socket which tries to connect to the given url.
   * @param url Url of the websocket server.
   */
  function setSocket(url: string) {
    try {
      var socket = new WebSocket(url)
      setConnectionState('CONNECTING')
      socket.onopen = (ev: Event) => onOpen(ev)
      socket.onmessage = (ev: MessageEvent<any>) => onMessage(ev)
      socket.onclose = (ev: CloseEvent) => onClose(ev)
      socket.onerror = (ev: Event) => onError(ev)

      socketRef.current = socket
      // Catch fail due to possible incorrect url.
    } catch {}
  }

  /**
   * Callback function for when the socket has connected sucessfully.
   * @param _ev Event argument.
   */
  function onOpen(_ev: Event) {
    setConnectionState('OPEN')

    try {
      // Authenticate the client.
      if (token) send(new AuthenticateOrchestratorMessage(token))
      // Let the orchestrator know that this client should receive images of new tracking objects.
      send(new SetUsesImagesMessage(true))
    } catch {
      // The first send can throw an error under testing, even though the message is sent properly.
    }
  }

  /**
   * Callback for when a message has been received by the websocket.
   * @param ev Event argument containing the message.
   */
  function onMessage(ev: MessageEvent<any>) {
    let data = JSON.parse(ev.data)
    switch (data.type) {
      case 'boundingBoxes':
        let object: BoxesClientMessage = data
        handleBoundingBoxesMessage(object)
        break
      case 'newObject':
        let object2: NewObjectClientMessage = data
        handleNewObjectMessage(object2)
        break
      case 'stop':
        let object3: StopClientMessage = data
        handleStopMessage(object3)
        break
    }
  }

  /**
   * Handles a bounding boxes message from the orchestrator, will pass on the message to all relevant listeners.
   * @param object The client message that was received.
   */
  function handleBoundingBoxesMessage(object: BoxesClientMessage) {
    var message = new BoxesClientMessage(
      object.cameraId,
      object.frameId,
      object.boxes.map(
        (box: Box) => new Box(box.boxId, box.rect, box.objectType, box.objectId)
      )
    )
    listenersRef.current
      ?.filter((listener) => listener.id === message.cameraId)
      .forEach((listener) => listener.callback(message.boxes, message.frameId))
  }

  /**
   * Handles a new Object message from the orchestrator, will set the new obect in the state.
   * @param object The client message that was received.
   */
  function handleNewObjectMessage(object: NewObjectClientMessage) {
    var message = new NewObjectClientMessage(object.objectId, object.image)
    setObjects((objects) => [
      ...objects.filter(
        (trackedObject) => trackedObject.objectId !== message.objectId
      ),
      message
    ])
  }

  /**
   * Handles a stop message from the orchestrator, will remove the object from the selection panel.
   * @param object The client message that was received.
   */
  function handleStopMessage(object: StopClientMessage) {
    var message = new StopClientMessage(object.objectId)
    setObjects((objects) =>
      objects.filter(
        (trackedObject) => trackedObject.objectId !== message.objectId
      )
    )
  }

  /**
   * Callback for when the connection is closed.
   * @param _ev Event argument.
   */
  function onClose(_ev: CloseEvent) {
    setConnectionState('CLOSED')
  }

  /**
   * Callback for when an error occurs with the socket.
   * @param _ev Event argument.
   */
  function onError(_ev: Event) {
    setConnectionState('ERROR')
  }

  /**
   * Adds a listener to this socket.
   * @param id Id of of the camera.
   * @param callback Callback for when a message arrives.
   * @returns The new listener.
   */
  function addListener(
    id: string,
    callback: (boxes: Box[], frameId: number) => void
  ) {
    var listener = ++listenerRef.current
    listenersRef.current?.push({ id: id, listener, callback: callback })
    return listener
  }

  /**
   * Remove a listener from this socket.
   * @param listener The Id of the listener to remove.
   */
  function removeListener(listener: number) {
    listenersRef.current = listenersRef.current?.filter(
      (x) => x.listener === listener
    )
  }

  /**
   * Sends a message over the websocket.
   * @param message The message to send over the socket.
   */
  function send(message: OrchestratorMessage) {
    if (!socketRef.current) throw new Error('socket is undefined')
    socketRef.current.send(JSON.stringify(message))
  }

  return (
    <websocketContext.Provider
      value={{
        setSocket: (url: string) => setSocket(url),
        send: (message: OrchestratorMessage) => send(message),
        addListener: (
          id: string,
          callback: (boxes: Box[], frameId: number) => void
        ) => addListener(id, callback),
        removeListener: (listener: number) => removeListener(listener),
        connectionState: connectionState,
        objects: objects
      }}
    >
      {props.children}
    </websocketContext.Provider>
  )
}
