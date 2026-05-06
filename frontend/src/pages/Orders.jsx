import { useEffect, useState } from "react";
import { apiDelete, apiGet, apiPost } from "../api/client";

export default function Orders() {
    const [orders, setOrders] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [products, setProducts] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");

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
            await loadData();
        } catch (err) {
            showMessage(err.message, "error");
        }
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
                </div>

                <div className="order-actions">
                    <button type="button" onClick={addItem}>
                        Add Item
                    </button>
                    <button type="submit">Create Order</button>
                </div>
            </form>

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
                                    <button onClick={() => handleDelete(order.order_id)}>
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}