/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Button, Card, Layout } from 'antd'
import { PlusOutlined } from '@ant-design/icons'

import { Grid } from 'components/grid'
import { CameraCard } from 'components/cameraCard'
import { SelectionCard } from 'components/selectionCard'
import { ObjectTypeFilter } from 'components/objectTypeFilter'
import { stream } from 'components/overlay'
import { websocketContext } from 'components/websocketContext'
import { environmentContext } from 'components/environmentContext'
import { StopOrchestratorMessage } from 'classes/orchestratorMessage'

const { Footer, Content } = Layout

/** The selection modes for the bounding boxes. */
export type indicator = 'All' | 'Selection' | 'None'

/**
 * Home container component containing video streams and control panel.
 * @returns The Home component.
 */
export function Home() {
  /** State containing which boundingboxes to draw. */
  const [currentIndicator, setCurrentIndicator] = React.useState<indicator>(
    'All'
  )

  /** State containing which camera currently is the primary camera. */
  const [primary, setPrimary] = React.useState<string>()

  const { send, objects, setSocket } = React.useContext(websocketContext)
  const { cameras, objectTypes, orchestratorWebsocketUrl } = React.useContext(
    environmentContext
  )

  const sources: stream[] = cameras.map((stream) => ({
    id: stream.Id,
    name: stream.Name,
    srcObject: {
      src: stream.Forwarder,
      type: 'application/x-mpegURL'
    }
  }))

  /** State to keep track of the current selected objectType. */
  const [filteredObjectTypes, setFilteredObjectTypes] = React.useState<
    string[]
  >([])

  React.useEffect(() => {
    setSocket(orchestratorWebsocketUrl)
  }, [])

  // Used for camera card key generation.
  var iterator = 0

  return (
    <Content
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
          // This card contains the buttons to change which boundingboxes are drawn.
          data-testid='indicatorsCard'
          headStyle={{ padding: 0 }}
          bodyStyle={{ padding: 0 }}
          size='small'
          title={
            <h2 style={{ margin: '0px 8px', fontSize: '20px' }}>Indicators</h2>
          }
        >
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))',
              justifyContent: 'left',
              padding: '4px'
            }}
          >
            <Button
              data-testid='AllButton'
              style={{ marginLeft: '4px' }}
              type={currentIndicator === 'All' ? 'primary' : 'default'}
              onClick={() => setCurrentIndicator('All')}
            >
              All
            </Button>
            <Button
              data-testid='SelectionButton'
              style={{ marginLeft: '4px' }}
              type={currentIndicator === 'Selection' ? 'primary' : 'default'}
              onClick={() => setCurrentIndicator('Selection')}
            >
              Selection
            </Button>
            <Button
              data-testid='NoneButton'
              style={{ marginLeft: '4px' }}
              type={currentIndicator === 'None' ? 'primary' : 'default'}
              onClick={() => setCurrentIndicator('None')}
            >
              None
            </Button>
          </div>
        </Card>

        <ObjectTypeFilter
          addHidden={(a) => addHidden(a)}
          removeHidden={(a) => removeHidden(a)}
          objectTypes={objectTypes.map((objectType) => [
            objectType,
            filteredObjectTypes.some(
              (filteredObjectType) => filteredObjectType === objectType
            )
          ])}
        />

        <Card
          // This card contains the objects that are being tracked.
          data-testid={'selectionCard'}
          bodyStyle={{ padding: '4px' }}
          headStyle={{ padding: 0 }}
          size={'small'}
          title={
            <h2 style={{ margin: '0px 8px', fontSize: '20px' }}>Selection</h2>
          }
        >
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))'
            }}
          >
            {objects.map((tracked) => (
              <SelectionCard
                key={`image-${iterator++}`}
                objectId={tracked.objectId}
                onClick={() => removeSelection(tracked.objectId)}
                src={tracked.image}
              />
            ))}
          </div>
        </Card>

        <Card
          // This card contains the list of cameras that are connected.
          data-testid={'cameraList'}
          bodyStyle={{ padding: '4px' }}
          headStyle={{ padding: 0 }}
          size={'small'}
          title={
            <h2 style={{ margin: '0px 8px', fontSize: '20px' }}>Cameras</h2>
          }
          extra={<PlusOutlined style={{ marginRight: 10 }} />}
        >
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))'
            }}
          >
            {sources &&
              sources.map((source) => (
                // Create a cameracard for each stream.
                <CameraCard
                  key={`cameraCard-${iterator++}`}
                  id={source.id}
                  title={source.name}
                  setSize={setPrimary}
                />
              ))}
          </div>
        </Card>
      </div>

      <div style={{ overflowY: 'auto' }} data-testid={'gridDiv'}>
        {sources && (
          // The grid contains all the videoplayers.
          <Grid
            sources={sources}
            primary={primary ?? sources[0]?.id}
            setPrimary={(sourceId: string) => setPrimary(sourceId)}
            indicator={currentIndicator}
            hiddenObjectTypes={filteredObjectTypes}
          />
        )}
      </div>
    </Content>
  )

  /**
   * Stop tracking an object.
   * @param id Stop tracking a selected object.
   */
  function removeSelection(id: number) {
    send(new StopOrchestratorMessage(id))
  }

  /**
   * Adds a filtered object type to the list of filtered types
   * @param objectType The object type to add.
   */
  function addHidden(objectType: string) {
    setFilteredObjectTypes(
      filteredObjectTypes.filter(
        (filteredObjectType) => filteredObjectType !== objectType
      )
    )
  }

  /**
   * Removes a filtered object type to the list of filtered types.
   * @param objectType The object type to remove.
   */
  function removeHidden(objectType: string) {
    setFilteredObjectTypes([...filteredObjectTypes, objectType])
  }
}
