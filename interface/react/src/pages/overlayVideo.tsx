import { Component } from 'react'

import { Overlay } from '../components/overlay'

export class OverlayVideo extends Component {
  render() {
    return <Overlay
        cameraId={"test"}
        onButtonClick={() => alert('resize')}
        key={'testvid'}
        autoplay={true}
        controls={true}
        width={300}
        height={300}
        sources={[{ src: 'http://localhost:80/testvid.m3u8' }]}
        showBoxes="All"
    />
  }
}