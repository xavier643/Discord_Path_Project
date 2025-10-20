import React from "react";
import { loginWithDiscord } from "../lib/api";

export default function Login() {
  return (
    <div style={card}>
      <h1>Welcome</h1>
      <p>Log in with Discord to continue.</p>
      <button style={primary} onClick={loginWithDiscord}>
        Login with Discord
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
