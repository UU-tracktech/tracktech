/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import CSS from 'csstype'
import { Button, Card } from 'antd'
import {
  VideoCameraOutlined,
  SettingOutlined,
  ExpandOutlined,
  CloseOutlined
} from '@ant-design/icons'

type cameraCardProps = {
  id: string
  title: string
  setSize: (sourceId: string) => void
}

/**
 * Component used in the cameras list. There is a card for each connected camera, which shows an identifier and buttons
 * to enlarge or shrink that camera's videoplayer
 * @param props Properties of the card
 * @returns An antd card with camera info
 */
export function CameraCard(props: cameraCardProps) {
  var buttonStyle: CSS.Properties = {
    margin: '8px 4px 8px 0px',
    padding: '2px',
    lineHeight: '0pt',
    height: '30px',
    width: '30px'
  }

  return (
    <Card
      //camera identifier
      key={props.id}
      data-testid={`camCard-${props.id}`}
      //The camera icon and the name next to it
      title={
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <VideoCameraOutlined style={{ padding: '0px 4px' }} />
          {props.title}
        </div>
      }
      //Styling
      size={'small'}
      headStyle={{ padding: '0px 8px' }}
      bodyStyle={{ padding: '0px 8px', width: '100%', lineHeight: 0 }}
      style={{ marginTop: 5 }}
    >
      <Button
        //Resize button
        data-testid={'resizeButton'}
        type={'primary'}
        onClick={() => props.setSize(props.id)}
        style={buttonStyle}
        icon={<ExpandOutlined />}
      ></Button>
    </Card>
  )
}
