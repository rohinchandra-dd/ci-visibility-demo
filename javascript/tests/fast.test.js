const {
  add,
  subtract,
  multiply,
  divide,
  isPalindrome,
  fibonacci,
  flatten,
  chunkList,
  mergeDicts,
  clamp,
} = require('../src/app');

describe('fast unit tests', () => {
  test('add positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('add negative numbers', () => {
    expect(add(-1, -1)).toBe(-2);
  });

  test('subtract numbers', () => {
    expect(subtract(10, 4)).toBe(6);
  });

  test('multiply numbers', () => {
    expect(multiply(3, 7)).toBe(21);
  });

  test('divide numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  test('divide by zero throws', () => {
    expect(() => divide(1, 0)).toThrow('Cannot divide by zero');
  });

  test('is palindrome simple', () => {
    expect(isPalindrome('racecar')).toBe(true);
  });

  test('is palindrome with spaces', () => {
    expect(isPalindrome('A man a plan a canal Panama')).toBe(true);
  });

  test('is palindrome not palindrome', () => {
    expect(isPalindrome('hello')).toBe(false);
  });

  test('fibonacci zero', () => {
    expect(fibonacci(0)).toBe(0);
  });

  test('fibonacci one', () => {
    expect(fibonacci(1)).toBe(1);
  });

  test('fibonacci ten', () => {
    expect(fibonacci(10)).toBe(55);
  });

  test('flatten nested list', () => {
    expect(flatten([1, [2, [3, 4]], 5])).toEqual([1, 2, 3, 4, 5]);
  });

  test('chunk list even', () => {
    expect(chunkList([1, 2, 3, 4], 2)).toEqual([[1, 2], [3, 4]]);
  });

  test('merge dicts', () => {
    expect(mergeDicts({ a: 1 }, { b: 2 })).toEqual({ a: 1, b: 2 });
  });

  test('clamp within range', () => {
    expect(clamp(5, 0, 10)).toBe(5);
  });

  test('clamp below minimum', () => {
    expect(clamp(-5, 0, 10)).toBe(0);
  });

  test('clamp above maximum', () => {
    expect(clamp(15, 0, 10)).toBe(10);
  });
});
