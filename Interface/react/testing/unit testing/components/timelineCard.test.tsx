/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { render, screen } from '@testing-library/react'
import { TimelineCard } from 'components/timelineCard'

describe('Tests for timelineCard component properties', () => {
  it('Shows the correct ID', () => {
    render(<TimelineCard cameraId={'someID'} />)

    expect(screen.queryByText('someID')).toBeTruthy()
  })

  it('Displays given children correctly', () => {
    render(<TimelineCard cameraId={'ID'} children={<span>Test</span>} />)

    expect(screen.queryByText('Test')).toBeTruthy()
  })
})
