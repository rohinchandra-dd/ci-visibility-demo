const API_BASE = import.meta.env.VITE_API_URL || '';

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
  register: (email, username, password) =>
    request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, username, password }),
    }),
  login: async (email, password) => {
    const data = await request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    localStorage.setItem('pulse_token', data.access_token);
    return data;
  },
  logout: () => localStorage.removeItem('pulse_token'),
  listArticles: () => request('/api/articles'),
  createArticle: (title, body, published = false) =>
    request('/api/articles', {
      method: 'POST',
      body: JSON.stringify({ title, body, published }),
    }),
  publishArticle: (id) =>
    request(`/api/articles/${id}/publish`, { method: 'POST' }),
  search: (q) => request(`/api/search?q=${encodeURIComponent(q)}`),
  addComment: (articleId, body) =>
    request('/api/comments', {
      method: 'POST',
      body: JSON.stringify({ body, article_id: articleId }),
    }),
};

export default api;
