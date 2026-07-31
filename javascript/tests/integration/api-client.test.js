const api = require('../../src/api/client.cjs');

describe('api client integration', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
    localStorage.clear();
  });

  test('login stores token', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ access_token: 'test-token' }),
    });
    await api.login('user@example.com', 'password');
    expect(localStorage.getItem('pulse_token')).toBe('test-token');
  });

  test('list articles calls correct endpoint', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [{ id: 1, title: 'Test' }],
    });
    const articles = await api.listArticles();
    expect(fetch).toHaveBeenCalledWith('/api/articles', expect.any(Object));
    expect(articles).toHaveLength(1);
  });

  for (let i = 1; i <= 20; i += 1) {
    test(`search query ${i}`, async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [{ id: i, title: `Result ${i}` }],
      });
      const results = await api.search(`query${i}`);
      expect(results[0].id).toBe(i);
    });
  }
});
