/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Button, Card } from 'antd'
import { Layout } from 'antd'

import { Grid, source } from '../components/grid'

export type indicator = 'All' | 'Selection' | 'None'
type tracked = { id: number, name: string, image: string, data: string }
export function Home() {
  const [sources, setSources] = React.useState<source[]>()
  const [currentIndicator, setCurrentIndicator] = React.useState<indicator>('All')
  const [tracking, setTracking] = React.useState<tracked[]>([])
  const [primary, setPrimary] = React.useState<string>()

  const selectionRef = React.useRef(0)

  React.useEffect(() => {
    fetch(process.env.PUBLIC_URL + '/config.json').then((text) =>
      text.json().then((json) => {
        var nexId = 0
        setSources(json.map((stream) => ({
          id: nexId++,
          name: stream.Name,
          srcObject: {
            src: stream.Forwarder,
            type: stream.Type
          }
        })))
      }))
  }, [])

  return (
    <Layout.Content style={{ display: 'grid', gridTemplateColumns: '1fr 4fr', gridAutoRows: '100%', overflow: 'hidden' }}>
      <div style={{ padding: '5px', overflowY: 'auto', display: 'grid', gap: '5px' }}>
        <Card>
          <h2>Indicators</h2>
          <Button type={currentIndicator === 'All' ? 'primary' : 'default'} onClick={() => setCurrentIndicator('All')}>All</Button>
          <Button type={currentIndicator === 'Selection' ? 'primary' : 'default'} onClick={() => setCurrentIndicator('Selection')}>Selection</Button>
          <Button type={currentIndicator === 'None' ? 'primary' : 'default'} onClick={() => setCurrentIndicator('None')}>None</Button>
        </Card>
        <Card>
          <div>
            <h2>Selection</h2>
            <Button onClick={async () => await addSelection()}>+</Button>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gridAutoRows: '100px' }}>
            {
              tracking && tracking.map((tracked) =>
                <img alt='tracked person' onClick={() => removeSelection(tracked.id)} style={{ width: '100%', height: '100%', margin: '5px' }} src={tracked.image} />
              )
            }
          </div>
        </Card>

        <Card>
          <h2>Cameras</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))' }}>
            {
              sources && sources.map((source) =>
                <Card key={source.id} title={source.name}>
                  <Button type='primary' onClick={() => setPrimary(source.id)}>View</Button>
                </Card>
              )
            }
          </div>
        </Card>
      </div>

      <div style={{ overflowY: 'auto' }}>
        {sources && <Grid
          sources={sources}
          primary={primary ?? sources[0]?.id}
          setPrimary={(sourceId: string) => setPrimary(sourceId)}
          indicator={currentIndicator} />}
      </div>
    </Layout.Content>)

  async function addSelection() {
    const pictures = ['car', 'guy', 'garden']
    const picture = pictures[Math.floor(Math.random() * pictures.length)]

    var result = await fetch(process.env.PUBLIC_URL + `/${picture}.png`)
    var blob = await result.blob()
    var reader = new FileReader()
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        setTracking(tracking.concat({ id: selectionRef.current++, name: 'abc', image: reader.result, data: '' }))
      }
    }
    reader.readAsDataURL(blob)
  }

  function removeSelection(id: number) {
    setTracking(tracking.filter(tracked => tracked.id !== id))
  }
}