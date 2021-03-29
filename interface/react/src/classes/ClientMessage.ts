export abstract class ClientMessage {
  constructor(type: string) {
    this.type = type
  }

  type: string
}

export class BoxesClientMessage extends ClientMessage {
  constructor(cameraId: number, frameId: number, boxes: Box[]) {
    super('boundingBoxes')

    this.cameraId = cameraId
    this.frameId = frameId
    this.boxes = boxes
  }

  cameraId: number
  frameId: number
  boxes: Box[]
}

export class Box {
  constructor(x: number, y: number, width: number, height: number, type: number) {
    this.x = x
    this.y = y
    this.width = width
    this.height = height
    this.type = type
  }

  x: number
  y: number
  width: number
  height: number
  type: number
}