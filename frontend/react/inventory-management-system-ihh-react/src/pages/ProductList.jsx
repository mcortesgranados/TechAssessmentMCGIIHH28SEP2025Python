import React, { useEffect, useState } from 'react';
import { fetchProducts, deleteProduct, updateProduct } from '../adapters/productApi';
import { useNavigate } from 'react-router-dom';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [editingProduct, setEditingProduct] = useState(null);
  const [formData, setFormData] = useState({});

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

  useEffect(() => { loadProducts(); }, []);

  const handleDelete = async (id) => {
    const token = localStorage.getItem('access_token');
    try {
      await deleteProduct(id, token);
      loadProducts();
    } catch (err) {
      setError('Could not delete product.');
    }
  };

  const navigate = useNavigate();

  const handleUpdateClick = (product) => {
    navigate(`/products/edit/${product.id}`);
  };


  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData((fd) => ({
      ...fd,
      [name]: value,
    }));
  };

  const handleUpdateSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('access_token');
    try {
      await updateProduct(editingProduct.id, formData, token);
      setEditingProduct(null);
      loadProducts();
    } catch (err) {
      setError('Could not update product.');
    }
  };

  const handleCancelEdit = () => {
    setEditingProduct(null);
  };

  const allKeys = products.length > 0 ? Object.keys(products[0]) : [];

  return (
    <div style={{ margin: '2rem' }}>
      <style>{`
        .product-table { border-collapse: collapse; width: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.1); font-family: 'Segoe UI', 'Arial', sans-serif; }
        .product-table th, .product-table td { border: 1px solid #eee; padding: 10px 14px; text-align: left; }
        .product-table th { background-color: #f7f7f7; font-weight: 600; }
        .product-table tr { background-color: #fff; transition: background 0.2s; }
        .product-table tr:hover { background-color: #e0f7fa; }
        .action-btn { background: #ff5252; color: #fff; border: none; padding: 7px 14px; border-radius: 4px; cursor: pointer; margin-right: 4px; font-size: 1em; }
        .edit-btn { background: #1976d2; color: #fff; border: none; padding: 7px 14px; border-radius: 4px; cursor: pointer; margin-right: 4px; font-size: 1em; }
        .edit-form { background: #fafafa; border: 1px solid #ddd; padding: 16px; margin-top: 16px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .edit-form label { display: block; margin-bottom: 6px; font-weight: 500; }
        .edit-form input { width: 100%; padding: 7px 10px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 1em; }
        .form-btn { background: #1976d2; color: #fff; border: none; padding: 7px 14px; border-radius: 4px; cursor: pointer; font-size: 1em; margin-right: 8px; }
        .form-btn.cancel { background: #999; }
        .error-msg { color: #d32f2f; font-weight: 500; }
      `}</style>
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
      {/* Inline edit form */}
      {editingProduct && (
        <form className="edit-form" onSubmit={handleUpdateSubmit}>
          <h3>Edit Product</h3>
          {allKeys.map((key) => (
            <div key={key}>
              <label htmlFor={key}>{key.charAt(0).toUpperCase() + key.slice(1)}</label>
              <input
                id={key}
                name={key}
                value={formData[key] ?? ''}
                onChange={handleFormChange}
                disabled={key === 'id'}
              />
            </div>
          ))}
          <button type="submit" className="form-btn">Save</button>
          <button type="button" className="form-btn cancel" onClick={handleCancelEdit}>Cancel</button>
        </form>
      )}
    </div>
  );
}

export default ProductList;