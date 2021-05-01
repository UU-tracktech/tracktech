/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { ReactNode } from 'react'

import { OrchestratorMessage } from '../classes/orchestratorMessage'
import { Box, BoxesClientMessage } from '../classes/clientMessage'

/** The various states the websocket can be in */
export type connectionState =
  | 'NONE'
  | 'CONNECTING'
  | 'OPEN'
  | 'CLOSING'
  | 'CLOSED'
  | 'ERROR'

/** Type containing all the arguments needed to create a context with a websocket */
export type websocketArgs = {
  setSocket: (url: string) => void
  send: (message: OrchestratorMessage) => void
  addListener: (
    id: string,
    callback: (boxes: Box[], frameId: number) => void
  ) => number
  removeListener: (listener: number) => void
  connectionState: connectionState
  socketUrl: string
}

/** The context which can be used by other components to send/receive messages */
export const websocketContext = React.createContext<websocketArgs>({
  setSocket: (url: string) => alert(JSON.stringify(url)),
  send: (message: OrchestratorMessage) => alert(JSON.stringify(message)),
  addListener: (_: string, _2: (boxes: Box[], frameId: number) => void) => 0,
  removeListener: (listener: number) => alert(`removing ${listener}`),
  connectionState: 'NONE',
  socketUrl: 'NO URL'
})

/** Listeners can listen for incoming messages and handle contents using the callback */
type Listener = {
  id: string
  listener: number
  callback: (boxes: Box[], frameId: number) => void
}

type WebsocketProviderProps = {
  children: ReactNode
}

export function WebsocketProvider(props: WebsocketProviderProps) {
  /** State keeping track of what state the websocket is in */
  const [connectionState, setConnectionState] = React.useState<connectionState>(
    'NONE'
  )

  /** State keeping track of where the socket is connected to */
  const [socketUrl, setSocketUrl] = React.useState(
    'wss://tracktech.ml:50011/client'
  )

  const socketRef = React.useRef<WebSocket>()
  const listenersRef = React.useRef<Listener[]>([])
  const listenerRef = React.useRef<number>(0)

  React.useEffect(() => setSocket(socketUrl), [])

  /** Creates a socket which tries to connect to the given url */
  function setSocket(url: string) {
    var socket = new WebSocket(url)
    setConnectionState('CONNECTING')
    socket.onopen = (ev: Event) => onOpen(ev)
    socket.onmessage = (ev: MessageEvent<any>) => onMessage(ev)
    socket.onclose = (ev: CloseEvent) => onClose(ev)
    socket.onerror = (ev: Event) => onError(ev)
    setSocketUrl(url)

    socketRef.current = socket
  }

  /** Callback function for when the socket has connected sucessfully */
  function onOpen(_ev: Event) {
    console.log('connected socket')
    setConnectionState('OPEN')
  }

  /** Callback for when a message has been received by the websocket
   *  This will pass on the message to all relevant listeners
   */
  function onMessage(ev: MessageEvent<any>) {
    //console.log('socket message', ev.data)
    var message: BoxesClientMessage = JSON.parse(ev.data)
    listenersRef.current
      ?.filter((listener) => listener.id === message.cameraId)
      .forEach((listener) => listener.callback(message.boxes, message.frameId))
  }

  /** Callback for when the connection is closed */
  function onClose(_ev: CloseEvent) {
    console.log('closed socket')
    setConnectionState('CLOSED')
  }

  /** Callback for when an error occurs with the socket */
  function onError(_ev: Event) {
    console.log('socket error')
    setConnectionState('ERROR')
  }

  /** Adds a listener to this socket */
  function addListener(
    id: string,
    callback: (boxes: Box[], frameId: number) => void
  ) {
    var listener = ++listenerRef.current
    listenersRef.current?.push({ id: id, listener, callback: callback })
    return listener
  }

  /**
   * Remove a listener from this socket
   * @param listener The ID of the listener to remove
   */
  function removeListener(listener: number) {
    listenersRef.current?.filter((x) => x.listener === listener)
  }

  /**
   * Sends a message over the websocket
   * @param message The message to send over the socket
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
        socketUrl: socketUrl
      }}
    >
      {props.children}
    </websocketContext.Provider>
  )
}
