/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import {
  StartOrchestratorMessage,
  StopOrchestratorMessage
} from '../../src/classes/orchestratorMessage'

/** Test the start message that gets sent to the orchestrator */
test('StartOrchestratorMessage', () => {
  const msg = new StartOrchestratorMessage('camID123', 3456, 2398)

  //Ensure it gets the 'start' type assigned on contruction
  expect(msg.type).toBe('start')
  //Ensure arguments are correct
  expect(msg.cameraId).toBe('camID123')
  expect(msg.frameId).toBe(3456)
  expect(msg.boxId).toBe(2398)
})

/** Test the stop message sent to the orchestrator to stop tracking */
test('StopOrchestratorMessage', () => {
  const msg = new StopOrchestratorMessage(495)

  //Ensure the 'stop' type gets assigned correctly
  expect(msg.type).toBe('stop')
  //Ensure arguments are correct
  expect(msg.objectId).toBe(495)
})
