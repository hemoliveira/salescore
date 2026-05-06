import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="navbar">
            <h1 style={{ color: "white" }}>SalesCore</h1>
            <div className="nav-links">
                <Link to="/customers">Customers</Link>
                <Link to="/products">Products</Link>
                <Link to="/orders">Orders</Link>
            </div>
        </nav>
    );
}