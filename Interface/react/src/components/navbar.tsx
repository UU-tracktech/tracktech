/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
  This component shows the navigation bar at the top of the page  
*/

import React from 'react'
import { Menu, Layout } from 'antd'
import { Link } from 'react-router-dom'

import { LoginButton } from './loginButton'
import { LoggedInUser } from './loggedInUser'

export function NavMenu() {
  return (
    <Layout.Header
      //Navbar styling
      style={{
        background: '#fff',
        width: '100%',
        height: '66px',
        paddingLeft: '10px',
        paddingRight: '10px',
        zIndex: 10
      }}
    >
      <div
        //Tracktech image logo styling
        style={{
          display: 'grid',
          width: '100px',
          height: '64px',
          overflow: 'hide',
          alignContent: 'center',
          float: 'left'
        }}
      >
        <img
          //The Tracktech logo at the left of the navbar
          style={{ maxHeight: '100px', maxWidth: '100px' }}
          src={
            'https://cdn.discordapp.com/attachments/809363612404678657/814798379913314304/a.gif'
          }
          alt="logo"
        />
      </div>
      {/* The login buttons on the right of the navbar. Has to come before the pages to not break styling */}
      <div style={{ float: 'right' }}>
        <LoginButton />
      </div>
      <div style={{ float: 'right', marginRight: '10px' }}>
        <LoggedInUser />
      </div>
      {/* Links to the pages in the navbar */}
      <Menu mode="horizontal" style={{ borderBottom: '3px solid #096dd9' }}>
        <Menu.Item style={{ borderBottom: '0px' }}>
          <Link to="/">Home</Link>
        </Menu.Item>
      </Menu>
    </Layout.Header>
  )
}
