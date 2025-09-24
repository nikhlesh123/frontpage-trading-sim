import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    // Get user info from token or API
    fetchUserInfo(token);
  }, [navigate]);

  const fetchUserInfo = async (token) => {
    try {
      setLoading(true);
      setError(null);
      
      // Try to get user info from API
      const response = await fetch('/api/auth/profile', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // If API call fails, we'll just show a basic dashboard
        // This could happen if backend isn't implemented yet
        setUser({ username: 'User', name: 'Trading User' });
      }
    } catch (err) {
      console.error('Failed to fetch user info:', err);
      // Set default user info if API is not available
      setUser({ username: 'User', name: 'Trading User' });
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">
          <h2>Loading Dashboard...</h2>
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Trading Simulator Dashboard</h1>
          <div className="user-info">
            <span>Welcome, {user?.name || user?.username || 'User'}!</span>
            <button onClick={handleLogout} className="btn btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-grid">
          {/* Account Management Section */}
          <section className="dashboard-card">
            <h2>Account Management</h2>
            <div className="card-content">
              <div className="action-buttons">
                <Link to="/profile" className="btn btn-primary">
                  <span className="btn-icon">👤</span>
                  View Profile
                </Link>
                <Link to="/settings" className="btn btn-secondary">
                  <span className="btn-icon">⚙️</span>
                  Account Settings
                </Link>
              </div>
              <p className="card-description">
                Manage your account information, view your profile, and update your settings.
              </p>
            </div>
          </section>

          {/* Portfolio Overview Section */}
          <section className="dashboard-card">
            <h2>Portfolio Overview</h2>
            <div className="card-content">
              <div className="portfolio-stats">
                <div className="stat-item">
                  <span className="stat-label">Portfolio Value</span>
                  <span className="stat-value">$10,000.00</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Available Cash</span>
                  <span className="stat-value">$5,000.00</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Total Return</span>
                  <span className="stat-value stat-positive">+$500.00</span>
                </div>
              </div>
              <div className="action-buttons">
                <button className="btn btn-primary">
                  View Full Portfolio
                </button>
              </div>
            </div>
          </section>

          {/* Trading Section */}
          <section className="dashboard-card">
            <h2>Trading</h2>
            <div className="card-content">
              <div className="action-buttons">
                <button className="btn btn-success">
                  <span className="btn-icon">📈</span>
                  Buy Stocks
                </button>
                <button className="btn btn-danger">
                  <span className="btn-icon">📉</span>
                  Sell Stocks
                </button>
                <button className="btn btn-info">
                  <span className="btn-icon">📊</span>
                  Market Research
                </button>
              </div>
              <p className="card-description">
                Execute trades, research market trends, and manage your investment strategy.
              </p>
            </div>
          </section>

          {/* Recent Activity Section */}
          <section className="dashboard-card">
            <h2>Recent Activity</h2>
            <div className="card-content">
              <div className="activity-list">
                <div className="activity-item">
                  <span className="activity-type">Buy</span>
                  <span className="activity-details">AAPL - 10 shares at $150.00</span>
                  <span className="activity-time">2 hours ago</span>
                </div>
                <div className="activity-item">
                  <span className="activity-type">Sell</span>
                  <span className="activity-details">GOOGL - 5 shares at $2,800.00</span>
                  <span className="activity-time">1 day ago</span>
                </div>
                <div className="activity-item">
                  <span className="activity-type">Buy</span>
                  <span className="activity-details">TSLA - 20 shares at $250.00</span>
                  <span className="activity-time">3 days ago</span>
                </div>
              </div>
              <div className="action-buttons">
                <button className="btn btn-outline">
                  View All Activity
                </button>
              </div>
            </div>
          </section>

          {/* Market Summary Section */}
          <section className="dashboard-card">
            <h2>Market Summary</h2>
            <div className="card-content">
              <div className="market-indices">
                <div className="index-item">
                  <span className="index-name">S&P 500</span>
                  <span className="index-value">4,150.25</span>
                  <span className="index-change positive">+1.2%</span>
                </div>
                <div className="index-item">
                  <span className="index-name">NASDAQ</span>
                  <span className="index-value">12,800.50</span>
                  <span className="index-change positive">+0.8%</span>
                </div>
                <div className="index-item">
                  <span className="index-name">DOW</span>
                  <span className="index-value">34,200.75</span>
                  <span className="index-change negative">-0.3%</span>
                </div>
              </div>
            </div>
          </section>

          {/* Quick Actions Section */}
          <section className="dashboard-card">
            <h2>Quick Actions</h2>
            <div className="card-content">
              <div className="quick-actions">
                <button className="quick-action-btn">
                  <span className="action-icon">💰</span>
                  <span className="action-label">Add Funds</span>
                </button>
                <button className="quick-action-btn">
                  <span className="action-icon">📋</span>
                  <span className="action-label">Watchlist</span>
                </button>
                <button className="quick-action-btn">
                  <span className="action-icon">📈</span>
                  <span className="action-label">Charts</span>
                </button>
                <button className="quick-action-btn">
                  <span className="action-icon">📰</span>
                  <span className="action-label">News</span>
                </button>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
