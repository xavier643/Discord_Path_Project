import React from "react";
import { logout } from "../lib/api";
import { useOutletContext } from "react-router-dom";

export default function Dashboard() {
  const { me } = useOutletContext();

  if (!me?.user) {
    return (
      <LoadingCard
        title="Loading dashboard…"
        message="Fetching your Discord data."
      />
    );
  }

  console.log(me);
  console.log(me.roles);
  console.log(me.roles["1421220625044738170"]);
  console.log(me.roles["1421220625044738170"].roles);

  for (const role in me.roles["1421220625044738170"].roles) {
    console.log(me.roles["1421220625044738170"].roles[role].name);
  }

  return (
    <div className="container">
      <div className="dashboard__header">
        <h1 className="dashboard__title">Hi, {me.user.username}</h1>
        <button className="btn btn-secondary" onClick={logout}>
          Logout
        </button>
      </div>

      <p className="muted">Servers using this bot that you are a member of:</p>
      {/* create list of guilds, if any. Then create a list of roles within said guild */}
      {me.authorized_guilds.length === 0 ? (
        <p>No authorized servers found.</p>
      ) : (
        <ul className="list">
          {me.authorized_guilds.map((g) => (
            <li key={g.id}>
              {g.name}
              <ul className="list">
                {me.roles?.[g.id]?.roles?.length > 0 ? (
                  me.roles[g.id].roles.map((r) => <li key={r.id}>{r.name}</li>)
                ) : (
                  <li className="muted">No roles found.</li>
                )}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
