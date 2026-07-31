function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const { fibonacci, mergeDicts } = require('../../src/utils');

describe('slow tests', () => {
  test('user lookup by email', async () => {
    await sleep(3000);
    const user = mergeDicts({ email: 'user@example.com' }, { active: true });
    expect(user.email).toBe('user@example.com');
  });

  test('generate monthly report', async () => {
    await sleep(8000);
    expect(fibonacci(20)).toBe(6765);
  });

  test('warm cache on startup', async () => {
    await sleep(5000);
    expect(fibonacci(8)).toBe(21);
  });
});

describe('slow extended tests', () => {
  for (let i = 1; i <= 12; i += 1) {
    test(`analytics batch ${i}`, async () => {
      await sleep(5000);
      expect(fibonacci(10 + i)).toBeGreaterThan(0);
    });
  }
});
