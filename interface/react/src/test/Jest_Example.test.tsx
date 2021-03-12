
import React from 'react';
import { add, newTotal } from './Jest_Example';
import './Jest_Example'
/*
Tests can be run by typing the command:

       npm run test

In the following examples some unit tests are displayed

*/

//A test that is (always) true
test('Example1', () => {expect(true).toBeTruthy()})

//A test that is (always) false
test('Example2', () => {expect(true).toBeTruthy()})

//A test that asserts if 1 + 2 is equal to 3
test('Example3', () => {expect(add(1,2)).toBe(3)});

//Another example with another assertion
test('Example4', () => {expect(add(3,4)).toBeGreaterThan(3)});

//Another test
test('Example5', () => {expect(newTotal(1, 2)).toBe('$3')});
/*
The newTotal function depends on the functionality of add, in order to make functions that are not dependent on other functions we can use a mock.
 */
//Creating a mock that returns some value
const sum = jest.fn(() => 6);