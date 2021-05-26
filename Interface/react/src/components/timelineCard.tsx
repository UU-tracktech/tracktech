/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
  The timelinecard component is used in the timelines list.
  There is a card for each camera that spotted the object at any point,
  which contains a timeline of important events.
*/

import React, { ReactNode } from 'react'
import { Card } from 'antd'
import { VideoCameraOutlined } from '@ant-design/icons'

type timelineCardProps = { cameraId: string; children?: ReactNode }

export function TimelineCard(props: timelineCardProps) {
  return (
    <Card
      //The camera id title
      title={
        <div style={{ display: 'inline-flex', alignItems: 'center' }}>
          <VideoCameraOutlined style={{ marginRight: '10px' }} />
          <span>{props.cameraId}</span>
        </div>
      }
      style={{
        margin: '0px 10px',
        minWidth: '300px'
      }}
    >
      {props.children}
    </Card>
  )
}
