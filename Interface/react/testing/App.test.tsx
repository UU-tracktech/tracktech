import React from 'react';
import { render, screen } from '@testing-library/react';
import { App } from '../src/App';
import fetchMock from 'jest-fetch-mock';

jest.mock("@react-keycloak/web", () => {
  const originalModule = jest.requireActual("@react-keycloak/web");
  return {
    ...originalModule,
    useKeycloak: () => ({
      keycloak: {authenticated: false, login: () => {}, logout: () => {}},
      initialized: false
    })
  }
})

test('App renders', async () => {
  fetch("www.google.com")
  render(<App />);
})