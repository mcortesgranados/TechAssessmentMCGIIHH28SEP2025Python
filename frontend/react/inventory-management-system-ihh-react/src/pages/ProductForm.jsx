import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

function ProductForm({ products, onSave }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const editing = Boolean(id);
  const productToEdit = editing ? products.find(p => String(p.id) === id) : { name: '', price: '' };
  const [name, setName] = useState(productToEdit ? productToEdit.name : '');
  const [price, setPrice] = useState(productToEdit ? productToEdit.price : '');

  useEffect(() => {
    if (editing && !productToEdit) navigate('/');
  }, [editing, productToEdit, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onSave(editing ? id : undefined, { name, price });
    navigate('/');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{editing ? 'Edit Product' : 'Add Product'}</h2>
      <input value={name} onChange={e => setName(e.target.value)} placeholder="Name" required />
      <input value={price} onChange={e => setPrice(e.target.value)} placeholder="Price" required type="number" />
      <button type="submit">{editing ? 'Update' : 'Create'}</button>
    </form>
  );
}

export default ProductForm;