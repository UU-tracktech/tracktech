/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'

import { Overlay, stream } from 'components/overlay'
import { indicator } from 'pages/home'

/**
 * Properties of the grid component.
 * Contains which stream is the primary stream, displayed large at the top,
 * contains a list of all video streams to display, and which boundingboxes/indicators to draw.
 */
export type gridProps = {
  primary?: string
  setPrimary: (sourceId: string) => void
  sources: stream[]
  indicator: indicator
  hiddenObjectTypes: string[]
}

/**
 * Component that creates a videoplayer and overlay for drawing on that player
 * for each camera source defined in the config file.
 * @param props Properties containing streams and filters.
 * @returns A grid of camera streams with corresponding overlay.
 */
export function Grid(props: gridProps) {
  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'grid',
        padding: '5px',
        gap: '5px',
        gridTemplateColumns: `repeat(auto-fit,minmax(30%, 1fr))`,
        gridTemplateRows: '60%',
        gridAutoRows: 'minmax(30%, 1fr)'
      }}
    >
      {props.sources.map((source) => {
        // The map goes through every source and creates an overlay component, which includes the video player.
        return (
          <div
            data-testid={'gridElement'}
            key={source.id}
            style={
              props.primary === source.id
                ? { gridRowStart: 1, gridColumnStart: 1, gridColumnEnd: -1 }
                : { justifySelf: 'stretch' }
            }
          >
            <Overlay
              source={source}
              onPrimary={() => props.setPrimary(source.id)}
              sources={[source.srcObject]}
              showBoxes={props.indicator}
              hiddenObjectTypes={props.hiddenObjectTypes}
              autoplay={process.env.NODE_ENV === 'production'}
            />
          </div>
        )
      })}
    </div>
  )
}
