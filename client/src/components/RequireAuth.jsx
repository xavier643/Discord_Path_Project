import React from "react";
import { useEffect, useState } from "react";
import { useLocation, Navigate } from "react-router-dom";
import { apiGet } from "../lib/api";

export default function RequireAuth({ children }) {
  const [state, setState] = useState({ loading: true, me: null });
  const loc = useLocation();

  useEffect(() => {
    let isMounted = true;
    (async () => {
      const r = await apiGet("/me");
      if (!isMounted) return;
      if (r.status === 401) setState({ loading: false, me: null });
      else if (!r.ok) setState({ loading: false, me: null });
      else setState({ loading: false, me: await r.json() });
    })();
    return () => {
      isMounted = false;
    };
  }, [loc.key]);

  if (state.loading)
    return <div style={{ padding: 24 }}>Checking session…</div>;
  if (!state.me) return <Navigate to="/login" replace />;

  return React.cloneElement(children, { me: state.me });
}
