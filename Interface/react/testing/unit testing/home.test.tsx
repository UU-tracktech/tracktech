/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { act, render, screen } from '@testing-library/react'
import { Home } from '../../src/pages/home'

beforeEach(async () => {
  await act(async () => {
    render(<Home />)
  })
})

describe('Checks if all components are there', () => {
  it('Shows the indicator section', () => {
    expect(screen.getByTestId('indicatorsCard')).toBeDefined
  })

  it('shows the object types section', () => {
    expect(screen.getByTestId('filterCard')).toBeDefined
  })

  it('shows the selection section', () => {
    expect(screen.getByTestId('selectionCard')).toBeDefined
  })

  it('shows the camera list', () => {
    expect(screen.getByTestId('cameraList')).toBeDefined
  })

  it('shows the grid', () => {
    expect(screen.getByTestId('gridDiv')).toBeDefined
  })
})
