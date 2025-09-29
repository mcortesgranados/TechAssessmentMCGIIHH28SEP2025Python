import { Routes, Route } from 'react-router-dom';
import LoginPage from '../pages/LoginPage';
import AuthenticatedPage from '../pages/AuthenticatedPage';
import ProductList from '../pages/ProductList';
import ProductForm from '../pages/ProductForm';

export default function AppRoutes({ auth,products, loading, error, addProduct, editProduct, removeProduct }) {
  return (
    <Routes>
      <Route path="/" element={<LoginPage onAuth={auth.login} />} />
      <Route path="/authenticated" element={<AuthenticatedPage />} />
       <Route path="/" element={<ProductList products={products} loading={loading} error={error} onDelete={removeProduct} />} />
      <Route path="/products/new" element={<ProductForm products={products} onSave={addProduct} />} />
      <Route path="/products/edit/:id" element={<ProductForm products={products} onSave={editProduct} />} />
   </Routes>
  );
}