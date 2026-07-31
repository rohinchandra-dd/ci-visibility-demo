export default function Feed({ articles }) {
  if (!articles.length) {
    return <p className="empty">No articles yet. Be the first to write one.</p>;
  }

  return (
    <section className="feed">
      <h1>Community Feed</h1>
      {articles.map((article) => (
        <article key={article.id} className="card">
          <h2>{article.title}</h2>
          <p>{article.body.slice(0, 200)}{article.body.length > 200 ? '...' : ''}</p>
        </article>
      ))}
    </section>
  );
}
