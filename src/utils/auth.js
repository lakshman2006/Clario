// Simple auth/token utilities and a small API helper

const TOKEN_KEY = 'access_token';

export const setToken = (token) => {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
  } catch {}
};

export const getToken = () => {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
};

export const removeToken = () => {
  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch {}
};

export const isAuthenticated = () => !!getToken();

export const apiRequest = async (url, options = {}) => {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
  };
  const res = await fetch(url, { ...options, headers });
  return res;
};

// Helper to handle API responses
export const handleApiResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Network error' }));
    throw new Error(error.message || `HTTP ${response.status}`);
  }
  return response.json();
};

// Helper for authenticated API calls
export const authenticatedRequest = async (url, options = {}) => {
  const token = getToken();
  if (!token) {
    throw new Error('Not authenticated');
  }
  
  const response = await apiRequest(url, options);
  return handleApiResponse(response);
};

