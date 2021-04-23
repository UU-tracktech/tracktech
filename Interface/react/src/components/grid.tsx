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
export type gridProps = { mainSourceId?: string, sources: source[], indicator: indicator }
type gridState = { mainSourceId?: string }
export class Grid extends Component<gridProps, gridState> {

  constructor(props: gridProps) {
    super(props)
    this.state = { mainSourceId: props.mainSourceId }
  }

  componentDidUpdate(oldProps: gridProps) {
    if (oldProps.mainSourceId !== this.props.mainSourceId) this.viewSource(this.props.mainSourceId)
  }

  viewSource(sourceId?: string) {
    this.setState({ mainSourceId: this.state.mainSourceId === sourceId ? undefined : sourceId })
  }

  render() {
    return <div style={{
      width: '100%', height: '100%', padding: 0,
      display: 'grid', gridTemplateColumns: `repeat(${Math.round(Math.sqrt(this.props.sources.length))}, 1fr)`, gridAutoRows: '1fr'
    }}>
      {
        this.props.sources.map((source) => {
          return <div key={source.id} style={{ ...(this.state.mainSourceId === source.id ? { gridRowStart: 1, gridRowEnd: 3, gridColumnStart: 1, gridColumnEnd: -1 } : {}), justifySelf: 'stretch' }}>
            <Overlay 
              cameraId={source.id} 
              onButtonClick={() => this.viewSource(source.id)} 
              sources={[source.srcObject]}
              showBoxes={this.props.indicator} />
          </div>
        })
      }
    </div >
  }
}