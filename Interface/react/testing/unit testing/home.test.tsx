/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from 'react'
import { act, render } from '@testing-library/react'
import { Home } from '../../src/pages/home'

test('Home renders', async () => {
  await act(async () => {
    render(<Home />)
  })
})
