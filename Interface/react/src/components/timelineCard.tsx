/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React, { ReactNode } from 'react'
import { Card } from 'antd'
import { VideoCameraOutlined } from '@ant-design/icons'

/** Properties for the timelineCard component, including the id of the camera and its children, which should only be an antd timeline. */
type timelineCardProps = { cameraId: string; children?: ReactNode }

/**
 * The timelinecard component is used in the timelines list.
 * There is a card for each camera that spotted the object at any point, which contains a timeline of important events.
 * @param props Properties for the timeline card.
 * @returns An antd card containing the camera id and the given children.
 */
export function TimelineCard(props: timelineCardProps) {
  return (
    <Card
      // The camera id title.
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
      {/* This should only be an antd timeline. */}
      {props.children}
    </Card>
  )
}
