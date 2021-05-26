/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/*
  This page contains timelines showing when objects where detected over time.
*/

import React from 'react'
import { Layout, Card, Timeline, Divider } from 'antd'
import { Typography } from 'antd'

import { ObjectCard } from '../components/objectCard'
import { TimelineCard } from '../components/timelineCard'
import { TimelineData, dateRange } from '../classes/timelineData'

const { Title } = Typography

export function Timelines() {
  /** State containing all the tracked objects */
  const [objects, setObjects] = React.useState<number[]>([])
  /** State containing the currently selected item */
  const [currentObject, setCurrentObject] = React.useState<string>(
    'Tracking timelines'
  )
  /** State containing the events of the currently selected item, which is null if no data is available */
  const [
    timelineEvents,
    setTimeLineEvents
  ] = React.useState<TimelineData | null>(new TimelineData([]))

  React.useEffect(() => {
    //Get all the tracked objects from the server and display them
    fetch('https://tracktech.ml:50011/objectIds').then((text) =>
      text.json().then((json) => {
        setObjects(json.data)
      })
    )
  }, [])

  var timelines: JSX.Element[] = []

  //Create the timeline of there is data
  if (timelineEvents != null) {
    var events = timelineEvents.GetImportantEvents()
    for (let cameraId in events) {
      let range: dateRange[] = events[cameraId]
      timelines.push(
        <TimelineCard cameraId={cameraId}>
          <Timeline style={{ padding: '10px' }}>
            {createTimelineItems(cameraId, range)}
          </Timeline>
        </TimelineCard>
      )
    }
    // Otherwise show a message explaining there is no data
  } else {
    timelines.push(
      <p style={{ paddingLeft: 10 }}>No tracking data available.</p>
    )
  }

  return (
    //Main content of the page
    <Layout.Content
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr 4fr',
        gridAutoRows: '100%',
        overflow: 'hidden'
      }}
    >
      <div
        style={{
          padding: '5px',
          overflowY: 'auto',
          display: 'grid',
          gap: '5px'
        }}
      >
        <Card
          //This card contains the objects have been or are being tracked
          bodyStyle={{ padding: '4px' }}
          headStyle={{ padding: 0 }}
          size="small"
          title={
            <h2 style={{ margin: '0px 8px', fontSize: '20px' }}>
              Tracked Objects
            </h2>
          }
        >
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
              gridAutoRows: '100px'
            }}
          >
            {/* Map the objects to cards */}
            {objects.map((objectId) => {
              return (
                <ObjectCard
                  key={objectId}
                  id={objectId}
                  viewCallback={(id: number) => setTimeline(id)}
                />
              )
            })}
          </div>
        </Card>
      </div>

      <div
        style={{ overflowY: 'auto', backgroundColor: 'white', margin: '5px' }}
      >
        {/*Show the currently selected object data */}
        <Title style={{ padding: '10px 10px 0px' }}>{currentObject}</Title>
        <Divider />
        <div
          style={{
            display: 'flex',
            flexWrap: 'nowrap',
            overflow: 'auto',
            minHeight: '100%'
          }}
        >
          {timelines}
        </div>
      </div>
    </Layout.Content>
  )

  //Get the timelines of the selected timelines and set them as visible
  async function setTimeline(id: number) {
    fetch('https://tracktech.ml:50011/timelines?objectId=' + id).then(
      (text) => {
        // The server might not have any data on the object
        if (text.status == 400) {
          setTimeLineEvents(null)
        } else {
          text.json().then((json) => {
            setTimeLineEvents(new TimelineData(json.data))
          })
        }
      }
    )
    setCurrentObject('Object ' + id)
  }

  // Create the array of timeline items
  function createTimelineItems(
    cameraId: string,
    rangeArray: dateRange[]
  ): JSX.Element[] {
    var val: JSX.Element[] = []
    rangeArray.forEach((x) => {
      //From
      val.push(
        <Timeline.Item key={`${cameraId}-from-${x.from.toISOString()}`}>
          {x.from.toISOString()} | Found object
        </Timeline.Item>
      )
      //To
      val.push(
        <Timeline.Item key={`${cameraId}-to-${x.to.toISOString()}`} color="red">
          {x.to.toISOString()} | Lost object
        </Timeline.Item>
      )
    })
    return val
  }
}
