import { NavLink } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="navbar">
            <h1>SalesCore</h1>
            <div className="nav-links">
                <NavLink to="/dashboard">Dashboard</NavLink>
                <NavLink to="/customers">Customers</NavLink>
                <NavLink to="/products">Products</NavLink>
                <NavLink to="/orders">Orders</NavLink>
            </div>
        </nav>
    );
}