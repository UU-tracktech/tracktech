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
  constructor(id: number, x1: number, y1: number, x2: number, y2: number, type: number) {
    this.id = id
    this.x1 = x1
    this.y1 = y1
    this.x2 = x2
    this.y2 = y2
    this.type = type
  }

  id: number
  x1: number
  y1: number
  x2: number
  y2: number
  type: number
}