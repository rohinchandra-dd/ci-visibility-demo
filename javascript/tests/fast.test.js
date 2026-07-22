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

  test('fibonacci negative throws', () => {
    expect(() => fibonacci(-1)).toThrow('n must be non-negative');
  });

  test('chunk list odd length', () => {
    expect(chunkList([1, 2, 3], 2)).toEqual([[1, 2], [3]]);
  });

  test('chunk list zero size throws', () => {
    expect(() => chunkList([1, 2, 3], 0)).toThrow('size must be positive');
  });

  test('merge dicts key collision', () => {
    expect(mergeDicts({ a: 1 }, { a: 2 })).toEqual({ a: 2 });
  });

  test('is palindrome empty string', () => {
    expect(isPalindrome('')).toBe(true);
  });

  test('flatten empty list', () => {
    expect(flatten([])).toEqual([]);
  });

  test('user profile merge', () => {
    expect(mergeDicts({ email: 'user@example.com' }, { name: 'User' })).toEqual({
      email: 'user@example.com',
      name: 'User',
    });
  });

  test('monthly report total', () => {
    expect(add(multiply(50, 99), 0)).toBe(4950);
  });

  test('checkout order total', () => {
    const subtotal = multiply(25, 3);
    expect(add(subtotal, 5)).toBe(80);
  });

  test('bulk import batching', () => {
    expect(chunkList([1, 2, 3, 4, 5], 2)).toEqual([[1, 2], [3, 4], [5]]);
  });

  test('cache warmup fibonacci', () => {
    expect(fibonacci(12)).toBe(144);
  });

  test('inventory stock decrement', () => {
    const stock = subtract(5, 2);
    expect(clamp(stock, 0, 10)).toBe(3);
  });

  test('api retry backoff clamp', () => {
    expect(clamp(120, 1, 60)).toBe(60);
  });

  test('notification payload merge', () => {
    expect(mergeDicts({ status: 'sent' }, { recipient: 'user@example.com' })).toEqual({
      status: 'sent',
      recipient: 'user@example.com',
    });
  });

  test('session token merge', () => {
    expect(mergeDicts({ token: 'abc' }, { token: 'xyz' })).toEqual({ token: 'xyz' });
  });

  test('add with zero', () => {
    expect(add(0, 7)).toBe(7);
  });

  test('multiply by zero', () => {
    expect(multiply(0, 100)).toBe(0);
  });

  test('divide negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });

  test('is palindrome single character', () => {
    expect(isPalindrome('a')).toBe(true);
  });

  test('merge dicts empty source', () => {
    expect(mergeDicts({}, { a: 1 })).toEqual({ a: 1 });
  });
});
