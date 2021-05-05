import * as React from 'react'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { Home } from '../../src/pages/home'
import '@testing-library/jest-dom'
import { act } from 'react-dom/test-utils'

test('The card containing the buttons is there', async () => {
  //We need to wait because otherwise there will be errors about updates still happening
  await act(async () => {
    render(<Home />)
  })

  expect(screen.queryByTestId('SelectionCard')).not.toBe(null)
})

test('The buttons are there', async () => {
  //We need to wait because otherwise there will be errors about updates still happening
  await act(async () => {
    render(<Home />)
  })

  const card = screen.queryByTestId('SelectionCard')
  expect(card).not.toBe(null)

  const allBut = screen.queryByTestId('AllButton')
  expect(allBut).not.toBe(null)

  const selBut = screen.queryByTestId('SelectionButton')
  expect(selBut).not.toBe(null)

  const noneBut = screen.queryByTestId('NoneButton')
  expect(noneBut).not.toBe(null)

  expect(card).toContainElement(allBut)
  expect(card).toContainElement(selBut)
  expect(card).toContainElement(noneBut)
})

test('Clicking buttons changes selection', async () => {
  //We need to wait because otherwise there will be errors about updates still happening
  await act(async () => {
    render(<Home />)
  })

  const allBut = screen.getByTestId('AllButton')
  const selBut = screen.getByTestId('SelectionButton')
  const noneBut = screen.getByTestId('NoneButton')

  //by default, the 'all' button is primary, and the others are default
  expect(allBut).toHaveClass('ant-btn-primary')
  expect(allBut).not.toHaveClass('ant-btn-default')
  expect(selBut).not.toHaveClass('ant-btn-primary')
  expect(selBut).toHaveClass('ant-btn-default')
  expect(noneBut).not.toHaveClass('ant-btn-primary')
  expect(noneBut).toHaveClass('ant-btn-default')

  //Simulate a click on the selection button
  fireEvent.click(selBut)
  //Now the All button should be back to default and selection should be primary
  expect(allBut).not.toHaveClass('ant-btn-primary')
  expect(allBut).toHaveClass('ant-btn-default')
  expect(selBut).toHaveClass('ant-btn-primary')
  expect(selBut).not.toHaveClass('ant-btn-default')
  expect(noneBut).not.toHaveClass('ant-btn-primary')
  expect(noneBut).toHaveClass('ant-btn-default')

  //again but now for the none button
  fireEvent.click(noneBut)
  expect(allBut).not.toHaveClass('ant-btn-primary')
  expect(allBut).toHaveClass('ant-btn-default')
  expect(selBut).not.toHaveClass('ant-btn-primary')
  expect(selBut).toHaveClass('ant-btn-default')
  expect(noneBut).toHaveClass('ant-btn-primary')
  expect(noneBut).not.toHaveClass('ant-btn-default')
})
