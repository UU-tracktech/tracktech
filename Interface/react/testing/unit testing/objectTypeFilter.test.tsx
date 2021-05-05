import * as React from 'react'
import { screen, render } from '@testing-library/react'
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

test.todo('the number of buttons correspond to the number of object types')

describe('Button clicking tests', () => {
  it.todo('changes appearance on click')

  it.todo('calls addHidden function correctly')

  it.todo('calls removeHidden function correctly')
})
