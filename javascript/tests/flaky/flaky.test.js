const { sendEmailSimulation } = require('../../src/services/notifications');

describe('flaky tests', () => {
  test('payment gateway timeout', () => {
    const result = sendEmailSimulation('user@example.com', 'Payment', 'Processing');
    if (!result.delivered) {
      throw new Error('Payment gateway timeout');
    }
    expect(result.delivered).toBe(true);
  });

  for (let i = 1; i <= 5; i += 1) {
    test(`email delivery ${i}`, () => {
      const result = sendEmailSimulation(`user${i}@example.com`, 'Subject', 'Body');
      if (!result.delivered) {
        throw new Error('Email delivery failed');
      }
      expect(result.delivered).toBe(true);
    });
  }
});

describe('flaky extended tests', () => {
  const scenarios = ['inventory race', 'rate limits', 'sessions', 'email queue', 'notifications'];
  scenarios.forEach((name, index) => {
    test(name, () => {
      const result = sendEmailSimulation(`flaky${index}@example.com`, name, 'test');
      if (!result.delivered) {
        throw new Error(`${name} failed intermittently`);
      }
      expect(result.delivered).toBe(true);
    });
  });
});
