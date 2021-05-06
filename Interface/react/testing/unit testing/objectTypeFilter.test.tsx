import * as React from 'react'
import { screen, render, getAllByTestId } from '@testing-library/react'
import '@testing-library/jest-dom'
import { ObjectTypeFilter } from '../../src/components/objectTypeFilter'

/** Basic test to ensure the coponent renders without errors */
test('it renders without error', () => {
  render(
    <ObjectTypeFilter
      objectTypes={[]}
      addHidden={jest.fn()}
      removeHidden={jest.fn()}
    />
  )
})

/** Group of tests that check visual aspects */
describe('Button display', () => {
  /** Check if the number of rendered buttons match the number of types to be filtered */
  it('shows the correct number of buttons', () => {
    //render with a list containing 6 types
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

    //Check that the card has 6 buttons as children
    const children = getAllByTestId(card, 'filterButton')
    expect(children.length).toBe(6)
  })

  /** Check if the button displays the name of what it filters */
  test('shows the correct type name on the buttons', () => {
    //Types to render and check that they exist
    const t1 = 'car'
    const t2 = 'person'
    const t3 = 'bike'

    render(
      <ObjectTypeFilter
        objectTypes={[
          [t1, false],
          [t2, false],
          [t3, false]
        ]}
        addHidden={jest.fn()}
        removeHidden={jest.fn()}
      />
    )

    //Check if the 3 types passed in the render show up
    expect(screen.queryByText(t1)).not.toBe(null)
    expect(screen.queryByText(t2)).not.toBe(null)
    expect(screen.queryByText(t3)).not.toBe(null)
    //Throw in some random types that weren't passed in render, they shouldn't exist
    expect(screen.queryByText('truck')).toBe(null)
    expect(screen.queryByText('elephant')).toBe(null)
  })
})

/** Collection of tests that check for button clicking functionality */
describe('Button clicking tests', () => {
  //Mock functions to pass to the rendered element
  const mockAdd = jest.fn()
  const mockRemove = jest.fn()

  it('calls addHidden function correctly', () => {
    render(
      <ObjectTypeFilter
        objectTypes={[['type', true]]} //type being true calls addHidden on click
        addHidden={mockAdd}
        removeHidden={mockRemove}
      />
    )

    //simulate a click
    screen.getByTestId('filterButton').click()

    //Ensure the add was called and the remove wasn't
    expect(mockAdd).toBeCalled
    expect(mockRemove).not.toBeCalled

    //reset for next test
    mockAdd.mockReset()
    mockRemove.mockReset()
  })

  it('calls removeHidden function correctly', () => {
    render(
      <ObjectTypeFilter
        objectTypes={[['type', false]]} //type being false calls removeHidden on click
        addHidden={mockAdd}
        removeHidden={mockRemove}
      />
    )

    //simulate a click
    screen.getByTestId('filterButton').click()

    //Ensure the remove was called and the add wasn't
    expect(mockAdd).not.toBeCalled
    expect(mockRemove).toBeCalled
  })
})
