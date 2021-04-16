import { enableFetchMocks } from 'jest-fetch-mock'
enableFetchMocks()
fetch.mockResponse(JSON.stringify([]))