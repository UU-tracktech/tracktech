/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { useContext } from 'react'
import { Layout, Card, Timeline, Divider } from 'antd'
import { Typography } from 'antd'

import { ObjectCard } from 'components/objectCard'
import { TimelineCard } from 'components/timelineCard'
import { TimelineData, dateRange } from 'classes/timelineData'
import { environmentContext } from 'components/environmentContext'
import { websocketContext } from 'components/websocketContext'

const { Title } = Typography

/**
 * Timeline container component containing timelines that show when objects where detected over time.
 * @returns The timelines page.
 */
export function Timelines() {
  // State containing all the tracked objects.
  const [objectIds, setObjectIds] = React.useState<number[]>([])
  // State containing the currently selected item.
  const [currentObject, setCurrentObject] = React.useState<string>(
    'Tracking timelines'
  )
  // State containing the events of the currently selected item, which is null if no data is available.
  const [
    timelineEvents,
    setTimeLineEvents
  ] = React.useState<TimelineData | null>(new TimelineData([]))

  const { orchestratorObjectIdsUrl, orchestratorTimelinesUrl } = useContext(
    environmentContext
  )

  const { objects } = useContext(websocketContext)

  React.useEffect(() => {
    // Get all the tracked objects from the server and display them.
    fetch(orchestratorObjectIdsUrl).then((text) =>
      text.json().then((json) => {
        if (json.data != undefined) setObjectIds(json.data)
      })
    )
  }, [])

  var timelines: JSX.Element[] = []

  // Create the timeline if there is data.
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
    // Otherwise show a message explaining there is no data.
  } else {
    timelines.push(
      <p style={{ paddingLeft: 10 }}>No tracking data available.</p>
    )
  }

  return (
    // Main content of the page.
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
          // This card contains the objects have been or are being tracked.
          bodyStyle={{ padding: '4px' }}
          headStyle={{ padding: 0 }}
          size='small'
          data-testid='tracked-objects-container'
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
              gridAutoRows: '100%'
            }}
          >
            {/* Map the objects to cards. */}
            {objectIds.map((objectId) => {
              var objectImage = objects.find(
                (message) => message.objectId == objectId
              )?.image
              return (
                <ObjectCard
                  key={objectId}
                  id={objectId}
                  viewCallback={(id: number) => setTimeline(id)}
                  image={objectImage}
                />
              )
            })}
          </div>
        </Card>
      </div>

      <div
        style={{ overflowY: 'auto', backgroundColor: 'white', margin: '5px' }}
      >
        {/* Show the currently selected object data. */}
        <Title
          data-testid='timelines-page-title'
          style={{ padding: '10px 10px 0px' }}
        >
          {currentObject}
        </Title>
        <Divider />
        <div
          data-testid='timelines-page-content'
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

  /**
   * Get the timelines of the selected timelines and set them as visible.
   * @param id Id of the object to get logging data from.
   */
  function setTimeline(id: number) {
    fetch(orchestratorTimelinesUrl + '?objectId=' + id).then((text) => {
      // The server might not have any data on the object.
      if (text.status == 400) {
        setTimeLineEvents(null)
      } else {
        text.json().then((json) => {
          setTimeLineEvents(new TimelineData(json.data))
        })
      }
    })
    setCurrentObject('Object ' + id)
  }

  /**
   * Create the array of timeline items.
   * @param cameraId Id of the camera to get items from.
   * @param rangeArray Logging data for this camera.
   * @returns
   */
  function createTimelineItems(
    cameraId: string,
    rangeArray: dateRange[]
  ): JSX.Element[] {
    var val: JSX.Element[] = []
    rangeArray.forEach((x) => {
      // From.
      val.push(
        <Timeline.Item key={`${cameraId}-from-${x.from.toUTCString()}`}>
          {x.from.toUTCString()} | Found object
        </Timeline.Item>
      )
      // To.
      val.push(
        <Timeline.Item key={`${cameraId}-to-${x.to.toUTCString()}`} color='red'>
          {x.to.toUTCString()} | Lost object
        </Timeline.Item>
      )
    })
    return val
  }
}
