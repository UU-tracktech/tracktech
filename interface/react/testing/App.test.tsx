import React from 'react';
import { render, screen } from '@testing-library/react';
import { Home } from '../src/pages/home';

test('renders learn react link', () => {
  render(<Home />); const linkElement = screen.getByText(/Cameras/i);
  expect(linkElement).toBeDefined()
});
