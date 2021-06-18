/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { DeleteOutlined } from '@ant-design/icons'
import { Button, Card, Popconfirm } from 'antd'

const { Meta } = Card

/** Properties for the selectionCard component, including click callback, id of the object and an image. */
type selectionCardProps = { onClick: () => void; objectId: number; src: string }

/**
 * Selection card used on the selection card on the home page.
 * It displays a tracked object including its cutout.
 * @param props Properties for the selection card.
 * @returns An antd card containing all selected objects, their ids, and an image.
 */
export function SelectionCard(props: selectionCardProps) {
  return (
    // The main card is used to display the image.
    <Card
      size='small'
      style={{
        display: 'inline-block',
        height: 'auto',
        margin: 2,
        paddingTop: 4
      }}
      cover={
        <img
          data-testid={`image-${props.src}`}
          src={props.src}
          style={{ display: 'block', height: 100, objectFit: 'contain' }}
        />
      }
    >
      {/* Meta is used to render the bottom description. */}
      <Meta
        title={
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              width: '100%'
            }}
          >
            {/* The span contains the obejct id / title, and the stop tracking button. */}
            {`Object ${props.objectId}`}{' '}
            <Popconfirm
              title='Are you sure to stop tracking this object?'
              onConfirm={() => props.onClick()}
              okText='Yes'
              cancelText='No'
              placement='bottomRight'
            >
              <Button
                icon={<DeleteOutlined />}
                type='text'
                style={{
                  justifySelf: 'end',
                  display: 'inline-flex',
                  justifyContent: 'center',
                  alignItems: 'center'
                }}
                data-testid={'deleteSelectionButton'}
              />
            </Popconfirm>
          </span>
        }
      />
    </Card>
  )
}
