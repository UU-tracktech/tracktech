/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import { Box } from 'classes/box'

/** Used by the overlay to store bounding boxes alongside their frameID. */
export class QueueItem {
    constructor(frameId: number, boxes: Box[]) {
      this.frameId = frameId
      this.boxes = boxes
    }
  
    frameId: number
    boxes: Box[]
  }