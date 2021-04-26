/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'

import { OrchestratorMessage } from '../classes/orchestratorMessage'
import { Box, BoxesClientMessage } from '../classes/clientMessage'

export type connectionState = 'NONE' | 'CONNECTING' | 'OPEN' | 'CLOSING' | 'CLOSED' | 'ERROR'

export type websocketArgs = {
  setSocket: (url: string) => void
  send: (message: OrchestratorMessage) => void
  addListener: (id: string, callback: (boxes: Box[], frameId: number) => void) => number
  removeListener: (listener: number) => void
  connectionState: connectionState
  socketUrl: string
}

export const websocketContext = React.createContext<websocketArgs>({
  setSocket: (url: string) => alert(JSON.stringify(url)),
  send: (message: OrchestratorMessage) => alert(JSON.stringify(message)),
  addListener: (_: string, _2: (boxes: Box[], frameId: number) => void) => 0,
  removeListener: (listener: number) => alert(`removing ${listener}`),
  connectionState: 'NONE',
  socketUrl: 'NO URL'
})

type Listener = { id: string, listener: number, callback: (boxes: Box[], frameId: number) => void }
export function WebsocketProvider(props) {
  const [connectionState, setConnectionState] = React.useState<connectionState>('NONE')
  const [socketUrl, setSocketUrl] = React.useState('wss://tracktech.ml:50010/client')

  const socketRef = React.useRef<WebSocket>()
  const listenersRef = React.useRef<Listener[]>()
  const listenerRef = React.useRef<number>(0)

  React.useEffect(() => setSocket(socketUrl), [])

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

  function onOpen(ev: Event) {
    console.log('connected socket')
    setConnectionState('OPEN')
  }

  function onMessage(ev: MessageEvent<any>) {
    console.log('socket message', ev.data)
    var message: BoxesClientMessage = JSON.parse(ev.data)
    listenersRef.current?.filter((listener) => listener.id === message.cameraId).forEach((listener) => listener.callback(message.boxes, message.frameId))
  }

  function onClose(ev: CloseEvent) {
    console.log('closed socket')
    setConnectionState('CLOSED')
  }

  function onError(ev: Event) {
    console.log('socket error')
    setConnectionState('ERROR')
  }

  function addListener(id: string, callback: (boxes: Box[], frameId: number) => void) {
    var listener = ++listenerRef.current
    listenersRef.current?.push({ id: id, listener, callback: callback })
    return listener
  }

  function removeListener(listener: number) {
    listenersRef.current?.filter(x => x.listener === listener)
  }

  function send(message: OrchestratorMessage) {
    if (!socketRef.current) throw new Error('socket is undefined')
    socketRef.current.send(JSON.stringify(message))
  }

  return (
    <websocketContext.Provider value={
      {
        setSocket: (url: string) => setSocket(url),
        send: (message: OrchestratorMessage) => send(message),
        addListener: (id: string, callback: (boxes: Box[], frameId: number) => void) => addListener(id, callback),
        removeListener: (listener: number) => removeListener(listener),
        connectionState: connectionState,
        socketUrl: socketUrl
      }}>
      {props.children}
    </websocketContext.Provider>
  )
}