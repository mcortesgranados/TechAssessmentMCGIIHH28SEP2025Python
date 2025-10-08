/**
 * AUTH API module.
 *
 * This module provides authentication functions for interacting with the backend.
 *
 * Hexagonal Architecture Principles:
 * - This function serves as an inbound adapter (driving port), providing an interface for authentication via HTTP.
 * - The authentication process can be extended to emit domain events (e.g., UserLoggedIn), supporting event-driven (SOLID) microservices.
 * - Outbound adapters may be added to publish authentication events for other services.
 */

/**
 * Authenticates a user with the backend using username and password.
 * Acts as an inbound adapter (hexagonal port).
 * Should trigger a 'UserLoggedIn' event (event-driven principle) on successful login.
 *
 * @async
 * @function loginUser
 * @param {Object} credentials - User credentials.
 * @param {string} credentials.username - Username for authentication.
 * @param {string} credentials.password - Password for authentication.
 * @returns {Promise<Response>} Resolves to the response object from the backend (contains tokens, user info, etc.).
 */
export async function loginUser({ username, password }) {
  const formBody = new URLSearchParams({
    grant_type: 'password',
    username,
    password,
    scope: '',
    client_id: 'string',
    client_secret: '********', // Replace as needed
  });
  const response = await fetch('http://localhost:8001/auth/login', {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formBody,
  });
  return response;
}