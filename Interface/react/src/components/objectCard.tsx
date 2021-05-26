/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
  The objectcard component is used in the object list on the timelines page.
  It shows an object that was tracked before.
*/

import React from 'react'
import { Button, Card } from 'antd'
import { UserOutlined } from '@ant-design/icons'

type objectCardProps = { id: number; viewCallback: (id: number) => {} }

export function ObjectCard(props: objectCardProps) {
  return (
    <Card
      //camera identifier
      key={props.id}
      //The camera icon and the name next to it
      title={
        <div style={{ display: 'inline-flex', alignItems: 'center' }}>
          <UserOutlined style={{ margin: 'middle', paddingRight: 7 }} />
          {`Object ${props.id}`}
        </div>
      }
      //Styling
      size="small"
      headStyle={{ padding: '0px 8px' }}
      bodyStyle={{ padding: '0px 8px', width: '100%', lineHeight: 0 }}
      style={{ marginTop: 5 }}
    >
      {/*Button that can be clicked to view the timelines of this object*/}
      <Button
        type="primary"
        onClick={() => props.viewCallback(props.id)}
        style={{ marginTop: 10 }}
      >
        View
      </Button>
    </Card>
  )
}
