import { Component } from 'react'

import { Overlay } from '../components/overlay'

export type source = { id: number, name: string, srcObject: { src: string, type: string } }
export type gridProps = { mainSourceId?: number, sources: source[] }
type gridState = { mainSourceId?: number }
export class Grid extends Component<gridProps, gridState> {

  constructor(props: gridProps) {
    super(props)
    this.state = { mainSourceId: props.mainSourceId }
  }

  componentDidUpdate(oldProps: gridProps) {
    if (oldProps.mainSourceId !== this.props.mainSourceId) this.viewSource(this.props.mainSourceId)
  }

  viewSource(sourceId?: number) {
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
            <Overlay onBoxClick={(id) => alert(id)} cameraId={source.id} onButtonClick={() => this.viewSource(source.id)} sources={[source.srcObject]} />
          </div>
        })
      }
    </div >
  }
}