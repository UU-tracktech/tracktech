export abstract class ClientMessage {
  constructor(type: string) {
    this.type = type
  }

  type: string
}

export class BoxesClientMessage extends ClientMessage {
  constructor(cameraId: string, frameId: number, boxes: Box[]) {
    super('boundingBoxes')

    this.cameraId = cameraId
    this.frameId = frameId
    this.boxes = boxes
  }

  cameraId: string
  frameId: number
  boxes: Box[]
}

export class Box {
  constructor(boxId: number, rect: number[], objectId?: number) {
    this.boxId = boxId
    this.rect = rect
    this.objectId = objectId
  }

  boxId: number
  rect: number[]
  objectId?: number
  
}