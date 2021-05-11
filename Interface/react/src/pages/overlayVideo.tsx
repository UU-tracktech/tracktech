/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/*
OverlayVideo is a page containing a single video player with an overlay for drawing
objects on top of it. Mainly used to debug anything todo with the videoplayer or overlay
*/

import React from 'react'
import { Overlay } from '../components/overlay'

export function OverlayVideo() {
  return (
    <div style={{ display: 'grid', height: '100%', width: '100%' }}>
      <Overlay
        cameraId={'test'}
        onPrimary={() => alert('on primary')}
        onPlayPause={() => {}}
        onTimestamp={() => {}}
        key={'testvid'}
        autoplay={true}
        controls={true}
        width={300}
        height={300}
        sources={[{ src: 'http://localhost:80/testvid.m3u8' }]}
        showBoxes="All"
        hiddenObjectTypes={[]}
      />
    </div>
  )
}
