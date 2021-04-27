/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Menu, Layout } from 'antd'
import { Link } from 'react-router-dom'

import { LoginButton } from './loginButton'
import { LoggedInUser } from './loggedInUser'

export function NavMenu() {

  return (
    <Layout.Header style={{ background: '#fff', width: '100%', height: '66px', paddingLeft: '10px', paddingRight: '10px' }}>
      <div style={{ display: 'grid', width: '100px', height: '64px', overflow: 'hide', alignContent: 'center', float: 'left' }}>
        <img style={{ maxHeight: '100px', maxWidth: '100px' }} src={'https://cdn.discordapp.com/attachments/809363612404678657/814798379913314304/a.gif'} alt='logo' />
      </div>
      <div style={{ float: 'right' }}>
        <LoginButton />
      </div>
      <div style={{ float: 'right', marginRight: '10px' }}>
        <LoggedInUser />
      </div>
      <Menu mode="horizontal" >
        {/*  <Navbar.Brand as={Link} to='/' >
         
        </Navbar.Brand> */}
        {/* <Navbar.Toggle style={{ float: 'right' }} aria-controls='basic-navbar-nav' /> */}

        <Menu.Item>
          <Link to="/" >
            Home
          </Link>
        </Menu.Item>
        <Menu.Item>
          <Link to="/websockets" >
            Websockets
          </Link>
        </Menu.Item>
        <Menu.Item>
          <Link to="/Overlay" >
            Overlay
          </Link>
        </Menu.Item>
      </Menu>
    </ Layout.Header>
  )
}