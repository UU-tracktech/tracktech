import React from 'react';
import { render, screen } from '@testing-library/react';
import { App } from '../src/App';

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

test('App renders', () => {
  render(<App />);
})