/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
  The grid component creates a videoplayer and overlay for drawing on that player
  for each camera source defined in the config file, which are passed in through the props
*/

import React from 'react'

import { Overlay } from './overlay'
import { indicator } from '../pages/home'
import { source } from '../classes/source'

/**
 * Properties of the grid component
 * Contains which stream is the primary stream, displayed large at the top,
 * contains a list of all video streams to display and which boundingboxes/indicators to draw
 */
export type gridProps = {
  primary?: string
  setPrimary: (sourceId: string) => void
  sources: source[]
  indicator: indicator
  hiddenObjectTypes: string[]
}

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
        //The map goes through every source and creates an overlay component,
        //which includes the video player
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
              onPlayPause={() => {}}
              onTimestamp={() => {}}
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
