import React, { Component } from 'react'
import VideoPlayer from '../components/VideojsPlayer'
import { Container, Col, Row, ButtonGroup, Button, Card, OverlayTrigger, Popover } from 'react-bootstrap'

type indicator = 'All' | 'Selection' | 'None'
type source = { id: number, name: string, srcObject: { src: string, type: string } }
type tracked = { id: number, name: string, image: string, data: string }
type homeState = { sources: source[], currentIndicator: indicator, tracking: tracked[], currentSource?: number }
export class Home extends Component<{}, homeState> {

  constructor(props: any) {
    super(props)
    this.state = { sources: [], currentIndicator: 'All', tracking: [] }
  }

  async componentDidMount() {
    var config = await (await fetch(process.env.PUBLIC_URL + '/config.json')).json()
    var nexId = 0
    this.setState({
      sources: config.map((stream) => ({
        id: nexId++,
        name: stream.Name,
        srcObject: {
          src: stream.Forwarder,
          type: stream.Type
        }
      }))
    })
  }


  render() {
    const boxStyle = { margin: '10px', padding: '5px', borderRadius: "5px", borderStyle: "outset" }
    const colStyle = { padding: '0px' }
    const bigSize = { width: 500, height: 400 }
    const smallSize = { width: 300, height: 200 }

    var mainSource = this.state.sources.find((source) => source.id === this.state.currentSource)
    var otherSources = this.state.sources.filter((source) => source.id !== this.state.currentSource)

    return (
      <Container fluid className='fill-height' style={{ height: '100%' }}>
        <Row className='fill-height' style={{ height: '100%' }}>
          <Col lg={2} className='border-right' style={colStyle}>
            <Row style={boxStyle}>
              <Container>
                <h2>Indicators</h2>
                <ButtonGroup>
                  <Button variant={this.state.currentIndicator === 'All' ? 'secondary' : 'light'} onClick={() => this.indicatorAll()}>All</Button>
                  <Button variant={this.state.currentIndicator === 'Selection' ? 'secondary' : 'light'} onClick={() => this.indicatorSelection()}>Selection</Button>
                  <Button variant={this.state.currentIndicator === 'None' ? 'secondary' : 'light'} onClick={() => this.indicatorNone()}>None</Button>
                </ButtonGroup>
              </Container>
            </Row>
            <Row style={boxStyle}>
              <Container>
                <h2>Cameras</h2>
                {
                  this.state.sources && this.state.sources.map((source) =>
                    <Card>
                      <Card.Body>
                        <Card.Title>{source.name}</Card.Title>
                        <Button variant="primary" onClick={() => this.viewSource(source)}>View</Button>
                      </Card.Body>
                    </Card>)
                }
              </Container>
            </Row>
            <Row style={boxStyle}>
              <Container>
                <Row className="d-flex justify-content-between">
                  <h2>Selection</h2>
                  <Button onClick={async () => await this.addSelection()}>+</Button>
                </Row>
                {
                  this.state.tracking && this.state.tracking.map((tracked) =>
                    <img alt="tracked person" onClick={() => this.removeSelection(tracked.id)} style={{ width: "75px", height: "75px", margin: "5px" }} src={tracked.image} />
                  )
                }
              </Container>
            </Row>
          </Col>
          <Col lg={10} style={colStyle}>

            <Row className="d-flex justify-content-center" style={{ margin: "5px", width: "100%" }}>
              {
                mainSource
                  ? <VideoPlayer key={mainSource.name} autoplay={true} controls={true} {...bigSize} sources={[mainSource.srcObject]} />
                  : <div style={{ width: `${bigSize.width}px`, height: `${bigSize.height}px` }}>please select video on the left hand side</div>
              }
            </Row>

            <Row className="d-flex justify-content-center" style={{ margin: "5px", width: "100%" }}>
              {
                otherSources.map((source) => <VideoPlayer key={source.name} autoplay={true} controls={true} {...smallSize} sources={[source.srcObject]} />)
              }
            </Row>
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

  private number = 0
  async addSelection() {
    const pictures = ["car", "guy", "garden"];
    const picture = pictures[Math.floor(Math.random() * pictures.length)];

    var result = await fetch(process.env.PUBLIC_URL + `/${picture}.png`)
    var blob = await result.blob()
    var reader = new FileReader()
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        console.log(reader.result)
        this.setState({ tracking: this.state.tracking.concat({ id: this.number++, name: "abc", image: reader.result, data: "" }) })
      }
    }
    reader.readAsDataURL(blob)
  }

  viewSource(source: source) {
    this.setState({ currentSource: source.id })
  }

  removeSelection(id: number) {
    this.setState({ tracking: this.state.tracking.filter(tracked => tracked.id !== id) })
  }
}