import { Component } from 'react'

import { Overlay } from '../components/overlay'

export class OverlayVideo extends Component {
  render() {
    return <Overlay cameraId={0} onBoxClick={(id) => alert(id)} onButtonClick={() => alert('resize')} key={'testvid'} autoplay={true} controls={true} width={300} height={300} sources={[{ src: 'http://sample.vodobox.com/big_buck_bunny_4k/big_buck_bunny_4k.m3u8' }]} />
  }
}