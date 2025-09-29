import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import ProductList from './pages/ProductList'; // <-- import ProductList
import ProductEdit from './pages/ProductEdit'; // <-- import ProductList
import AuthenticatedPage from './pages/AuthenticatedPage';


function Home() {
  return (
    <div>
      <h2>Welcome to Inventory Management System</h2>
      <Link to="/login">Login</Link>
      <br />
      <Link to="/products">Products</Link> {/* Add link to products page */}
    </div>
  );
}

function Dashboard() {
  return (
    <div>
      <h2>Dashboard (Protected)</h2>
      <p>If you see this, you are logged in!</p>
      <Link to="/">Home</Link>     
      <Link to="/products">Go to Products CRUD</Link>
    </div>
  );
}

function handleAuth(token) {
  console.log('Authenticated! Token:', token);
}

function App() {

  const [token, setToken] = useState(null);

  function handleAuth(token) {
    setToken(token);
    localStorage.setItem('access_token', token);
    console.log('Authenticated! Token:', token);
  }

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginPage onAuth={handleAuth} />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/authenticated" element={<AuthenticatedPage token={token} />} />
            <Route path="/products" element={<ProductList token={token} />} />
            <Route path="/products/edit/:id" element={<ProductEdit />} />
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;