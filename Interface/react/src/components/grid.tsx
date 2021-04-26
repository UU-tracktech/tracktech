/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Overlay } from '../components/overlay'
import { indicator } from '../pages/home'

export type source = { id: string, name: string, srcObject: { src: string, type: string } }
export type gridProps = { sourceSizes: Map<string, number>, setSize: (sourceId: string, size: number) => void, sources: source[], indicator: indicator }

export function Grid(props: gridProps) {
  return <div style={{
    width: '100%', height: '100%', padding: '5px',
    display: 'grid', gap: '5px',
    gridTemplateColumns: `repeat(auto-fit,minmax(250px, 1fr))`, gridAutoRows: 'minmax(200px, 1fr)'
  }}>
    {
      props.sources.map((source) => {
        var size = props.sourceSizes.get(source.id) ?? 1
        return <div key={source.id} style={{ gridColumn: `span ${size}`, gridRow: `span ${size}`, justifySelf: 'stretch' }}>
          <Overlay
            cameraId={source.id}
            onUp={() => props.setSize(source.id, (props.sourceSizes.get(source.id) ?? 1) + 1)}
            onDown={() => props.setSize(source.id, Math.max(1, (props.sourceSizes.get(source.id) ?? 1) - 1))}
            sources={[source.srcObject]}
            showBoxes={props.indicator} />
        </div>
      })
    }
  </div >
}
