import { useEffect, useState } from "react";
import { apiDelete, apiGet, apiPost, apiPut } from "../api/client";

export default function Customers() {
    const [customers, setCustomers] = useState([]);
    const [form, setForm] = useState({ name: "", city: "" });
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

    async function loadCustomers() {
        try {
            setLoading(true);
            setError("");
            const data = await apiGet("/customers");
            setCustomers(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadCustomers();
    }, []);

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            if (editingId) {
                await apiPut(`/customers/${editingId}`, form);
                showMessage("Customer updated successfully");
            } else {
                await apiPost("/customers", form);
                showMessage("Customer created successfully");
            }

            setEditingId(null);
            setForm({ name: "", city: "" });

            await loadCustomers();
        } catch (err) {
            showMessage(err.message, "error");
        }
    }

    async function handleDelete(customerId) {
        try {
            await apiDelete(`/customers/${customerId}`);
            showMessage("Customer deleted successfully");
            await loadCustomers();
        } catch (err) {
            showMessage(err.message, "error");
        }
    }

    function handleEdit(customer) {
        setEditingId(customer.customer_id);
        setForm({
            name: customer.name,
            city: customer.city || "",
        });
    }

    function handleCancelEdit() {
        setEditingId(null);
        setForm({ name: "", city: "" });
    }

    return (
        <div className="page">
            <h2>Customers</h2>

            {message && (
                <div className={`alert ${messageType === "error" ? "alert-error" : "alert-success"}`}>
                    {message}
                </div>
            )}

            <form onSubmit={handleSubmit} className="form-card">
                <input
                    type="text"
                    placeholder="Customer name"
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
                <input
                    type="text"
                    placeholder="City"
                    value={form.city}
                    onChange={(e) => setForm({ ...form, city: e.target.value })}
                />
                <button type="submit">
                    {editingId ? "Update Customer" : "Create Customer"}
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

            {loading && <p className="loading-text">Loading customers...</p>}

            <table className="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>City</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {customers.map((customer) => (
                        <tr key={customer.customer_id}>
                            <td>{customer.customer_id}</td>
                            <td>{customer.name}</td>
                            <td>{customer.city || "-"}</td>
                            <td>
                                <div className="action-buttons">
                                    <button onClick={() => handleEdit(customer)}>
                                        Edit
                                    </button>
                                    &nbsp;
                                    <button
                                        className="danger-button"
                                        onClick={() => handleDelete(customer.customer_id)}
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