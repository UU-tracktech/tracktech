import { Component } from 'react'
import { Navbar, Nav, Button, Form } from 'react-bootstrap'

export class NavMenu extends Component {

  render() {
    return (
      <header>
        <Navbar bg="primary" variant="dark" expand="lg">
          <Navbar.Brand href="/" >
            Tracktech
           {/*  <img style={{maxHeight: "100px", maxWidth:"100px"}} src={"https://cdn.discordapp.com/attachments/809363612404678657/814798379913314304/a.gif"} alt="logo" /> */}
          </Navbar.Brand>
          <Navbar.Toggle style={{ float: "right" }} aria-controls="basic-navbar-nav" />
          <Navbar.Collapse className="mr-auto">
            <Nav>
              <Nav.Link style={{ padding: "8px 25px" }} color="light" href="/">Home</Nav.Link>
              <Nav.Link style={{ padding: "8px 25px" }} href="/websockets">Websockets</Nav.Link>
              <Nav.Link style={{ padding: "8px 25px" }} href="/Logging">Logging</Nav.Link>
            </Nav>
            <Form inline className="ml-auto">
              <Button onClick={this.onLoginPress}>Login</Button>
            </Form>
          </Navbar.Collapse>
        </Navbar>
      </header>
    )
  }

  onLoginPress() {
    alert('login')
  }
}