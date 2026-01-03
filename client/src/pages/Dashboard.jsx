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

  return (
    <div className="container">
      <div className="dashboard__header">
        <h1 className="dashboard__title">Hi, {me.user.username}</h1>
        <button className="btn btn-secondary" onClick={logout}>
          Logout
        </button>
      </div>
    </div>
  );
}
