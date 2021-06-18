/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import { Box } from 'classes/box'

/** Abstract class for messages received from the processor orchestrator. */
export abstract class ClientMessage {
  constructor(type: string) {
    this.type = type
  }

  type: string
}

/** The BoxesClientMessage is created when bounding box data is received. */
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

/** The newObject message is sent when a new object is being tracked, and a cutout is available. */
export class NewObjectClientMessage extends ClientMessage {
  constructor(objectId: number, image: string) {
    super('newObject')

    this.objectId = objectId
    this.image = image
  }

  objectId: number
  image: string
}

/** The stop message is sent when an object is no longer being tracked. */
export class StopClientMessage extends ClientMessage {
  constructor(objectId: number) {
    super('stop')

    this.objectId = objectId
  }

  objectId: number
}
