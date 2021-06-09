/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/** Any message going to the orchestrator needs to be of type OrchestratorMessage */
export abstract class OrchestratorMessage {
  constructor(type: string) {
    this.type = type
  }

  type: string
}

/**
 * The StartOrchestratorMessage lets the orchestrator know to start sending
 * boundingbox data for the specified camera
 */
export class StartOrchestratorMessage extends OrchestratorMessage {
  constructor(
    cameraId: string,
    frameId: number,
    boxId: number,
    image?: string
  ) {
    super('start')

    this.cameraId = cameraId
    this.frameId = frameId
    this.boxId = boxId
    this.image = image
  }

  cameraId: string
  frameId: number
  boxId: number
  image?: string
}

/**
 * The StopOrchestratorMessage will tell the orchestrator to stop sending
 * data about the specified camera
 */
export class StopOrchestratorMessage extends OrchestratorMessage {
  constructor(objectId: number) {
    super('stop')

    this.objectId = objectId
  }

  objectId: number
}

/**
 * The SetUsesImagesMessage is used to specify whether this client should receive
 * messages of newly tracked objects
 */
export class SetUsesImagesMessage extends OrchestratorMessage {
  constructor(usesImages: boolean) {
    super('setUsesImages')

    this.usesImages = usesImages
  }

  usesImages: boolean
}
