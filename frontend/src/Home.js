import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home">
      <h1>Welcome to Trading Simulator</h1>
      <p>Start your virtual trading journey and practice with fake money!</p>
      <div className="home-actions">
        <Link to="/signup" className="btn btn-primary">Get Started</Link>
        <Link to="/login" className="btn btn-secondary">Login</Link>
      </div>
    </div>
  );
}

export default Home;
