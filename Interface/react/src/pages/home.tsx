/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Component } from 'react'
import { ButtonGroup, Button, Card } from 'react-bootstrap'

import { Grid, source } from '../components/grid'

export type indicator = 'All' | 'Selection' | 'None'
type tracked = { id: number, name: string, image: string, data: string }
type homeState = { sources: source[], currentIndicator: indicator, tracking: tracked[], mainSourceId?: string }
export class Home extends Component<{}, homeState> {

  constructor(props: any) {
    super(props)
    this.state = { sources: [], currentIndicator: 'All', tracking: [] }
  }

  async componentDidMount() {
    console.log(await fetch(process.env.PUBLIC_URL + '/config.json'))
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

  viewSource(sourceId: string) {
    this.setState({ mainSourceId: sourceId })
  }

  render() {
    return (
      <div style={{ display: "grid", gridTemplateColumns: "1fr 4fr", gridAutoRows: "100%", overflow: 'hidden' }}>
        <div style={{ padding: '5px', overflowY: "auto", display: "grid", gap: '5px' }}>
          <Card>
            <h2>Indicators</h2>
            <ButtonGroup>
              <Button variant={this.state.currentIndicator === 'All' ? 'secondary' : 'light'} onClick={() => this.indicatorAll()}>All</Button>
              <Button variant={this.state.currentIndicator === 'Selection' ? 'secondary' : 'light'} onClick={() => this.indicatorSelection()}>Selection</Button>
              <Button variant={this.state.currentIndicator === 'None' ? 'secondary' : 'light'} onClick={() => this.indicatorNone()}>None</Button>
            </ButtonGroup>
          </Card>
          <Card>
            <div>
              <h2>Selection</h2>
              <Button onClick={async () => await this.addSelection()}>+</Button>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(100px, 1fr))", gridAutoRows: '100px' }}>
              {
                this.state.tracking && this.state.tracking.map((tracked) =>
                  <img alt="tracked person" onClick={() => this.removeSelection(tracked.id)} style={{ width: "100%", height: "100%", margin: "5px" }} src={tracked.image} />
                )
              }
            </div>
          </Card>

          <Card>
            <h2>Cameras</h2>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(100px, 1fr))" }}>
              {
                this.state.sources && this.state.sources.map((source) =>
                  <Card key={source.id}>
                    <Card.Body>
                      <Card.Title>{source.name}</Card.Title>
                      <Button variant="primary" onClick={() => this.viewSource(source.id)}>View</Button>
                    </Card.Body>
                  </Card>
                )
              }
            </div>
          </Card>
        </div>

        <div style={{ overflowY: "auto" }}>
          <Grid
            sources={this.state.sources}
            mainSourceId={new Map().set(this.state.mainSourceId, 3)}
            indicator={this.state.currentIndicator} />
        </div>
      </div>
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
    const pictures = ["car", "guy", "garden"]
    const picture = pictures[Math.floor(Math.random() * pictures.length)]

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

  removeSelection(id: number) {
    this.setState({ tracking: this.state.tracking.filter(tracked => tracked.id !== id) })
  }
}