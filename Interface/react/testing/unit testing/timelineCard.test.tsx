/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import { TimelineCard } from '../../src/components/timelineCard'

test('Timeline card renders without error', () => {
  render(<TimelineCard cameraId='testCam' />)
})

test('Timeline card shows correct name', () => {
  //Render a card with 'testCam' as the title
  const { rerender } = render(<TimelineCard cameraId='testCam' />)
  expect(screen.queryByText('testCam')).not.toBe(null)

  //rerender the card with 'differentCam' as title.
  //'title' as title should be gone and now it should be 'different'
  rerender(<TimelineCard cameraId='differentCam' />)
  expect(screen.queryByText('testCam')).toBe(null)
  expect(screen.queryByText('differentCam')).not.toBe(null)
})

test('Timeline card children are rendered', () => {
  //Render a card with children
  render(
    <TimelineCard cameraId='testCam'>
      <span>Test</span>
    </TimelineCard>
  )
  expect(screen.queryByText('Test')).not.toBe(null)
})
