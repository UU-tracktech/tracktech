/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import * as React from 'react'
import { TimelineData, ToDate, timelineEvents, dateRange } from '../../src/classes/timelineData'

test('test ToDate', () => {
  var dateString: string = '2021/05/24 | 14:53:22'
  var date: Date = ToDate(dateString)

  expect(date.getFullYear()).toBe(2021)
  expect(date.getMonth()).toBe(5)
  expect(date.getDate()).toBe(24)
  expect(date.getHours()).toBe(14)
  expect(date.getMinutes()).toBe(53)
  expect(date.getSeconds()).toBe(22)
})

test('test GetImportantEvents with 2 event', () => {
  // Create a new timeline log
  var timelineData = new TimelineData([
    {
      timeStamp: '2021/05/24 | 14:53:22',
      processorId: 'https://tracktech.ml:50008/stream.m3u8'
    },
    {
      timeStamp: '2021/05/24 | 14:53:23',
      processorId: 'https://tracktech.ml:50008/stream.m3u8'
    },
    {
      timeStamp: '2021/05/24 | 14:53:24',
      processorId: 'https://tracktech.ml:50008/stream.m3u8'
    },
    {
      timeStamp: '2021/05/24 | 14:53:40',
      processorId: 'https://tracktech.ml:50008/stream.m3u8'
    },
    {
      timeStamp: '2021/05/24 | 14:53:41',
      processorId: 'https://tracktech.ml:50008/stream.m3u8'
    }
  ])

  var events: timelineEvents = timelineData.GetImportantEvents()

  var firstCamEvents: dateRange[] = events["https://tracktech.ml:50008/stream.m3u8"]
  // There should be two event
  expect(firstCamEvents.length).toBe(2)
  // The first should start at 2021/05/24 | 14:53:22 and end at 2021/05/24 | 14:53:24
  expect(firstCamEvents[0].from).toStrictEqual(new Date(2021, 5, 24, 14, 53, 22))
  expect(firstCamEvents[0].to).toStrictEqual(new Date(2021, 5, 24, 14, 53, 24))
  // The second should start at 2021/05/24 | 14:53:40 and end at 2021/05/24 | 14:53:41
  expect(firstCamEvents[1].from).toStrictEqual(new Date(2021, 5, 24, 14, 53, 40))
  expect(firstCamEvents[1].to).toStrictEqual(new Date(2021, 5, 24, 14, 53, 41))
})
