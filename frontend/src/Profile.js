import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch('/api/auth/profile', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch profile: ${response.status}`);
      }

      const data = await response.json();
      setProfile(data);
    } catch (err) {
      setError(err.message);
      console.error('Profile fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchProfile();
  };

  if (loading) {
    return (
      <div className="profile-container">
        <div className="loading">
          <h2>Loading Profile...</h2>
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container">
        <div className="error">
          <h2>Error Loading Profile</h2>
          <p>{error}</p>
          <button onClick={handleRefresh} className="btn btn-primary">
            Try Again
          </button>
          <Link to="/dashboard" className="btn btn-secondary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>My Profile</h1>
        <div className="profile-actions">
          <Link to="/settings" className="btn btn-primary">
            Edit Profile
          </Link>
          <Link to="/dashboard" className="btn btn-secondary">
            Back to Dashboard
          </Link>
        </div>
      </div>

      {profile && (
        <div className="profile-content">
          <div className="profile-card">
            <div className="profile-field">
              <label>User ID:</label>
              <span>{profile.id}</span>
            </div>
            <div className="profile-field">
              <label>Username:</label>
              <span>{profile.username}</span>
            </div>
            <div className="profile-field">
              <label>Name:</label>
              <span>{profile.name || 'Not provided'}</span>
            </div>
            <div className="profile-field">
              <label>Email:</label>
              <span>{profile.email}</span>
            </div>
            <div className="profile-field">
              <label>Member Since:</label>
              <span>{new Date(profile.created_at).toLocaleDateString()}</span>
            </div>
            <div className="profile-field">
              <label>Last Updated:</label>
              <span>{new Date(profile.updated_at).toLocaleDateString()}</span>
            </div>
          </div>

          <div className="profile-stats">
            <h3>Account Statistics</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Portfolio Value:</span>
                <span className="stat-value">${profile.portfolio_value || '0.00'}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Total Trades:</span>
                <span className="stat-value">{profile.total_trades || 0}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Account Balance:</span>
                <span className="stat-value">${profile.balance || '0.00'}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Profile;
