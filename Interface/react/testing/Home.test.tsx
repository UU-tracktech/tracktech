import React from 'react';
import { render, screen } from '@testing-library/react';
import { Home } from '../src/pages/home';

test('Home renders', () => {
    render(<Home />);
})