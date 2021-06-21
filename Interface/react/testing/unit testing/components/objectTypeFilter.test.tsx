/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

*/

import React from 'react'
import { screen, render } from '@testing-library/react'
import { ObjectTypeFilter } from 'components/objectTypeFilter'

// Collection of tests for the properties of the ObjectTypeFilter component
describe('Tests for the objectTypeFilter properties', () => {
  // Test that the correct text is displayed on a button
  it('Renders the object type as text on the button', () => {
    let types: [string, boolean][] = [['typeName', false]]

    render(
      <ObjectTypeFilter
        objectTypes={types}
        addHidden={jest.fn()}
        removeHidden={jest.fn()}
      />
    )

    expect(screen.queryByText('typeName')).toBeTruthy()
  })

  // Test that every type gets a button
  it('Renders a number of buttons equal to the number of object types', () => {
    let types: [string, boolean][] = [
      ['type1', false],
      ['type2', false],
      ['type3', false],
      ['type4', false],
      ['type5', false]
    ]

    render(
      <ObjectTypeFilter
        objectTypes={types}
        addHidden={jest.fn()}
        removeHidden={jest.fn()}
      />
    )

    expect(screen.getAllByTestId('filterButton').length).toBe(types.length)
  })

  // Test that clicking the button calls the correct function based on visibility
  it('Toggles the visibility of a type when clicking the button', () => {
    let mockHide = jest.fn()
    let mockShow = jest.fn()

    render(
      <ObjectTypeFilter
        objectTypes={[
          ['type1', true],
          ['type2', false]
        ]}
        addHidden={mockHide}
        removeHidden={mockShow}
      />
    )

    expect(screen.queryByText('type1')).toBeTruthy()
    expect(screen.queryByText('type2')).toBeTruthy()

    screen.getByText('type1').click()
    expect(mockHide).toBeCalled()
    expect(mockHide).toBeCalledWith('type1')

    screen.getByText('type2').click()
    expect(mockShow).toBeCalled()
    expect(mockShow).toBeCalledWith('type2')
  })
})
