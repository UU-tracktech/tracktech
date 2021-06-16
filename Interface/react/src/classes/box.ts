/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/** The size of the overlay, used to scale the drawing of the bounding boxes. */
export type size = { left: number; top: number; width: number; height: number }

/** Structure that represents a bounding box. */
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
  
    /**
     * Transform tha coordinates that are in between 0 and 1 to coordinates relative to the width and height of the display.
     * @param width Width of the display.
     * @param height Height of the display.
     * @returns A size object containing the relative offset, widht and height.
     */
    toSize(width: number, height: number): size {
      var x1 = this.rect[0],
        y1 = this.rect[1],
        x2 = this.rect[2],
        y2 = this.rect[3]
  
      // Flip x/y to get the top left corner.
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