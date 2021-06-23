/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { screen, render } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { NavMenu } from 'components/navbar'
import {
  MockAuthProvider,
  fakeJWTToken
} from '../utilities/mockAuthContextProvider'

// Render the navbar for each test
beforeEach(() => {
  render(
    <MockAuthProvider state='authenticated' token={fakeJWTToken}>
      <BrowserRouter>
        <NavMenu />
      </BrowserRouter>
    </MockAuthProvider>
  )
})

// Collection of tests that check if all expected components are there
describe('Navbar component checks', () => {
  // The tracktech logo top left of the navbar
  it('Contains the tracktech logo image', () => {
    expect(screen.queryByAltText('logo')).toBeTruthy()
  })

  // The links to the different pages
  it('Contains links to home and timeline', () => {
    expect(screen.queryByText('Home')).toBeTruthy()
    expect(screen.queryByText('Timelines')).toBeTruthy()
  })

  // The login/logout button (in this case logout because of how the mock is set up)
  it('Contains the login/logout button', () => {
    expect(screen.queryByText('Logout')).toBeTruthy()
  })

  // The login info section which shows a message to log in or the username
  it('Contains the login info', () => {
    expect(screen.queryByText('John Doe')).toBeTruthy()
  })
})
