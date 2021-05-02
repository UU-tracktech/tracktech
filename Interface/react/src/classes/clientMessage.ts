/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/** Incoming messages are of type ClientMessage */
export abstract class ClientMessage {
  constructor(type: string) {
    this.type = type
  }

  type: string
}

/** The BoxesClientMessage is created when bounding box data is received */
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

/** Structure that represents a bounding box */
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

/** Used by the overlay to store bounding boxes alongside their frameID */
export class QueueItem {
  constructor(frameId: number, boxes: Box[]) {
    this.frameId = frameId
    this.boxes = boxes
  }

  frameId: number
  boxes: Box[]
}
