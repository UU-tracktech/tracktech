/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { render, screen } from '@testing-library/react'
import { Timelines } from 'pages/timelines'

// Tests that simply check if all expected components are there
describe('Checks if all components are there', () => {
  it('Shows the tracked objects card', () => {
    render(<Timelines />)
    expect(screen.getByTestId('tracked-objects-container')).toBeDefined()
  })

  it('shows the timelines page title', () => {
    render(<Timelines />)
    expect(screen.getByTestId('timelines-page-title')).toBeDefined()
  })

  it('shows the timelines page content', () => {
    render(<Timelines />)
    expect(screen.getByTestId('timelines-page-content')).toBeDefined()
  })
})