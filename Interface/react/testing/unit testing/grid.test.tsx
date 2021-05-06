import * as React from 'react'
import { render, screen } from '@testing-library/react'
import { Grid } from '../../src/components/grid'

it('renders without error', () => {
  render(
    <Grid
      primary="0"
      setPrimary={jest.fn}
      sources={[]}
      indicator={'All'}
      hiddenObjectTypes={[]}
    />
  )
})

/** A list containing 3 made up sources to test with */
const mockSources = [
  {
    id: '0',
    name: 'source1',
    srcObject: { src: 'link', type: 'type' }
  },
  {
    id: '1',
    name: 'source2',
    srcObject: { src: 'link', type: 'type' }
  },
  {
    id: '2',
    name: 'source3',
    srcObject: { src: 'link', type: 'type' }
  }
]

it('number of elements match number of sources', () => {
  //temporarily replace the alert function with an empty function
  //This stops an error from appearing after a window.alert call in de overlay component
  //jest/jsdom does not imlement the alert function, therefore throwing an error when it's called
  const jsdomAlert = window.alert //keep a copy to restore it after the test
  window.alert = () => {}

  render(
    <Grid
      primary="0"
      setPrimary={jest.fn}
      sources={mockSources}
      indicator={'All'}
      hiddenObjectTypes={[]}
    />
  )

  //The grid contains an overlay for each VideoPlayer
  //There are 3 sources in the list, so there should be 3 overlays/videoplayers
  expect(screen.queryAllByTestId('gridElement').length).toBe(mockSources.length)

  //restore the alert function
  window.alert = jsdomAlert
})

/** Test to check the setPrimary function changes which video becomes primary */
it.todo('Calls the setPrimary function')
//Not sure how to test this.
//The function gets called either from the video control bar or the cameracard
//cameracard is not rendered so cant use that
//the controlbar does not load until the player is playing
//players wont play/load bar because sources are not valid videos
//maybe it needs some async logic with an actual video link in the sources?
