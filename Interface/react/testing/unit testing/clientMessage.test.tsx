/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import {
  Box,
  BoxesClientMessage,
  QueueItem,
  NewObjectClientMessage,
  StopClientMessage
} from '../../src/classes/clientMessage'

import { size } from '../../src/classes/size'

//Test creation of a BoxesClientMessage
test('BoxesClientMessage', () => {
  const msg = new BoxesClientMessage('camID', 786, [])

  //This kind of message should automatically get created with type boundingboxes
  expect(msg.type).toBe('boundingBoxes')
  //Ensure arguments are used
  expect(msg.cameraId).toBe('camID')
  expect(msg.frameId).toBe(786)
  expect(msg.boxes).toStrictEqual([])
})

//Test creation of a box object
test('Box test', () => {
  const box = new Box(8, [0, 1, 2, 3], 'person', 2346)

  //Ensure all arguments are passed and used correctly
  expect(box.boxId).toBe(8)
  expect(box.rect).toStrictEqual([0, 1, 2, 3])
  expect(box.objectType).toBe('person')
  expect(box.objectId).toBe(2346)
})

//Test toSize of a box object
test('Box toSize test', () => {
  const box = new Box(8, [0, 1, 2, 3], 'person', 2346)

  expect(box.toSize(2, 2)).toStrictEqual({
    left: 0,
    top: 2,
    width: 4,
    height: 4
  })

  const box2 = new Box(4, [2, 4, 0, 1], 'person2', 2346)

  expect(box2.toSize(2, 2)).toStrictEqual({
    left: 0,
    top: 2,
    width: 4,
    height: 6
  })
})

//Test creation of a queueItem
test('QueueItem test', () => {
  const item = new QueueItem(3487, [])

  expect(item.frameId).toBe(3487)
  expect(item.boxes).toStrictEqual([])
})

//Test creation of a NewObjectClientMessage
test('NewObjectClientMessage test', () => {
  const item = new NewObjectClientMessage(123, 'testImage')

  expect(item.objectId).toBe(123)
  expect(item.image).toStrictEqual('testImage')
})

//Test creation of a StopClientMessage
test('StopClientMessage test', () => {
  const item = new StopClientMessage(1234)

  expect(item.objectId).toBe(1234)
})

//Test creation of a StopClientMessage
test('StopClientMessage test', () => {
  const item = new StopClientMessage(1234)

  expect(item.objectId).toBe(1234)
})
