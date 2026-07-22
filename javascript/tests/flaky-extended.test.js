describe('flaky tests for javascript-tests pipeline', () => {
  test('race condition on inventory', () => {
    if (Math.floor(Math.random() * 10) < 4) {
      throw new Error('Expected stock=5, got stock=3');
    }
    expect(true).toBe(true);
  });

  test('third party api rate limit', () => {
    if (Math.random() < 0.35) {
      throw new Error('HTTP 429: Too Many Requests');
    }
    expect(true).toBe(true);
  });

  test('concurrent user session', () => {
    if (Math.random() < 0.38) {
      throw new Error('Session token mismatch after concurrent writes');
    }
    expect(true).toBe(true);
  });
});
