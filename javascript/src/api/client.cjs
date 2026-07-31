/** CommonJS API client for Jest tests. */

const API_BASE = process.env.VITE_API_URL || '';

function getToken() {
  return localStorage.getItem('pulse_token');
}

async function request(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || response.statusText);
  }
  return response.json();
}

const api = {
  login: async (email, password) => {
    const data = await request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    localStorage.setItem('pulse_token', data.access_token);
    return data;
  },
  listArticles: () => request('/api/articles'),
  search: (q) => request(`/api/search?q=${encodeURIComponent(q)}`),
};

module.exports = api;
