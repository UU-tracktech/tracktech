/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
  The cameracard component is used in the cameras list.
  There is a card for each connected camera, shows an identifier and buttons
  to enlarge, shrink or (TODO: delete) that camera's videoplayer
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

// The properties each card has
type cameraCardProps = {
  id: string //An identifier so we know what camera it belongs to
  title: string //The name of the camera
  setSize: (sourceId: string) => void //callback function for the resize button
}

export function CameraCard(props: cameraCardProps) {
  //Style property so it can be reused to prevent duplicate code
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
      //The settings icon (TODO: implement camera settings)
      extra={
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <SettingOutlined />
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
      <Button
        //Delete button (TODO: implement removing a camera feed)
        type={'primary'}
        data-testid={'deleteButton'}
        danger
        onClick={() => alert('clicked on delete')}
        style={buttonStyle}
        icon={<CloseOutlined />}
      ></Button>
    </Card>
  )
}
