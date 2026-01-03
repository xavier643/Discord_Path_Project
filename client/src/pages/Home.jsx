import React from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div style={card}>
      <h1>Welcome to my page</h1>
      <p>This is a simple public homepage.</p>

      <button style={primary} onClick={() => navigate("/app/dashboard")}>
        View Example Project
      </button>
    </div>
  );
}

const card = {
  maxWidth: 520,
  margin: "40px auto",
  padding: 24,
  border: "1px solid #e5e7eb",
  borderRadius: 14,
  boxShadow: "0 2px 10px rgba(0,0,0,.06)",
  fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial",
  textAlign: "center",
};

const primary = {
  background: "#5865F2",
  color: "#fff",
  border: 0,
  borderRadius: 10,
  padding: "10px 14px",
  fontWeight: 600,
  cursor: "pointer",
};
