/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { act, render, screen } from '@testing-library/react'
import { App } from '../../src/app'

let mockAuthenticated = false

jest.mock('@react-keycloak/web', () => {
  return {
    useKeycloak: () => ({
      keycloak: {
        authenticated: mockAuthenticated
      }
    })
  }
})

test('App renders without errors', async () => {
  await act(async () => {
    render(<App />)
  })
})

test('shows login notification if not authenticated', async () => {
  await act(async () => {
    render(<App />)
  })

  expect(screen.queryByTestId('loginAlert')).not.toBe(null)
})

test('shows home if authenticated', async () => {
  mockAuthenticated = true

  await act(async () => {
    render(<App />)
  })

  expect(screen.queryByTestId('loginAlert')).toBe(null)
})
