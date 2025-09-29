import React, { useEffect, useState } from 'react';
import { fetchProducts, updateProduct } from '../adapters/productApi';
import { useParams, useNavigate } from 'react-router-dom';

function ProductEdit() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [formData, setFormData] = useState({});
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    // If you have fetchProductById, use that; else filter from fetchProducts
    fetchProducts(token)
      .then(products => {
        const prod = products.find(p => String(p.id) === String(id));
        if (prod) {
          setProduct(prod);
          setFormData(prod);
        } else {
          setError('Product not found');
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Could not load product.');
        setLoading(false);
      });
  }, [id]);

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(fd => ({ ...fd, [name]: value }));
  };

  const handleUpdateSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('access_token');
    try {
      await updateProduct(id, formData, token);
      navigate('/products');
    } catch {
      setError('Could not update product.');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!product) return null;

  const allKeys = Object.keys(product);

  return (
    <div style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <style>{`
        .edit-form { background: #fafafa; border: 1px solid #ddd; padding: 16px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .edit-form label { display: block; margin-bottom: 6px; font-weight: 500; }
        .edit-form input { width: 100%; padding: 7px 10px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 1em; }
        .form-btn { background: #1976d2; color: #fff; border: none; padding: 7px 14px; border-radius: 4px; cursor: pointer; font-size: 1em; margin-right: 8px; }
      `}</style>
      <h2>Edit Product</h2>
      <form className="edit-form" onSubmit={handleUpdateSubmit}>
        {allKeys.map(key => (
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
        <button type="button" className="form-btn" onClick={() => navigate('/products')}>Cancel</button>
      </form>
    </div>
  );
}

export default ProductEdit;