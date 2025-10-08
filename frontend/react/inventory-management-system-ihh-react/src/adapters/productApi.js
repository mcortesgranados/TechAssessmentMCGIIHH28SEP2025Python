/**
 * PRODUCTS API module.
 *
 * This module provides functions to interact with the Products microservice backend.
 *
 * Hexagonal Architecture Principles:
 * - These functions serve as inbound adapters (driving ports), providing an interface to the backend via HTTP.
 * - Each mutation (create/update/delete) can be extended to emit domain events, supporting event-driven (SOLID) microservices.
 * - Outbound adapters can be added to publish events (e.g., ProductCreated, ProductUpdated, ProductDeleted).
 * - Adjust API_URL as needed for your backend endpoint.
 */

/**
 * The base URL for the products API.
 * Acts as the entry point for API integration.
 * @constant
 * @type {string}
 */
const API_URL = 'http://localhost:8001/products'; // Adjust to your backend

/**
 * Fetches all products from the backend.
 * Acts as an inbound adapter (hexagonal port).
 * Can be extended to publish 'ProductsFetched' events.
 *
 * @async
 * @function fetchProducts
 * @param {string} token - Bearer token for authorization.
 * @returns {Promise<Array>} Resolves to an array of product objects.
 * @throws {Error} If the fetch operation fails.
 */
export async function fetchProducts(token) {
  console.log('MCG fetchProducts called with token:', token); // Log the token for debugging

  const response = await fetch(API_URL, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  if (!response.ok) throw new Error('Failed to fetch products');
  return response.json();
}

/**
 * Creates a new product in the backend.
 * Acts as an inbound adapter (hexagonal port).
 * Should trigger a 'ProductCreated' event (event-driven principle).
 *
 * @async
 * @function createProduct
 * @param {Object} product - Product data.
 * @param {string} token - Bearer token for authorization.
 * @returns {Promise<Object>} Resolves to the created product object.
 * @throws {Error} If the creation fails.
 */
export async function createProduct(product, token) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(product),
  });
  if (!response.ok) throw new Error('Failed to create product');
  return response.json();
}

/**
 * Updates an existing product in the backend.
 * Acts as an inbound adapter (hexagonal port).
 * Should trigger a 'ProductUpdated' event (event-driven principle).
 *
 * @async
 * @function updateProduct
 * @param {string|number} id - The ID of the product to update.
 * @param {Object} product - The updated product data.
 * @param {string} token - Bearer token for authorization.
 * @returns {Promise<Object>} Resolves to the updated product object.
 * @throws {Error} If the update fails.
 */
export async function updateProduct(id, product, token) {
  const response = await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(product),
  });
  if (!response.ok) throw new Error('Failed to update product');
  return response.json();
}

/**
 * Deletes a product from the backend.
 * Acts as an inbound adapter (hexagonal port).
 * Should trigger a 'ProductDeleted' event (event-driven principle).
 *
 * @async
 * @function deleteProduct
 * @param {string|number} id - The ID of the product to delete.
 * @param {string} token - Bearer token for authorization.
 * @returns {Promise<void>} Resolves when the product is deleted.
 * @throws {Error} If the deletion fails.
 */
export async function deleteProduct(id, token) {
  const response = await fetch(`${API_URL}/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (!response.ok) throw new Error('Failed to delete product');
}