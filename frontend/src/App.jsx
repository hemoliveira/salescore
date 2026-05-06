import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Customers from "./pages/Customers";
import Products from "./pages/Products";
import Orders from "./pages/Orders";
import "./styles/global.css";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/customers" element={<Customers />} />
          <Route path="/products" element={<Products />} />
          <Route path="/orders" element={<Orders />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
