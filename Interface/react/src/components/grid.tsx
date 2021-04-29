/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Overlay } from './overlay'
import { indicator } from '../pages/home'

export type source = { id: string, name: string, srcObject: { src: string, type: string } }
export type gridProps = { primary?: string, setPrimary: (sourceId: string) => void, sources: source[], indicator: indicator }

export function Grid(props: gridProps) {
  return <div style={{
    width: '100%', height: '100%', padding: '5px',
    display: 'grid', gap: '5px',
    gridTemplateColumns: `repeat(auto-fit,minmax(30%, 1fr))`, gridTemplateRows: '60%', gridAutoRows: 'minmax(30%, 1fr)'
  }}>
    {
      props.sources.map((source) => {
        return <div key={source.id} style={
          props.primary === source.id
          ? { gridRowStart: 1, gridColumnStart: 1, gridColumnEnd: -1 }
          : { justifySelf: 'stretch' }}>
          <Overlay
            cameraId={source.srcObject.src}
            onPrimary={() => props.setPrimary(source.id)}
            onPlayPause={() => { }}
            onTimestamp={() => { }}
            sources={[source.srcObject]}
            showBoxes={props.indicator} />
        </div>
      })
    }
  </div >
}
