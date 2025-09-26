import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home.jsx";
import NotFound from "./pages/NotFound.jsx";

export default function App() {
  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: 16 }}>
      <header style={{ display: "flex", gap: 12, marginBottom: 16 }}>
        <Link to="/">Home</Link>
        <a href="/health">/health (static)</a>
      </header>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}
