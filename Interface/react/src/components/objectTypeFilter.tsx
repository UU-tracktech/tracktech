/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { Button, Card } from 'antd'

export type ObjectTypeFilterProps = {
  objectTypes: [string, boolean][]
  addHidden: (filteredObjectType: string) => void
  removeHidden: (filteredObjectType: string) => void
}
export function ObjectTypeFilter(props: ObjectTypeFilterProps) {
  return (
    <Card
      //This card contains the buttons to change which boundingboxes are drawnsize="small"
      headStyle={{ padding: 0 }}
      bodyStyle={{ padding: 0 }}
      title={
        <h2 style={{ margin: '0px 8px', fontSize: '20px' }}>Object Types</h2>
      }
    >
      <div
        style={{
          padding: '4px',
          display: 'grid',
          rowGap: '4px',
          columnGap: '4px',
          gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))'
        }}
      >
        {props.objectTypes.map(([objectType, hidden]) => {
          return (
            <Button
              key={objectType}
              type={hidden ? 'default' : 'primary'}
              onClick={
                hidden
                  ? () => props.addHidden(objectType)
                  : () => props.removeHidden(objectType)
              }
            >
              {objectType}
            </Button>
          )
        })}
      </div>
    </Card>
  )
}
