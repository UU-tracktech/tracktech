/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Menu, Layout } from 'antd'
import { Link } from 'react-router-dom'

import { LoginButton } from 'components/loginButton'
import { LoggedInUser } from 'components/loggedInUser'

/**
 * Navigation bar at the top of the page.
 * @returns The antd Navbar containing a logo, page navigation, and login info.
 */
export function NavMenu() {
  return (
    <Layout.Header
      // Navbar styling.
      style={{
        background: '#fff',
        paddingLeft: '10px',
        paddingRight: '10px',
        zIndex: 10,
        display: 'grid',
        gridTemplateColumns: 'auto auto 1fr auto auto',
        gridTemplateRows: '66px',
        alignContent: 'center',
        columnGap: '10px'
      }}
    >
      <img
        // The Tracktech logo at the left of the navbar.
        style={{ maxHeight: '100px', maxWidth: '100px', alignSelf: 'center' }}
        src={process.env.PUBLIC_URL + '/logo.gif'}
        alt={'logo'}
      />
      {/* Links to the pages in the navbar. */}
      <Menu mode={'horizontal'}>
        <Menu.Item>
          <Link to={'/'}>Home</Link>
        </Menu.Item>
        <Menu.Item style={{ borderBottom: '0px' }}>
          <Link to='/timelines'>Timelines</Link>
        </Menu.Item>
      </Menu>

      {/* The login buttons on the right of the navbar. Has to come before the pages to not break styling. */}
      <div style={{ gridColumnStart: '4' }}>
        <LoggedInUser />
      </div>
      <div style={{ gridColumnStart: '5' }}>
        <LoginButton />
      </div>
    </Layout.Header>
  )
}
