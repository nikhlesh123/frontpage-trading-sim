import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [stockLTP, setStockLTP] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch stock LTP on component mount
  useEffect(() => {
    fetchStockLTP();
  }, []);

  const fetchStockLTP = async () => {
    try {
      const response = await fetch('/api/stocks/ltp?symbol=RELIANCE');
      const data = await response.json();
      setStockLTP(data.ltp);
    } catch (error) {
      console.error('Error fetching stock LTP:', error);
      setStockLTP('Error loading price');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.token);
        window.location.href = '/dashboard';
      } else {
        alert('Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed');
    }
  };

  return (
    <div className="home">
      <h1>Welcome to Trading Simulator</h1>
      <p>Start your virtual trading journey and practice with fake money!</p>
      
      {/* Stock LTP Display */}
      <div className="stock-display">
        <h3>RELIANCE Stock Price</h3>
        <div className="ltp-price">
          {loading ? 'Loading...' : `₹${stockLTP}`}
        </div>
      </div>

      {/* Login Form */}
      <div className="login-section">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary">Login</button>
        </form>
      </div>

      {/* Signup Button */}
      <div className="home-actions">
        <Link to="/signup" className="btn btn-success">Get Started - Sign Up</Link>
      </div>
    </div>
  );
}

export default Home;
