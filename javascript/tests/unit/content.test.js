const {
  formatArticleTitle,
  truncateBody,
  validateEmail,
  calculateReadingTime,
  add,
  multiply,
} = require('../../src/services/content');

describe('content service unit tests', () => {
  test('format article title', () => {
    expect(formatArticleTitle('  Hello   World  ')).toBe('Hello World');
  });

  test('truncate body', () => {
    expect(truncateBody('short')).toBe('short');
    expect(truncateBody('a'.repeat(300), 50).endsWith('...')).toBe(true);
  });

  test('validate email', () => {
    expect(validateEmail('user@example.com')).toBe(true);
    expect(validateEmail('invalid')).toBe(false);
  });

  test('calculate reading time', () => {
    expect(calculateReadingTime(400)).toBe(2);
  });

  test.each([
    [1, 2, 3],
    [10, 5, 15],
    [100, 200, 300],
  ])('add %i + %i = %i', (a, b, expected) => {
    expect(add(a, b)).toBe(expected);
  });

  test.each(Array.from({ length: 20 }, (_, i) => [i + 1, (i + 1) * 2]))(
    'multiply %i by 2',
    (n, expected) => {
      expect(multiply(n, 2)).toBe(expected);
    },
  );
});
