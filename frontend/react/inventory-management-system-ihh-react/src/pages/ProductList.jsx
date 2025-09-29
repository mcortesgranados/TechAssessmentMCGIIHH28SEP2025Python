import React, { useEffect, useState } from 'react';
import { fetchProducts, deleteProduct } from '../adapters/productApi';
import { useNavigate } from 'react-router-dom';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const loadProducts = async () => {
    setLoading(true);
    const token = localStorage.getItem('access_token');
    try {
      const data = await fetchProducts(token);
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
    const token = localStorage.getItem('access_token');
    try {
      await deleteProduct(id, token);
      loadProducts();
    } catch (err) {
      setError('Could not delete product.');
    }
  };

  const handleUpdateClick = (product) => {
    navigate(`/products/edit/${product.id}`);
  };

  const allKeys = products.length > 0 ? Object.keys(products[0]) : [];

  return (
    <div style={{ margin: '2rem' }}>
      <style>{`
        .create-btn {
          background: #43a047;
          color: #fff;
          border: none;
          padding: 10px 22px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 1.1em;
          margin-bottom: 18px;
        }
        .product-table {
          border-collapse: collapse;
          width: 100%;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        .product-table th, .product-table td {
          border: 1px solid #eee;
          padding: 10px 14px;
          text-align: left;
        }
        .product-table th {
          background-color: #f7f7f7;
          font-weight: 600;
        }
        .product-table tr {
          background-color: #fff;
          transition: background 0.2s;
        }
        .product-table tr:hover {
          background-color: #e0f7fa;
        }
        .action-btn {
          background: #ff5252;
          color: #fff;
          border: none;
          padding: 7px 14px;
          border-radius: 4px;
          cursor: pointer;
          margin-right: 4px;
          font-size: 1em;
        }
        .edit-btn {
          background: #1976d2;
          color: #fff;
          border: none;
          padding: 7px 14px;
          border-radius: 4px;
          cursor: pointer;
          margin-right: 4px;
          font-size: 1em;
        }
        .error-msg {
          color: #d32f2f;
          font-weight: 500;
        }
      `}</style>
      <button className="create-btn" onClick={() => navigate('/products/create')}>
        Create New Product
      </button>
      <h2>Products</h2>
      {loading && <div>Loading...</div>}
      {error && <div className="error-msg">{error}</div>}
      {!loading && !error && (
        <table className="product-table">
          <thead>
            <tr>
              {allKeys.map((key) => (
                <th key={key}>
                  {key.charAt(0).toUpperCase() + key.slice(1)}
                </th>
              ))}
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id}>
                {allKeys.map((key) => (
                  <td key={key}>
                    {typeof p[key] === 'object' ? JSON.stringify(p[key]) : p[key]}
                  </td>
                ))}
                <td>
                  <button className="action-btn" onClick={() => handleDelete(p.id)}>
                    Delete
                  </button>
                  <button className="edit-btn" onClick={() => handleUpdateClick(p)}>
                    Update
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ProductList;