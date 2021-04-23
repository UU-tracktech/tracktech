/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

export abstract class OrchestratorMessage {
  constructor(type: string) {
    this.type = type
  }

  type: string
}

export class StartOrchestratorMessage extends OrchestratorMessage {
  constructor(cameraId: string, frameId: number, boxId: number) {
    super('start')

    this.cameraId = cameraId
    this.frameId = frameId
    this.boxId = boxId
  }

  cameraId: string
  frameId: number
  boxId: number
}

export class StopOrchestratorMessage extends OrchestratorMessage {
  constructor(objectId: number) {
    super('stop')

    this.objectId = objectId
  }

  objectId: number
}

export class TestOrchestratorMessage extends OrchestratorMessage {
  constructor(cameraId: string) {
    super('test')

    this.cameraId = cameraId
  }

  cameraId: string
}