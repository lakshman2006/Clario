import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { setToken, handleApiResponse } from '../utils/auth';

const OAuthCallback = () => {
  const navigate = useNavigate();
  const [status, setStatus] = useState('Processing...');
  const [error, setError] = useState('');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        setStatus('Completing sign-in...');
        
        // Get URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        const error = urlParams.get('error');
        
        if (error) {
          throw new Error(`OAuth error: ${error}`);
        }
        
        if (!code) {
          throw new Error('No authorization code received');
        }
        
        // Exchange code for token via backend
        const response = await fetch(
          `http://localhost:8000/api/v1/auth/google/callback?code=${code}`,
          { method: 'GET' }
        );
        
        const result = await handleApiResponse(response);
        
        if (result.status === 'success' && result.data?.access_token) {
          setToken(result.data.access_token);
          setStatus('Sign-in successful! Redirecting...');
          setTimeout(() => navigate('/profile'), 1500);
        } else {
          throw new Error('No access token received from server');
        }
        
      } catch (error) {
        console.error('OAuth callback error:', error);
        setError(error.message);
        setStatus('Sign-in failed');
        setTimeout(() => navigate('/login'), 3000);
      }
    };

    handleCallback();
  }, [navigate]);

  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center', 
      minHeight: '100vh',
      flexDirection: 'column',
      gap: '1rem',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white'
    }}>
      <div style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>
        {status}
      </div>
      
      {error && (
        <div style={{ 
          color: '#ff6b6b', 
          textAlign: 'center',
          maxWidth: '400px',
          padding: '1rem'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {status.includes('failed') && (
        <button 
          onClick={() => navigate('/login')}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: 'white',
            color: '#667eea',
            border: 'none',
            borderRadius: '0.5rem',
            cursor: 'pointer'
          }}
        >
          Return to Login
        </button>
      )}
      
      {status.includes('successful') && (
        <div style={{ color: '#51cf66' }}>
          ✓ Authentication complete
        </div>
      )}
    </div>
  );
};

export default OAuthCallback;


