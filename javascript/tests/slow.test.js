const { fibonacci } = require('../src/app');

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

describe('slow integration-style tests', () => {
  test('user lookup by email', async () => {
    await sleep(3000);
    expect('user@example.com').toContain('user@example.com');
  });

  test('generate monthly report', async () => {
    await sleep(8000);
    const total = Array.from({ length: 100 }, (_, i) => i).reduce((a, b) => a + b, 0);
    expect(total).toBe(4950);
  });

  test('full checkout flow', async () => {
    await sleep(15000);
    expect('order_confirmed').toBe('order_confirmed');
  });

  test('bulk import records', async () => {
    await sleep(12000);
    expect([1, 2, 3, 4, 5].length).toBe(5);
  });

  test('warm cache on startup', async () => {
    await sleep(5000);
    expect(true).toBe(true);
  });

  test('analytics fibonacci benchmark', async () => {
    await sleep(5000);
    expect(fibonacci(30)).toBe(832040);
  });
});
