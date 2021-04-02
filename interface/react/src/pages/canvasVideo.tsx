import { Component } from 'react'

import { VideoPlayer } from '../components/VideojsPlayer'
import { Canvas } from '../components/canvas'

export class CanvasVideo extends Component {
  render() {
    return <Canvas cameraId={0} width={300} height={270} onClickCallback={(id) => alert(id)}>
      < VideoPlayer onClick={() => alert('resize')} key={'testvid'} autoplay={true} controls={true} width={300} height={300} sources={[{ src: 'http://sample.vodobox.com/big_buck_bunny_4k/big_buck_bunny_4k.m3u8' }]} />
    </Canvas>
  }
}