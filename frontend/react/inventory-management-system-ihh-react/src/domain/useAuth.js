/**
 * AUTH HOOK module.
 *
 * This module provides a React hook to manage authentication state within a component.
 *
 * Hexagonal Architecture Principles:
 * - This hook acts as an inbound adapter (driving port), exposing authentication state and actions to the UI layer.
 * - The login/logout actions can be extended to emit domain events (e.g., UserLoggedIn, UserLoggedOut) for event-driven microservices.
 * - Outbound adapters may be integrated to broadcast authentication events to other parts of the system.
 */

/**
 * useAuth React hook for managing authentication state.
 * Acts as an inbound adapter (hexagonal port) to the authentication domain.
 * Can be extended to trigger 'UserLoggedIn' and 'UserLoggedOut' events (event-driven principle).
 *
 * @function useAuth
 * @returns {Object} Authentication state and actions:
 *   - token: Current authentication token (string or null)
 *   - login: Function to set token (login user)
 *   - logout: Function to clear token (logout user)
 *   - isAuthenticated: Boolean indicating if user is authenticated
 */
export function useAuth() {
  const [token, setToken] = useState(null);

  const login = (access_token) => setToken(access_token);
  const logout = () => setToken(null);

  return { token, login, logout, isAuthenticated: Boolean(token) };
}