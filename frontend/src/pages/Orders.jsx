import { useEffect, useState } from "react";
import { apiDelete, apiGet, apiPost, apiPut } from "../api/client";

export default function Orders() {
    const [orders, setOrders] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [products, setProducts] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");
    const [editingOrderId, setEditingOrderId] = useState(null);
    const [newItem, setNewItem] = useState({ product_id: "", quantity: 1 });

    function showMessage(text, type = "success") {
        setMessage(text);
        setMessageType(type);

        setTimeout(() => {
            setMessage("");
            setMessageType("");
        }, 12000);
    }

    const [form, setForm] = useState({
        customer_id: "",
        order_date: "",
        items: [{ product_id: "", quantity: 1 }],
    });

    async function loadData() {
        try {
            setLoading(true);
            setError("");

            const [ordersData, customersData, productsData] = await Promise.all([
                apiGet("/orders"),
                apiGet("/customers"),
                apiGet("/products"),
            ]);

            setOrders(ordersData);
            setCustomers(customersData);
            setProducts(productsData);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadData();
    }, []);

    function updateItem(index, field, value) {
        const updatedItems = [...form.items];
        updatedItems[index][field] = value;
        setForm({ ...form, items: updatedItems });
    }

    function addItem() {
        setForm({
            ...form,
            items: [...form.items, { product_id: "", quantity: 1 }],
        });
    }

    function removeItem(index) {
        if (form.items.length === 1) return;

        const updatedItems = form.items.filter((_, itemIndex) => itemIndex !== index);
        setForm({ ...form, items: updatedItems });
    }

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            setError("");

            if (editingOrderId) {
                await apiPut(`/orders/${editingOrderId}`, {
                    customer_id: Number(form.customer_id),
                    order_date: form.order_date,
                });
                showMessage("Order updated successfully");
                setEditingOrderId(null);
                setForm({
                    customer_id: "",
                    order_date: "",
                    items: [{ product_id: "", quantity: 1 }],
                });
            } else {
                await apiPost("/orders", {
                    customer_id: Number(form.customer_id),
                    order_date: form.order_date,
                    items: form.items.map((item) => ({
                        product_id: Number(item.product_id),
                        quantity: Number(item.quantity),
                    })),
                });
                setForm({
                    customer_id: "",
                    order_date: "",
                    items: [{ product_id: "", quantity: 1 }],
                });
                showMessage("Order created successfully");
            }
            await loadData();
        } catch (err) {
            showMessage(err.message, "error");
        }
    }

    async function handleDelete(orderId) {
        try {
            setError("");
            await apiDelete(`/orders/${orderId}`);
            showMessage("Order deleted successfully");
            if (editingOrderId === orderId) {
                setEditingOrderId(null);
            }
            await loadData();
        } catch (err) {
            showMessage(err.message, "error");
        }
    }

    async function handleRemoveItem(orderId, itemId) {
        try {
            await apiDelete(`/orders/${orderId}/items/${itemId}`);
            showMessage("Item removed from order");
            await loadData();
        } catch (err) {
            showMessage(err.message, "error");
        }
    }

    async function handleAddItem(orderId) {
        try {
            if (!newItem.product_id) {
                throw new Error("Please select a product");
            }
            await apiPost(`/orders/${orderId}/items`, {
                product_id: Number(newItem.product_id),
                quantity: Number(newItem.quantity),
            });
            setNewItem({ product_id: "", quantity: 1 });
            showMessage("Item added to order");
            await loadData();
        } catch (err) {
            showMessage(err.message, "error");
        }
    }

    function handleEdit(order) {
        setEditingOrderId(order.order_id);
        setForm({
            customer_id: order.customer_id,
            order_date: order.order_date,
            items: [],
        });
    }

    function handleCancelEdit() {
        setEditingOrderId(null);
        setForm({
            customer_id: "",
            order_date: "",
            items: [{ product_id: "", quantity: 1 }],
        });
    }

    const customerMap = Object.fromEntries(
        customers.map((customer) => [customer.customer_id, customer.name])
    );

    const productMap = Object.fromEntries(
        products.map((product) => [product.product_id, product.name])
    );

    return (
        <div className="page">
            <h2>Orders</h2>

            {message && (
                <div className={`alert ${messageType === "error" ? "alert-error" : "alert-success"}`}>
                    {message}
                </div>
            )}

            <form onSubmit={handleSubmit} className="form-card">
                <h3 style={{ width: "100%", textAlign: "left", marginBottom: "16px" }}>
                    {editingOrderId ? `Edit Order #${editingOrderId}` : "Create Order"}
                </h3>
                <div style={{ display: "flex", gap: "16px", width: "100%", flexWrap: "wrap", marginBottom: "16px" }}>
                    <select
                        value={form.customer_id}
                        onChange={(e) => setForm({ ...form, customer_id: e.target.value })}
                    >
                        <option value="">Select customer</option>
                        {customers.map((customer) => (
                            <option key={customer.customer_id} value={customer.customer_id}>
                                {customer.name}
                            </option>
                        ))}
                    </select>

                    <input
                        type="date"
                        value={form.order_date}
                        onChange={(e) => setForm({ ...form, order_date: e.target.value })}
                    />

                    <button type="submit">
                        {editingOrderId ? "Update Header" : "Create Order"}
                    </button>

                    {editingOrderId && (
                        <button
                            type="button"
                            className="secondary-button"
                            onClick={handleCancelEdit}
                        >
                            Cancel Edit
                        </button>
                    )}
                </div>

                {!editingOrderId && (
                    <div className="items-wrapper">
                        {form.items.map((item, index) => (
                            <div key={index} className="order-item-row">
                                <select
                                    value={item.product_id}
                                    onChange={(e) => updateItem(index, "product_id", e.target.value)}
                                >
                                    <option value="">Select product</option>
                                    {products.map((product) => (
                                        <option key={product.product_id} value={product.product_id}>
                                            {product.name}
                                        </option>
                                    ))}
                                </select>

                                <input
                                    type="number"
                                    min="1"
                                    value={item.quantity}
                                    onChange={(e) => updateItem(index, "quantity", e.target.value)}
                                />

                                <button
                                    type="button"
                                    className="secondary-button"
                                    onClick={() => removeItem(index)}
                                >
                                    Remove
                                </button>
                            </div>
                        ))}
                        <div className="order-actions" style={{ marginTop: "16px" }}>
                            <button type="button" onClick={addItem}>
                                Add Item
                            </button>
                        </div>
                    </div>
                )}
            </form>

            {editingOrderId && (
                <div className="form-card" style={{ flexDirection: "column", alignItems: "flex-start" }}>
                    <h3>Manage Order Items</h3>

                    <div className="editing-items-list" style={{ width: "100%", margin: "16px 0" }}>
                        {orders.find((o) => o.order_id === editingOrderId)?.items.map((item) => (
                            <div
                                key={item.item_id}
                                style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    padding: "12px 0",
                                    borderBottom: "1px solid #e2e8f0",
                                }}
                            >
                                <span>
                                    {productMap[item.product_id] || `Product #${item.product_id}`}{" "}
                                    (Qty: {item.quantity}) —{" "}
                                    {Number(item.total).toLocaleString("en-US", {
                                        style: "currency",
                                        currency: "USD",
                                    })}
                                </span>
                                <button
                                    type="button"
                                    className="danger-button"
                                    style={{ padding: "6px 12px", fontSize: "12px" }}
                                    onClick={() => handleRemoveItem(editingOrderId, item.item_id)}
                                >
                                    Remove Item
                                </button>
                            </div>
                        ))}
                    </div>

                    <div style={{ display: "flex", gap: "16px", width: "100%", flexWrap: "wrap", alignItems: "center" }}>
                        <select
                            value={newItem.product_id}
                            onChange={(e) => setNewItem({ ...newItem, product_id: e.target.value })}
                            style={{ flex: 1 }}
                        >
                            <option value="">Select product to add</option>
                            {products.map((product) => (
                                <option key={product.product_id} value={product.product_id}>
                                    {product.name}
                                </option>
                            ))}
                        </select>

                        <input
                            type="number"
                            min="1"
                            value={newItem.quantity}
                            onChange={(e) => setNewItem({ ...newItem, quantity: e.target.value })}
                            style={{ maxWidth: "120px" }}
                        />

                        <button type="button" onClick={() => handleAddItem(editingOrderId)}>
                            Add Item
                        </button>
                    </div>
                </div>
            )}

            {loading && <p className="loading-text">Loading orders...</p>}

            <table className="data-table">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Date</th>
                        <th>Products</th>
                        <th>Total Items</th>
                        <th>Order Total</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map((order) => {
                        const totalItems = order.items.reduce(
                            (sum, item) => sum + Number(item.quantity),
                            0
                        );

                        const orderTotal = order.items.reduce(
                            (sum, item) => sum + Number(item.total),
                            0
                        );

                        return (
                            <tr key={order.order_id}>
                                <td>{order.order_id}</td>
                                <td>
                                    {customerMap[order.customer_id] || `Customer #${order.customer_id}`}
                                </td>
                                <td>{order.order_date}</td>
                                <td>
                                    <ul className="item-list">
                                        {order.items.map((item) => (
                                            <li key={item.item_id}>
                                                {productMap[item.product_id] || `Product #${item.product_id}`}{" "}
                                                (Qty: {item.quantity})
                                            </li>
                                        ))}
                                    </ul>
                                </td>
                                <td>{totalItems}</td>
                                <td>
                                    {orderTotal.toLocaleString("en-US", {
                                        style: "currency",
                                        currency: "USD",
                                    })}
                                </td>
                                <td>
                                    <div className="action-buttons">
                                        <button onClick={() => handleEdit(order)}>
                                            Edit
                                        </button>
                                        <button
                                            className="danger-button"
                                            onClick={() => handleDelete(order.order_id)}
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}