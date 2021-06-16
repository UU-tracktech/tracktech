/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { render, screen } from '@testing-library/react'
import { Grid } from 'components/grid'

// The test environment has no implementation for window.alert
// so to prevent errors, create a mock implementation for these tests
beforeAll(() => {
  jest.spyOn(window, 'alert').mockImplementation(() => {})
})

afterAll(() => {
  jest.spyOn(window, 'alert').mockRestore()
})

// Tests for the creation of the grid and function calling
describe('Tests for grid properties', () => {
  // Test if the number of grid elements matches the number of sources passed through properties
  it('Creates a gridelement for every source', () => {
    const testSources = [
      {
        id: 'src1',
        name: 'cam1',
        srcObject: { src: 'src', type: 'type' }
      },
      {
        id: 'src2',
        name: 'cam2',
        srcObject: { src: 'src', type: 'type' }
      },
      {
        id: 'src3',
        name: 'cam3',
        srcObject: { src: 'src', type: 'type' }
      },
      {
        id: 'src4',
        name: 'cam4',
        srcObject: { src: 'src', type: 'type' }
      }
    ]

    render(
      <Grid
        primary={'src1'}
        setPrimary={jest.fn()}
        sources={testSources}
        indicator={'All'}
        hiddenObjectTypes={[]}
      />
    )

    expect(screen.queryAllByTestId('gridElement').length).toBe(
      testSources.length
    )
  })

  // Test if clicking the Set primary button calls the setPrimary function correctly
  it('Calls the setprimary function correctly', async () => {
    // VideoJs will throw some errors about the source being incompatible
    // Replace the error implementation to keep logs clean
    let spy = jest.spyOn(console, 'error').mockImplementation(() => {})
    let mockFn = jest.fn()

    render(
      <Grid
        setPrimary={mockFn}
        sources={[
          {
            id: 'src1',
            name: 'cam1',
            srcObject: { src: 'src', type: 'type' }
          }
        ]}
        indicator={'All'}
        hiddenObjectTypes={[]}
      />
    )

    while (screen.queryByText('Set primary') == null) {
      await new Promise((r) => setTimeout(r, 100))
    }

    screen.getByText('Set primary').click()
    expect(mockFn).toBeCalled()
    expect(mockFn).toBeCalledWith('src1')

    // Restore the console.error implementation
    spy.mockRestore()
  })
})
