import { useState } from 'react';

export function useAuth() {
  const [token, setToken] = useState(null);

  const login = (access_token) => setToken(access_token);
  const logout = () => setToken(null);

  return { token, login, logout, isAuthenticated: Boolean(token) };
}