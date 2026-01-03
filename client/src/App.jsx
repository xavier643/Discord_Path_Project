import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import NotFound from "./pages/NotFound.jsx";

import RequireAuth from "./guards/RequireAuth.jsx";
import ProtectedLayout from "./layouts/ProtectedLayout.jsx";
import PublicLayout from "./layouts/PublicLayout.jsx";

export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route element={<PublicLayout />}>
        <Route path="/" element={<Home />} />
      </Route>

      <Route path="/login" element={<Login />} />

      {/* Protected route group */}
      <Route
        path="/app"
        element={
          <RequireAuth>
            <ProtectedLayout />
          </RequireAuth>
        }
      >
        {/* /app -> /app/dashboard */}
        <Route index element={<Navigate to="dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
      </Route>

      {/* Catch-all */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
