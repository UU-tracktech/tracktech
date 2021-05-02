/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import { App } from '../src/app'
import fetchMock from 'jest-fetch-mock'

jest.mock('@react-keycloak/web', () => {
  const originalModule = jest.requireActual('@react-keycloak/web')
  return {
    ...originalModule,
    useKeycloak: () => ({
      keycloak: { authenticated: false, login: () => {}, logout: () => {} },
      initialized: false
    })
  }
})

test('App renders', async () => {
  fetch('www.google.com')
  render(<App />)
})
