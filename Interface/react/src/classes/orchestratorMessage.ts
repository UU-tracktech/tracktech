/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/** Abstract class for messages sent to the processor orchestrator. */
export abstract class OrchestratorMessage {
  constructor(type: string) {
    this.type = type
  }

  type: string
}

/**
 * Message to start tracking an object on a specified camera.
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
 * Message to stop tracking of an object.
 */
export class StopOrchestratorMessage extends OrchestratorMessage {
  constructor(objectId: number) {
    super('stop')

    this.objectId = objectId
  }

  objectId: number
}

/**
 * Message used to specify whether this client should receive images of tracked objects.
 */
export class SetUsesImagesMessage extends OrchestratorMessage {
  constructor(usesImages: boolean) {
    super('setUsesImages')

    this.usesImages = usesImages
  }

  usesImages: boolean
}

/**
 * Message used to authenticate this client with the processor orchestrator, to make sure it handles the messages.
 */
export class AuthenticateOrchestratorMessage extends OrchestratorMessage {
  constructor(jwt: string) {
    super('authenticate')

    this.jwt = jwt
  }

  jwt: string
}
