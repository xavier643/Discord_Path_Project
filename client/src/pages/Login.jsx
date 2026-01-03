import React from "react";
import { loginWithDiscord } from "../lib/api";

export default function Login() {
  return (
    <div className="card">
      <h1>Welcome</h1>
      <p>Log in with Discord to continue.</p>
      <button className="btn btn-primary" onClick={loginWithDiscord}>
        Login with Discord
      </button>
    </div>
  );
}
