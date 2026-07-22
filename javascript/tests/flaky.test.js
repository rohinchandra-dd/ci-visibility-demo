describe('flaky tests', () => {
  test('payment gateway timeout', () => {
    if (Math.random() < 0.4) {
      throw new Error('Gateway timeout after 30s');
    }
    expect(true).toBe(true);
  });
});
