import { useState } from 'react';

export default function ArticleEditor({ onSubmit }) {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    await onSubmit(title, body);
    setTitle('');
    setBody('');
  };

  return (
    <form className="card editor" onSubmit={handleSubmit}>
      <h1>Write an article</h1>
      <label>
        Title
        <input value={title} onChange={(e) => setTitle(e.target.value)} required />
      </label>
      <label>
        Body
        <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={10} required />
      </label>
      <button type="submit">Publish</button>
    </form>
  );
}
