import React, { useEffect, useState } from 'react';
import { fetchProducts, deleteProduct } from '../adapters/productApi';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const loadProducts = async () => {
    setLoading(true);
    // Retrieve the token from localStorage
    const token = localStorage.getItem('access_token');
    console.log('ProductList token:', token); // For debugging
    try {
      const data = await fetchProducts(token); // Pass token here!
      setProducts(data);
      setError('');
    } catch (err) {
      setError('Could not fetch products.');
    }
    setLoading(false);
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleDelete = async (id) => {
    // Retrieve the token from localStorage
    const token = localStorage.getItem('access_token');
    try {
      await deleteProduct(id, token); // Pass token here!
      loadProducts();
    } catch (err) {
      setError('Could not delete product.');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>Products</h2>
      <ul>
        {products.map(p => (
          <li key={p.id}>
            {p.name} - ${p.price}
            <button onClick={() => handleDelete(p.id)}>Delete</button>
          </li>
        ))}
      </ul>
      {/* Add links/buttons for Create/Edit as needed */}
    </div>
  );
}

export default ProductList;