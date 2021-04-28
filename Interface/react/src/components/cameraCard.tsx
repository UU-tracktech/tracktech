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
  FullscreenOutlined,
  FullscreenExitOutlined,
  CloseOutlined
} from '@ant-design/icons'

type cameraCardProps = {
  id: string
  title: string
  setSize: (sourceId: string, size: number) => void
}

export function CameraCard(props: cameraCardProps) {
  const [isBig, setBig] = React.useState<boolean>(false)

  var iconStyle: CSS.Properties = {
    fontSize: '16pt'
  }

  var buttonStyle: CSS.Properties = {
    margin: '8px 4px 8px 0px',
    padding: '2px',
    lineHeight: '0pt',
    height: '30px',
    width: '30px'
  }

  return (
    <Card
      key={props.id}
      title={
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <VideoCameraOutlined style={{ padding: '0px 4px' }} />
          {props.title}
        </div>
      }
      extra={
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <SettingOutlined />
        </div>
      }
      size="small"
      headStyle={{ padding: '0px 8px' }}
      bodyStyle={{ padding: '0px 8px', width: '100%', lineHeight: 0 }}
      style={{ marginTop: 5 }}
    >
      <Button type="primary" onClick={() => toggleSize()} style={buttonStyle}>
        {isBig ? (
          <FullscreenExitOutlined style={iconStyle} />
        ) : (
          <FullscreenOutlined style={iconStyle} />
        )}
      </Button>
      <Button
        type="primary"
        danger
        onClick={() => alert('clicked on delete')}
        style={buttonStyle}
      >
        {<CloseOutlined style={iconStyle} />}
      </Button>
    </Card>
  )

  function toggleSize() {
    setBig(!isBig)
    var size = isBig ? 1 : 3
    props.setSize(props.id, size)
  }
}
