/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { TimelineData, ToDate } from 'classes/timelineData'

//Collection of tests that test the creation of timelines for objects
describe('TimelineData class tests', () => {
  // Test creation of a timeline for a single object that appeared only once
  it('Creates a correct timeline for one object with one entry', () => {
    let log = [{ timeStamp: '2021/6/10 | 16:17:20', processorId: '1' }]
    let data = new TimelineData(log)
    expect(data.GetImportantEvents()).toMatchObject({
      '1': [
        {
          from: ToDate(log[0].timeStamp),
          to: ToDate(log[0].timeStamp)
        }
      ]
    })
  })

  // Test creation of a timeline for multiple objects that both appeared once
  it('Creates a correct timeline for multiple objects with one entry', () => {
    let log = [
      { timeStamp: '2021/6/10 | 16:17:20', processorId: '1' },
      { timeStamp: '2021/6/10 | 16:18:20', processorId: '2' }
    ]
    let data = new TimelineData(log)

    expect(data.GetImportantEvents()).toMatchObject({
      '1': [
        {
          from: ToDate(log[0].timeStamp),
          to: ToDate(log[0].timeStamp)
        }
      ],
      '2': [
        {
          from: ToDate(log[1].timeStamp),
          to: ToDate(log[1].timeStamp)
        }
      ]
    })
  })

  // Test the creation of a timeline for one object that appeared twice over a long period of time
  it('Creates a correct timeline for one object with multiple entries', () => {
    let log = [
      { timeStamp: '2021/6/10 | 16:17:20', processorId: 'processor1' },
      { timeStamp: '2021/6/10 | 16:27:20', processorId: 'processor1' }
    ]
    let data = new TimelineData(log)

    expect(data.GetImportantEvents()).toMatchObject({
      processor1: [
        {
          from: ToDate(log[0].timeStamp),
          to: ToDate(log[0].timeStamp)
        },
        {
          from: ToDate(log[1].timeStamp),
          to: ToDate(log[1].timeStamp)
        }
      ]
    })
  })

  // Test the creation of a timeline for one object that appeared twice within the threshold to maintain tracking
  it('Creates a correct timeline for one object with multiple entries within the threshold', () => {
    let log = [
      { timeStamp: '2021/6/10 | 16:17:20', processorId: 'processor1' },
      { timeStamp: '2021/6/10 | 16:17:22', processorId: 'processor1' }
    ]
    let data = new TimelineData(log)

    expect(data.GetImportantEvents()).toMatchObject({
      processor1: [
        {
          from: ToDate(log[0].timeStamp),
          to: ToDate(log[1].timeStamp)
        }
      ]
    })
  })

  // Test the creation of a timeline for one object that appeared multiple times at different intervals
  it('Creates a correct timeline for one object with many entries', () => {
    let log = [
      { timeStamp: '2021/6/10 | 16:17:20', processorId: 'processor1' },
      { timeStamp: '2021/6/10 | 16:17:21', processorId: 'processor1' },
      { timeStamp: '2021/6/10 | 16:17:22', processorId: 'processor1' },
      { timeStamp: '2021/6/10 | 16:20:50', processorId: 'processor1' },
      { timeStamp: '2021/6/10 | 16:25:22', processorId: 'processor1' },
      { timeStamp: '2021/6/10 | 16:25:23', processorId: 'processor1' }
    ]
    let data = new TimelineData(log)

    expect(data.GetImportantEvents()).toMatchObject({
      processor1: [
        {
          from: ToDate(log[0].timeStamp),
          to: ToDate(log[2].timeStamp)
        },
        {
          from: ToDate(log[3].timeStamp),
          to: ToDate(log[3].timeStamp)
        },
        {
          from: ToDate(log[4].timeStamp),
          to: ToDate(log[5].timeStamp)
        }
      ]
    })
  })
})

// Test the toDate function used for timelineData
describe('TimelineData Function test', () => {
  it('returns a correct date', () => {
    let date = ToDate('2021/6/10 | 16:17:20')
    let expected = new Date(2021, 6, 10, 16, 17, 20)
    expect(date).toStrictEqual(expected)
  })
})
