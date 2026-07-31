export default function Navbar({ loggedIn, onNavigate, onLogout }) {
  return (
    <header className="navbar">
      <div className="brand" onClick={() => onNavigate('feed')}>Pulse</div>
      <nav>
        {loggedIn ? (
          <>
            <button type="button" onClick={() => onNavigate('feed')}>Feed</button>
            <button type="button" onClick={() => onNavigate('editor')}>Write</button>
            <button type="button" onClick={onLogout}>Logout</button>
          </>
        ) : (
          <button type="button" onClick={() => onNavigate('login')}>Login</button>
        )}
      </nav>
    </header>
  );
}
