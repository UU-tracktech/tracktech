/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import {
  SetUsesImagesMessage,
  StartOrchestratorMessage,
  StopOrchestratorMessage,
  AuthenticateOrchestratorMessage
} from 'classes/orchestratorMessage'

// Collection of tests for the classes contained in the orchestratorMessage file
describe('Test the creation of classes in the orchestratorMessage file', () => {
  // Test the creation of the StartOrchestratorMessage
  it('Creates the StartOrchestratorMessage correctly', () => {
    // Test a message without an image link
    let msg = new StartOrchestratorMessage('camID', 2, 3)
    expect(msg.type).toBe('start')
    expect(msg.cameraId).toBe('camID')
    expect(msg.frameId).toBe(2)
    expect(msg.boxId).toBe(3)
    expect(msg.image).not.toBeDefined()

    // Test with an image link
    msg = new StartOrchestratorMessage('camID', 2, 3, 'LinkToImage')
    expect(msg.image).toBe('LinkToImage')
  })

  // Test the creation of the StopOrchestratorMessage
  it('Creates the StopOrchestratorMessage correctly', () => {
    let msg = new StopOrchestratorMessage(3)
    expect(msg.type).toBe('stop')
    expect(msg.objectId).toBe(3)
  })

  // Test the creation of the setUsesImageMessage
  it('Creates the setUsesImageMessage correctly', () => {
    let msg = new SetUsesImagesMessage(true)
    expect(msg.type).toBe('setUsesImages')
    expect(msg.usesImages).toBeTruthy()
  })

  // Test the creation of the AuthenticateOrchestratorMessage
  it('Creates the AuthenticateOrchestratorMessage correctly', () => {
    const msg = new AuthenticateOrchestratorMessage('test')
    expect(msg.type).toBe('authenticate')
    expect(msg.jwt).toBe('test')
  })
})
