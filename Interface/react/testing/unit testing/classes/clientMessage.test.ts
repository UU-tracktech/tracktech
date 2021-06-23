/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import {
  BoxesClientMessage,
  NewObjectClientMessage,
  StopClientMessage
} from 'classes/clientMessage'
import { Box } from 'classes/box'
import { QueueItem } from 'classes/queueItem'

// Collection of tests for the classes contained in the clientmessage file
describe('Test the creation of each class in the clientMesasage file', () => {
  // Test the boundingbox message creation
  it('Creates boundingbox message correctly', () => {
    let boxes = [new Box(24, [1, 2, 3, 4], 'objType')]
    let msg = new BoxesClientMessage('camID', 123, boxes)

    expect(msg.type).toBe('boundingBoxes')
    expect(msg.cameraId).toBe('camID')
    expect(msg.frameId).toBe(123)
    expect(msg.boxes).toBe(boxes)
  })

  // Test the newObject message creation
  it('Creates newObject message correctly', () => {
    let msg = new NewObjectClientMessage(321, 'linkToImage')

    expect(msg.type).toBe('newObject')
    expect(msg.objectId).toBe(321)
    expect(msg.image).toBe('linkToImage')
  })

  // Test the creation of the stop message
  it('Creates stop message correctly', () => {
    let msg = new StopClientMessage(765)

    expect(msg.type).toBe('stop')
    expect(msg.objectId).toBe(765)
  })

  // Test the creation of a box
  it('Creates boxes correctly', () => {
    //A boundingbox belonging to a classified object that is not tracked
    let classedBox = new Box(32, [1, 2, 3, 4], 'someType')

    expect(classedBox.boxId).toBe(32)
    expect(classedBox.rect).toStrictEqual([1, 2, 3, 4])
    expect(classedBox.objectType).toBe('someType')
    expect(classedBox.objectId).not.toBeDefined()

    //The bounding box made for a tracked object
    let trackedBox = new Box(51, [5, 6, 7, 8], 'otherType', 12)

    expect(trackedBox.boxId).toBe(51)
    expect(trackedBox.rect).toStrictEqual([5, 6, 7, 8])
    expect(trackedBox.objectType).toBe('otherType')
    expect(trackedBox.objectId).toBe(12)
  })

  // Test if the toSize function returns the correct size
  it('Obtains correct size of a box', () => {
    let expected = { left: 10, top: 10, width: 10, height: 10 }

    let box = new Box(1, [2, 2, 4, 4], 'someType')
    expect(box.toSize(5, 5)).toStrictEqual(expected)

    let box2 = new Box(2, [4, 4, 2, 2], 'someType')
    expect(box2.toSize(5, 5)).toStrictEqual(expected)
  })

  // Test the creation of a QueueItem
  it('Creates QueueItems correctly', () => {
    let boxList = [new Box(78, [1, 2, 3, 4], 'someType')]
    let item = new QueueItem(37, boxList)

    expect(item.frameId).toBe(37)
    expect(item.boxes).toBe(boxList)
  })
})
