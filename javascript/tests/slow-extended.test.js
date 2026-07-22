const { fibonacci, mergeDicts } = require('../src/app');

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

describe('slow tests for javascript-tests pipeline', () => {
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
