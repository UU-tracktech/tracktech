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

/** The newObject message is sent when a new object is beeing tracked and a cutout is available */
export class NewObjectClientMessage extends ClientMessage {
  constructor(objectId: number, image: string) {
    super('newObject')

    this.objectId = objectId
    this.image = image
  }

  objectId: number
  image: string
}

/** The stop message is sent when an object is no longer being tracked */
export class StopClientMessage extends ClientMessage {
  constructor(objectId: number) {
    super('stop')

    this.objectId = objectId
  }

  objectId: number
}

/** Structure that represents a bounding box */
export class Box {
  constructor(
    boxId: number,
    rect: [number, number, number, number],
    objectType: string,
    objectId?: number
  ) {
    this.boxId = boxId
    this.rect = rect
    this.objectType = objectType
    this.objectId = objectId
  }

  boxId: number
  rect: [number, number, number, number]
  objectType: string
  objectId?: number

  toSize(width: number, height: number) {
    var x1 = this.rect[0],
      y1 = this.rect[1],
      x2 = this.rect[2],
      y2 = this.rect[3]

    //Flip x/y to get the top left corner
    if (x1 > x2) [x1, x2] = [x2, x1]
    if (y1 > y2) [y1, y2] = [y2, y1]

    return {
      left: x1 * width,
      top: y1 * height,
      width: (x2 - x1) * width,
      height: (y2 - y1) * height
    }
  }
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
