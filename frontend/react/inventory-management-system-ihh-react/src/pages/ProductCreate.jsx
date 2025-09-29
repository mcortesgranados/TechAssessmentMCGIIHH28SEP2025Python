import React, { useState } from 'react';
import { createProduct } from '../adapters/productApi';
import { useNavigate } from 'react-router-dom';

function ProductCreate() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    stock: ''
  });
  const [error, setError] = useState('');

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(fd => ({ ...fd, [name]: value }));
  };

  const handleCreateSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('access_token');
    try {
      // Convert price and stock to numbers before sending
      const payload = {
        ...formData,
        price: Number(formData.price),
        stock: Number(formData.stock)
      };
      await createProduct(payload, token);
      navigate('/products');
    } catch (err) {
      setError('Could not create product.');
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <style>{`
        .create-form { background: #fafafa; border: 1px solid #ddd; padding: 16px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .create-form label { display: block; margin-bottom: 6px; font-weight: 500; }
        .create-form input { width: 100%; padding: 7px 10px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 1em; }
        .form-btn { background: #43a047; color: #fff; border: none; padding: 7px 14px; border-radius: 4px; cursor: pointer; font-size: 1em; margin-right: 8px; }
      `}</style>
      <h2>Create Product</h2>
      <form className="create-form" onSubmit={handleCreateSubmit}>
        <div>
          <label htmlFor="name">Name</label>
          <input id="name" name="name" value={formData.name} onChange={handleFormChange} required />
        </div>
        <div>
          <label htmlFor="description">Description</label>
          <input id="description" name="description" value={formData.description} onChange={handleFormChange} required />
        </div>
        <div>
          <label htmlFor="price">Price</label>
          <input id="price" name="price" type="number" value={formData.price} onChange={handleFormChange} required />
        </div>
        <div>
          <label htmlFor="stock">Stock</label>
          <input id="stock" name="stock" type="number" value={formData.stock} onChange={handleFormChange} required />
        </div>
        <button type="submit" className="form-btn">Create</button>
        <button type="button" className="form-btn" onClick={() => navigate('/products')}>Cancel</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: '1em' }}>{error}</div>}
    </div>
  );
}

export default ProductCreate;