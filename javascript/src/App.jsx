import { useEffect, useState } from 'react';
import api from './api/client.js';
import ArticleEditor from './components/ArticleEditor';
import Feed from './components/Feed';
import LoginForm from './components/LoginForm';
import Navbar from './components/Navbar';

export default function App() {
  const [articles, setArticles] = useState([]);
  const [loggedIn, setLoggedIn] = useState(Boolean(localStorage.getItem('pulse_token')));
  const [view, setView] = useState('feed');
  const [error, setError] = useState('');

  const loadArticles = async () => {
    try {
      const data = await api.listArticles();
      setArticles(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadArticles();
  }, []);

  const handleLogin = async (email, password) => {
    await api.login(email, password);
    setLoggedIn(true);
    setView('feed');
    setError('');
  };

  const handleLogout = () => {
    api.logout();
    setLoggedIn(false);
    setView('login');
  };

  const handleCreate = async (title, body) => {
    await api.createArticle(title, body, true);
    await loadArticles();
    setView('feed');
  };

  return (
    <div className="app">
      <Navbar
        loggedIn={loggedIn}
        onNavigate={setView}
        onLogout={handleLogout}
      />
      <main className="container">
        {error && <p className="error">{error}</p>}
        {!loggedIn && view === 'login' && <LoginForm onLogin={handleLogin} />}
        {loggedIn && view === 'feed' && <Feed articles={articles} />}
        {loggedIn && view === 'editor' && <ArticleEditor onSubmit={handleCreate} />}
      </main>
    </div>
  );
}
