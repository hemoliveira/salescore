import { useEffect, useState } from "react";
import { apiDelete, apiGet, apiPost, apiPut } from "../api/client";

export default function Products() {
    const [products, setProducts] = useState([]);
    const [form, setForm] = useState({
        name: "",
        category: "",
        price: "",
    });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");
    const [editingId, setEditingId] = useState(null);

    function showMessage(text, type = "success") {
        setMessage(text);
        setMessageType(type);

        setTimeout(() => {
            setMessage("");
            setMessageType("");
        }, 12000);
    }

    async function loadProducts() {
        try {
            setLoading(true);
            setError("");
            const data = await apiGet("/products");
            setProducts(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadProducts();
    }, []);

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            setError("");

            const payload = {
                name: form.name,
                category: form.category || null,
                price: Number(form.price),
            };

            if (editingId) {
                await apiPut(`/products/${editingId}`, payload);
                showMessage("Product updated successfully");
            } else {
                await apiPost("/products", payload);
                showMessage("Product created successfully");
            }

            setEditingId(null);
            setForm({
                name: "",
                category: "",
                price: "",
            });

            await loadProducts();
        } catch (err) {
            showMessage(err.message, "error");
        }
    }

    async function handleDelete(productId) {
        try {
            setError("");
            await apiDelete(`/products/${productId}`);
            showMessage("Product deleted successfully");
            await loadProducts();
        } catch (err) {
            showMessage(err.message, "error");
        }
    }

    function handleEdit(product) {
        setEditingId(product.product_id);
        setForm({
            name: product.name,
            category: product.category || "",
            price: product.price,
        });
    }

    function handleCancelEdit() {
        setEditingId(null);
        setForm({ name: "", category: "", price: "" });
    }

    return (
        <div className="page">
            <h2>Products</h2>

            {message && (
                <div className={`alert ${messageType === "error" ? "alert-error" : "alert-success"}`}>
                    {message}
                </div>
            )}

            <form onSubmit={handleSubmit} className="form-card">
                <input
                    type="text"
                    placeholder="Product name"
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                />

                <input
                    type="text"
                    placeholder="Category"
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                />

                <input
                    type="number"
                    step="0.01"
                    placeholder="Price"
                    value={form.price}
                    onChange={(e) => setForm({ ...form, price: e.target.value })}
                />

                <button type="submit">
                    {editingId ? "Update Product" : "Create Product"}
                </button>

                {editingId && (
                    <button
                        type="button"
                        className="secondary-button"
                        onClick={handleCancelEdit}
                    >
                        Cancel
                    </button>
                )}
            </form>

            {loading && <p className="loading-text">Loading products...</p>}

            <table className="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map((product) => (
                        <tr key={product.product_id}>
                            <td>{product.product_id}</td>
                            <td>{product.name}</td>
                            <td>{product.category || "-"}</td>
                            <td>
                                {Number(product.price).toLocaleString("en-US", {
                                    style: "currency",
                                    currency: "USD",
                                })}
                            </td>
                            <td>
                                <div className="action-buttons">
                                    <button onClick={() => handleEdit(product)}>
                                        Edit
                                    </button>
                                    &nbsp;
                                    <button
                                        className="danger-button"
                                        onClick={() => handleDelete(product.product_id)}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}