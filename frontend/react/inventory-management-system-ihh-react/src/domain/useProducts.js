import { useState, useEffect } from 'react';
import { fetchProducts, createProduct, updateProduct, deleteProduct } from '../adapters/productApi';

export function useProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  async function loadProducts() {
    setLoading(true);
    try {
      const data = await fetchProducts();
      setProducts(data);
      setError('');
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  }

  async function addProduct(product) {
    await createProduct(product);
    await loadProducts();
  }

  async function editProduct(id, product) {
    await updateProduct(id, product);
    await loadProducts();
  }

  async function removeProduct(id) {
    await deleteProduct(id);
    await loadProducts();
  }

  return { products, loading, error, addProduct, editProduct, removeProduct };
}