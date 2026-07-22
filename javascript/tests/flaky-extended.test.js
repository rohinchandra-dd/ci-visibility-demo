describe('flaky tests for javascript-tests pipeline', () => {
  test('race condition on inventory', () => {
    const stock = 5;
    expect(stock).toBe(5);
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

  test('email delivery is eventually consistent', () => {
    if (Math.random() < 0.35) {
      throw new Error('SMTP connection reset');
    }
    expect(true).toBe(true);
  });

  test('async notification delivery', () => {
    if (Math.floor(Math.random() * 10) < 3) {
      throw new Error('Notification not received within 5s');
    }
    expect(true).toBe(true);
  });
});
