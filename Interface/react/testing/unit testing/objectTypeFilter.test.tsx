import * as React from 'react'
import { screen, render, getAllByTestId } from '@testing-library/react'
import { ObjectTypeFilter } from '../../src/components/objectTypeFilter'

test('it renders without error', () => {
  render(
    <ObjectTypeFilter
      objectTypes={[]}
      addHidden={jest.fn()}
      removeHidden={jest.fn()}
    />
  )
})

test('the number of buttons correspond to the number of object types', () => {
  render(
    <ObjectTypeFilter
      objectTypes={[
        ['type1', false],
        ['type2', false],
        ['type3', false],
        ['type4', false],
        ['type5', false],
        ['type6', false]
      ]}
      addHidden={jest.fn()}
      removeHidden={jest.fn()}
    />
  )

  //get the Card containing the buttons
  const card = screen.getByTestId('filterCard')

  //We passed a list of 6 elements, so the card should have 6 buttons as children
  const children = getAllByTestId(card, 'filterButton')
  expect(children.length).toBe(6)
})

describe('Button clicking tests', () => {
  it.todo('changes appearance on click')

  it.todo('calls addHidden function correctly')

  it.todo('calls removeHidden function correctly')
})
