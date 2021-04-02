import { Component } from 'react'
import { Navbar, Nav, Button, Form } from 'react-bootstrap'
import { Link } from 'react-router-dom'

import LoginButton from './LoginButton'

export class NavMenu extends Component {

  render() {
    return (
      <header>
        <Navbar bg="primary" variant="dark" expand="lg">
          <Navbar.Brand as={Link} to="/" >
            Tracktech
           {/*  <img style={{maxHeight: "100px", maxWidth:"100px"}} src={"https://cdn.discordapp.com/attachments/809363612404678657/814798379913314304/a.gif"} alt="logo" /> */}
          </Navbar.Brand>
          <Navbar.Toggle style={{ float: "right" }} aria-controls="basic-navbar-nav" />
          <Navbar.Collapse className="mr-auto">
            <Nav>
              <Nav.Link as={Link} style={{ padding: "8px 25px" }} color="light" to="/">Home</Nav.Link>
              <Nav.Link as={Link} style={{ padding: "8px 25px" }} to="/websockets">Websockets</Nav.Link>
              <Nav.Link as={Link} style={{ padding: "8px 25px" }} to="/Canvas">Canvas</Nav.Link>
            </Nav>
            <Form inline className="ml-auto">
              <LoginButton />
            </Form>
          </Navbar.Collapse>
        </Navbar>
      </header>
    )
  }
}