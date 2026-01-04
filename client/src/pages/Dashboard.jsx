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
      {/* <RolesList roles={me.roles} /> */}
      <div className="dashboard__content">
        <h2 className="dashboard__subtitle">Are you the Owner?</h2>
        <p>
          {me.is_owner
            ? "Yes, you are the owner of the guild."
            : "No, you are not the owner of the guild."}
        </p>
        <h2 className="dashboard__subtitle">Your Roles</h2>
        <ul className="roles__list">
          {me.roles && me.roles.length > 0 ? (
            me.roles.map((role) => (
              <li key={role.id} className="roles__item">
                {role.name}
              </li>
            ))
          ) : (
            <li className="roles__item muted">No roles assigned</li>
          )}
        </ul>
      </div>
    </div>
  );
}
