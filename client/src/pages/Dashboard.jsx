import React from "react";
import { logout } from "../lib/api";
import { useOutletContext } from "react-router-dom";

export default function Dashboard() {
  const { me } = useOutletContext();

  if (!me?.user) return <div>Loading...</div>;

  return (
    <div style={wrap}>
      <div style={row}>
        <h1 style={{ margin: 0 }}>Hi, {me.user.username}</h1>
        <button style={secondary} onClick={logout}>
          Logout
        </button>
      </div>
      <p>Servers using this bot that you are a member of:</p>
      <ul>
        <ul>
          {(me.authorized_guilds ?? []).length > 0 ? (
            me.authorized_guilds.map((g) => <li key={g.id}>{g.name}</li>)
          ) : (
            <li>No authorized guilds</li>
          )}
        </ul>
      </ul>
    </div>
  );
}

const wrap = {
  maxWidth: 720,
  margin: "40px auto",
  fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial",
};

const row = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  marginBottom: "1rem",
};

const secondary = {
  background: "#eef2ff",
  color: "#111827",
  border: 0,
  borderRadius: 10,
  padding: "8px 12px",
  fontWeight: 600,
  cursor: "pointer",
};
