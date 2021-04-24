/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { Component } from 'react'
import { Box } from '../classes/clientMessage'

import { Overlay } from '../components/overlay'
import { indicator } from '../pages/home'

export type source = { id: string, name: string, srcObject: { src: string, type: string } }
export type gridProps = { mainSourceId: Map<string, number>, sources: source[], indicator: indicator }
type gridState = { sourceSize: Map<string, number> }
export class Grid extends Component<gridProps, gridState> {

  constructor(props: gridProps) {
    super(props)
    this.state = { sourceSize: props.mainSourceId }
  }

  componentDidUpdate(oldProps: gridProps) {
    if (oldProps.mainSourceId !== this.props.mainSourceId) this.setState({ sourceSize: this.props.mainSourceId })
  }

  setSize(sourceId: string, size: number) {
    this.setState({ sourceSize: new Map(this.state.sourceSize.set(sourceId, size)) })
  }

  render() {
    return <div style={{
      width: '100%', height: '100%', padding: '5px',
      display: 'grid', gap: '5px',
      gridTemplateColumns: `repeat(auto-fit,minmax(250px, 1fr))`, gridAutoRows: 'minmax(200px, 1fr)'
    }}>
      {
        this.props.sources.map((source) => {
          var size = ((this.state.sourceSize.get(source.id) ?? 1))
          return <div key={source.id} style={{ gridColumn: `span ${size}`, gridRow: `span ${size}`, justifySelf: 'stretch' }}>
            <Overlay
              cameraId={source.id}
              onUp={() => this.setSize(source.id, size + 1)}
              onDown={() => this.setSize(source.id, Math.max(1, size - 1))}
              sources={[source.srcObject]}
              showBoxes={this.props.indicator} />
          </div>
        })
      }
    </div >
  }
}