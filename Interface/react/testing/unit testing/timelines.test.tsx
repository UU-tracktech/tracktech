/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { act, render, screen } from '@testing-library/react'
import { Home } from '../../src/pages/home'
import { Timelines } from '../../src/pages/timelines'

beforeEach(async () => {
  await act(async () => {
    render(<Timelines />)
  })
})

describe('Checks if all components are there', () => {
  it('Shows the tracked objects card', () => {
    expect(screen.getByTestId('tracked-objects-container')).toBeDefined
  })

  it('shows the timelines page title', () => {
    expect(screen.getByTestId('timelines-page-title')).toBeDefined
  })

  it('shows the timelines page content', () => {
    expect(screen.getByTestId('timelines-page-content')).toBeDefined
  })
})
