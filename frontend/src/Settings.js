import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Settings() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [updating, setUpdating] = useState(false);
  const navigate = useNavigate();

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
      setFormData(prev => ({
        ...prev,
        name: data.name || ''
      }));
    } catch (err) {
      setError(err.message);
      console.error('Profile fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear messages when user starts typing
    setError(null);
    setSuccess(null);
  };

  const validateForm = () => {
    if (formData.newPassword && formData.newPassword !== formData.confirmPassword) {
      setError('New passwords do not match');
      return false;
    }
    if (formData.newPassword && formData.newPassword.length < 6) {
      setError('New password must be at least 6 characters long');
      return false;
    }
    if (formData.newPassword && !formData.currentPassword) {
      setError('Current password is required to set new password');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setUpdating(true);
    setError(null);
    setSuccess(null);

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      // Prepare update data
      const updateData = {
        name: formData.name
      };

      // Only include password fields if user wants to change password
      if (formData.newPassword) {
        updateData.currentPassword = formData.currentPassword;
        updateData.newPassword = formData.newPassword;
      }

      const response = await fetch('/api/auth/profile', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || `Update failed: ${response.status}`);
      }

      const updatedProfile = await response.json();
      setProfile(updatedProfile);
      setSuccess('Profile updated successfully!');
      
      // Clear password fields after successful update
      setFormData(prev => ({
        ...prev,
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }));

    } catch (err) {
      setError(err.message);
      console.error('Profile update error:', err);
    } finally {
      setUpdating(false);
    }
  };

  const handleCancel = () => {
    if (profile) {
      setFormData({
        name: profile.name || '',
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    }
    setError(null);
    setSuccess(null);
  };

  if (loading) {
    return (
      <div className="settings-container">
        <div className="loading">
          <h2>Loading Settings...</h2>
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error && !profile) {
    return (
      <div className="settings-container">
        <div className="error">
          <h2>Error Loading Settings</h2>
          <p>{error}</p>
          <button onClick={fetchProfile} className="btn btn-primary">
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
    <div className="settings-container">
      <div className="settings-header">
        <h1>Account Settings</h1>
        <div className="settings-actions">
          <Link to="/profile" className="btn btn-secondary">
            View Profile
          </Link>
          <Link to="/dashboard" className="btn btn-secondary">
            Back to Dashboard
          </Link>
        </div>
      </div>

      <div className="settings-content">
        <form onSubmit={handleSubmit} className="settings-form">
          <div className="form-section">
            <h3>Personal Information</h3>
            
            <div className="form-group">
              <label htmlFor="username">Username (read-only):</label>
              <input
                type="text"
                id="username"
                value={profile?.username || ''}
                disabled
                className="form-control disabled"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email (read-only):</label>
              <input
                type="email"
                id="email"
                value={profile?.email || ''}
                disabled
                className="form-control disabled"
              />
            </div>

            <div className="form-group">
              <label htmlFor="name">Full Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Enter your full name"
                className="form-control"
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Change Password</h3>
            <p className="form-help">Leave password fields empty if you don't want to change your password.</p>
            
            <div className="form-group">
              <label htmlFor="currentPassword">Current Password:</label>
              <input
                type="password"
                id="currentPassword"
                name="currentPassword"
                value={formData.currentPassword}
                onChange={handleInputChange}
                placeholder="Enter current password"
                className="form-control"
                autoComplete="current-password"
              />
            </div>

            <div className="form-group">
              <label htmlFor="newPassword">New Password:</label>
              <input
                type="password"
                id="newPassword"
                name="newPassword"
                value={formData.newPassword}
                onChange={handleInputChange}
                placeholder="Enter new password (min 6 characters)"
                className="form-control"
                autoComplete="new-password"
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm New Password:</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                placeholder="Confirm new password"
                className="form-control"
                autoComplete="new-password"
              />
            </div>
          </div>

          {error && (
            <div className="alert alert-error">
              <strong>Error:</strong> {error}
            </div>
          )}

          {success && (
            <div className="alert alert-success">
              <strong>Success:</strong> {success}
            </div>
          )}

          <div className="form-actions">
            <button 
              type="submit" 
              disabled={updating}
              className="btn btn-primary"
            >
              {updating ? 'Updating...' : 'Update Profile'}
            </button>
            <button 
              type="button" 
              onClick={handleCancel}
              disabled={updating}
              className="btn btn-secondary"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Settings;
