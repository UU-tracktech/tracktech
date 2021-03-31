export abstract class OrchestratorMessage {
  constructor(type: string) {
    this.type = type
  }

  type: string
}

export class StartOrchestratorMessage extends OrchestratorMessage {
  constructor(cameraId: number, frameId: number, boxId: number) {
    super('start')

    this.cameraId = cameraId
    this.frameId = frameId
    this.boxId = boxId
  }

  cameraId: number
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
  constructor(cameraId: number) {
    super('test')

    this.cameraId = cameraId
  }

  cameraId: number
}