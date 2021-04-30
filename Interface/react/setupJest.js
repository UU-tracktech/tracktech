/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import { enableFetchMocks } from 'jest-fetch-mock'
enableFetchMocks()
fetch.mockResponse(JSON.stringify([]))