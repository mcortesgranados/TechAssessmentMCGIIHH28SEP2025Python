/**
 * PRODUCTS HOOK module.
 *
 * This module provides a React hook for managing product data from the backend.
 *
 * Hexagonal Architecture Principles:
 * - This hook acts as an inbound adapter (driving port), exposing product state and actions to the UI layer.
 * - Product actions (add/edit/remove) can be extended to emit domain events (e.g., ProductAdded, ProductEdited, ProductRemoved) for event-driven microservices.
 * - Outbound adapters may be integrated to broadcast product-related events to other parts of the system.
 * - Makes use of product API functions as outbound adapters to interact with the backend.
 */

/**
 * useProducts React hook for managing product state.
 * Acts as an inbound adapter (hexagonal port) to the products domain.
 * Can be extended to trigger domain events (event-driven principle) on add/edit/remove operations.
 *
 * @function useProducts
 * @returns {Object} Products state and CRUD actions:
 *   - products: Array of product objects
 *   - loading: Boolean indicating if loading is in progress
 *   - error: Error message string (empty if no error)
 *   - addProduct: Function to add a new product
 *   - editProduct: Function to edit/update an existing product
 *   - removeProduct: Function to delete a product
 */
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