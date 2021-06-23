/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Button, Card } from 'antd'
import { UserOutlined } from '@ant-design/icons'

/** Properties of the objectCard component, containing object id and click callback. */
type objectCardProps = {
  id: number
  viewCallback: (id: number) => void
  image?: string
}

/**
 * Component used in the object list on the timelines page, shows an object that was tracked before.
 * @param props Properties of this component including an objectid and callback to view data.
 * @returns The card component.
 */
export function ObjectCard(props: objectCardProps) {
  return (
    <Card
      // Camera identifier.
      key={props.id}
      data-testid={`object-${props.id}`}
      // The camera icon and the name next to it.
      title={
        <div style={{ display: 'inline-flex', alignItems: 'center' }}>
          <UserOutlined style={{ margin: 'middle', paddingRight: 7 }} />
          <span>{`Object ${props.id}`}</span>
        </div>
      }
      // Styling.
      size='small'
      headStyle={{ padding: '0px 8px' }}
      bodyStyle={{ padding: '8px 8px', width: '100%', lineHeight: 0 }}
      style={{ marginTop: 5 }}
    >
      <div
        style={{
          width: '100%',
          display: 'grid'
        }}
      >
        {props.image ? (
          <img src={props.image} style={{ margin: '0px auto' }} />
        ) : (
          <p style={{ margin: '5px auto' }}>No image available.</p>
        )}
        {/* Button that can be clicked to view the timelines of this object. */}
        <Button
          type='primary'
          onClick={() => props.viewCallback(props.id)}
          style={{ marginTop: 10 }}
          data-testid='objectViewButton'
        >
          View
        </Button>
      </div>
    </Card>
  )
}
