import React, { Component } from 'react'
import VideoPlayer from '../components/VideojsPlayer'
import { Container, Col, Row, ButtonGroup, Button } from 'react-bootstrap'

type indicator = 'All' | 'Selection' | 'None'
type homeState = { sources: any[], currentIndicator: indicator }
export class Home extends Component<{}, homeState> {

  constructor(props: any) {
    super(props)
    this.state = { sources: [], currentIndicator: 'All' }
  }

  async componentDidMount() {
    var config = await (await fetch(process.env.PUBLIC_URL + '/config.json')).json()
    this.setState({
      sources: config.map((stream) => ({
        name: stream.Name,
        srcObject: {
          src: stream.Forwarder,
          type: stream.Type
        }
      }))
    })
  }

  render() {
    return (
      <Container fluid className='fill-height' style={{ height: '100%' }}>
        <Row className='fill-height' style={{ height: '100%' }}>
          <Col lg={3} className='border-right'>
            <Container className='bg-secondary text-white' style={{ marginTop: '10px', padding: '5px', borderRadius: "5px" }}>
              <h2>Indicators</h2>
              <ButtonGroup>
                <Button variant={this.state.currentIndicator === 'All' ? 'secondary' : 'light'} onClick={() => this.indicatorAll()}>All</Button>
                <Button variant={this.state.currentIndicator === 'Selection' ? 'secondary' : 'light'} onClick={() => this.indicatorSelection()}>Selection</Button>
                <Button variant={this.state.currentIndicator === 'None' ? 'secondary' : 'light'} onClick={() => this.indicatorNone()}>None</Button>
              </ButtonGroup>
            </Container>
          </Col>
          <Col lg={9}>
            {
              this.state.sources && this.state.sources.map((source) =>
                <Row>
                  <h1>{source.name}</h1>
                  <VideoPlayer key={source.name} autoplay={true} controls={true} sources={[source.srcObject]} />
                </Row>)
            }
          </Col>
        </Row>
      </Container>
    )
  }

  indicatorAll() {
    this.setState({ currentIndicator: 'All' })
  }

  indicatorSelection() {
    this.setState({ currentIndicator: 'Selection' })
  }

  indicatorNone() {
    this.setState({ currentIndicator: 'None' })
  }
}