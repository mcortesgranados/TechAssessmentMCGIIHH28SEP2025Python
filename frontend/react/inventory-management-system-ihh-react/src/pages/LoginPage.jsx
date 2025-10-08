/**
 * LOGIN PAGE component.
 *
 * This component provides a user interface for authenticating users.
 *
 * Hexagonal Architecture Principles:
 * - Acts as an inbound adapter (driving port), presenting authentication actions to the UI layer.
 * - The login process integrates with the authentication domain via the loginUser API function (outbound port).
 * - Can be extended to trigger domain events (e.g., UserLoginAttempted, UserLoggedIn) for event-driven microservices.
 * - Serves as a boundary between the UI and authentication domain logic.
 */

/**
 * LoginPage React component.
 * Renders a login form and handles authentication logic.
 * On successful authentication, calls onAuth with access token and navigates to dashboard.
 * Handles error states for failed or unauthorized login attempts.
 *
 * @component
 * @param {Object} props
 * @param {function} props.onAuth - Callback to handle successful authentication (receives access token).
 * @returns {JSX.Element} Login form UI.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../adapters/authApi';

function LoginPage({ onAuth }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await loginUser({ username, password });
      if (response.status === 200) {
        const data = await response.json();
        onAuth(data.access_token);
        navigate('/dashboard');
      } else if (response.status === 401) {
        setError('Unauthorized: Invalid username or password.');
      } else {
        const data = await response.json();
        setError(data.detail || `Error: ${response.status}`);
      }
    } catch (err) {
      setError('Network error');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>
      <input type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" required />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required />
      <button type="submit">Login</button>
      {/* Error message shown below the button */}
      {error && <div style={{color:'red', marginTop:'10px'}}>{error}</div>}
    </form>
  );
}

export default LoginPage;