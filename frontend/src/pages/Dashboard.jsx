import { useEffect, useState } from "react";
import { apiGet } from "../api/client";

export default function Dashboard() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadDashboard() {
        try {
            setLoading(true);
            setError("");
            const dashboardData = await apiGet("/dashboard");
            setData(dashboardData);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadDashboard();
    }, []);

    if (loading) return <div className="loading-text">Loading dashboard...</div>;
    if (error) return <div className="error">{error}</div>;
    if (!data) return null;

    const { summary, categories, top_customer } = data;

    return (
        <div className="page dashboard">
            <h2>Monthly Dashboard</h2>

            <div className="dashboard-grid">
                <div className="card kpi-card">
                    <span className="card-icon">💰</span>
                    <div className="card-info">
                        <h3>Monthly Revenue</h3>
                        <p className="kpi-value">{summary.monthly_revenue || "$ 0.00"}</p>
                    </div>
                </div>

                <div className="card kpi-card">
                    <span className="card-icon">📦</span>
                    <div className="card-info">
                        <h3>Total Orders</h3>
                        <p className="kpi-value">{summary.total_orders || 0}</p>
                    </div>
                </div>

                {top_customer && (
                    <div className="card kpi-card highlight-card">
                        <span className="card-icon">🏆</span>
                        <div className="card-info">
                            <h3>Top Customer</h3>
                            <p className="kpi-name">{top_customer.customer}</p>
                            <p className="kpi-sub">{top_customer.total_spent}</p>
                        </div>
                    </div>
                )}
            </div>

            <div className="dashboard-sections">
                <div className="card section-card">
                    <h3>Sales by Category</h3>
                    {categories.length === 0 ? (
                        <p className="no-data">No sales recorded this month.</p>
                    ) : (
                        <div className="category-list">
                            {categories.map((cat, idx) => (
                                <div key={idx} className="category-item">
                                    <span className="category-name">
                                        {cat.category || "Uncategorized"}
                                    </span>
                                    <span className="category-val">{cat.revenue}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

