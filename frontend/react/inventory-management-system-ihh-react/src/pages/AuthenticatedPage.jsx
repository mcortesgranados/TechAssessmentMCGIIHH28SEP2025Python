/**
 * AUTHENTICATED PAGE component.
 *
 * This component renders a message indicating successful authentication.
 *
 * Hexagonal Architecture Principles:
 * - Acts as an inbound adapter (driving port) presenting authenticated state to the UI.
 * - Can be extended to trigger or react to domain events (e.g., UserAuthenticated) for event-driven microservices.
 * - Serves as a boundary between the UI and authentication domain logic.
 */

/**
 * AuthenticatedPage React component.
 * Displays a message confirming successful login.
 * Can be extended to include navigation to other protected resources (e.g., Products CRUD page).
 *
 * @component
 * @returns {JSX.Element} UI for authenticated state.
 */
import React from 'react';
import { Link } from 'react-router-dom';

function AuthenticatedPage() {
  return (
    <div>
      <h2>Authenticated!</h2>
      <p>You are successfully logged in.</p>
      {/* Link to Products CRUD page */}
      {/* Example: <Link to="/products">Go to Products</Link> */}
    </div>
  );
}

export default AuthenticatedPage;