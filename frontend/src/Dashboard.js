import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [tradeHistory, setTradeHistory] = useState([]);
  const [userStats, setUserStats] = useState({
    totalTrades: 0,
    profitLoss: 0,
    portfolioValue: 100000, // Starting with $100,000 virtual money
    successRate: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token || !userData) {
      navigate('/login');
      return;
    }

    try {
      setUser(JSON.parse(userData));
    } catch (error) {
      console.error('Error parsing user data:', error);
      navigate('/login');
      return;
    }

    fetchTradeHistory();
  }, [navigate]);

  const fetchTradeHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/trade/history', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setTradeHistory(data.trades || []);
        calculateStats(data.trades || []);
      } else if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
      } else {
        setError('Failed to fetch trade history');
      }
    } catch (error) {
      console.error('Error fetching trade history:', error);
      setError('Network error while fetching trade data');
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (trades) => {
    const totalTrades = trades.length;
    let totalProfitLoss = 0;
    let successfulTrades = 0;

    trades.forEach(trade => {
      if (trade.profit_loss) {
        totalProfitLoss += parseFloat(trade.profit_loss);
        if (trade.profit_loss > 0) {
          successfulTrades++;
        }
      }
    });

    const successRate = totalTrades > 0 ? (successfulTrades / totalTrades * 100).toFixed(1) : 0;
    const portfolioValue = 100000 + totalProfitLoss; // Starting value + profit/loss

    setUserStats({
      totalTrades,
      profitLoss: totalProfitLoss,
      portfolioValue,
      successRate
    });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/');
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Trading Simulator Dashboard</h1>
          <div className="user-info">
            <span>Welcome, {user?.username || user?.email}</span>
            <button onClick={handleLogout} className="btn btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        {error && (
          <div className="error-message">
            {error}
            <button onClick={fetchTradeHistory} className="retry-btn">
              Retry
            </button>
          </div>
        )}

        {/* User Stats Section */}
        <section className="stats-section">
          <h2>Portfolio Overview</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Portfolio Value</h3>
              <div className="stat-value">
                {formatCurrency(userStats.portfolioValue)}
              </div>
            </div>
            <div className="stat-card">
              <h3>Total Trades</h3>
              <div className="stat-value">{userStats.totalTrades}</div>
            </div>
            <div className="stat-card">
              <h3>Profit/Loss</h3>
              <div className={`stat-value ${
                userStats.profitLoss >= 0 ? 'profit' : 'loss'
              }`}>
                {formatCurrency(userStats.profitLoss)}
              </div>
            </div>
            <div className="stat-card">
              <h3>Success Rate</h3>
              <div className="stat-value">{userStats.successRate}%</div>
            </div>
          </div>
        </section>

        {/* Trade History Section */}
        <section className="history-section">
          <h2>Recent Trade History</h2>
          {tradeHistory.length === 0 ? (
            <div className="no-trades">
              <p>No trades yet. Start trading to see your history here!</p>
              <Link to="/trade" className="btn btn-primary">
                Start Trading
              </Link>
            </div>
          ) : (
            <div className="trade-history">
              <div className="table-container">
                <table className="trades-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Symbol</th>
                      <th>Type</th>
                      <th>Quantity</th>
                      <th>Price</th>
                      <th>P&L</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tradeHistory.slice(0, 10).map((trade, index) => (
                      <tr key={trade.id || index}>
                        <td>{formatDate(trade.created_at || trade.date)}</td>
                        <td className="symbol">{trade.symbol}</td>
                        <td>
                          <span className={`trade-type ${trade.type}`}>
                            {trade.type?.toUpperCase()}
                          </span>
                        </td>
                        <td>{trade.quantity}</td>
                        <td>{formatCurrency(trade.price || 0)}</td>
                        <td className={`pnl ${
                          trade.profit_loss >= 0 ? 'profit' : 'loss'
                        }`}>
                          {trade.profit_loss ? formatCurrency(trade.profit_loss) : '-'}
                        </td>
                        <td>
                          <span className={`status ${trade.status}`}>
                            {trade.status?.toUpperCase()}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              {tradeHistory.length > 10 && (
                <div className="view-more">
                  <Link to="/trade-history" className="btn btn-outline">
                    View All Trades ({tradeHistory.length})
                  </Link>
                </div>
              )}
            </div>
          )}
        </section>

        {/* Quick Actions */}
        <section className="actions-section">
          <h2>Quick Actions</h2>
          <div className="actions-grid">
            <Link to="/trade" className="action-card">
              <h3>New Trade</h3>
              <p>Execute a new trade with real-time market data</p>
            </Link>
            <Link to="/portfolio" className="action-card">
              <h3>View Portfolio</h3>
              <p>Manage your current holdings and positions</p>
            </Link>
            <Link to="/market" className="action-card">
              <h3>Market Data</h3>
              <p>View live stock prices and market trends</p>
            </Link>
            <Link to="/profile" className="action-card">
              <h3>Profile Settings</h3>
              <p>Update your account settings and preferences</p>
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
