const { fibonacci } = require('../src/app');

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

describe('slow integration-style tests', () => {
  test('analytics fibonacci benchmark', async () => {
    await sleep(5000);
    expect(fibonacci(30)).toBe(832040);
  });
});
