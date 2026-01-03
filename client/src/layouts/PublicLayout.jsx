import React from "react";
import { Outlet, NavLink } from "react-router-dom";

import SiteFooter from "../components/SiteFooter";
import SiteHeader from "../components/SiteHeader";

export default function PublicLayout() {
  return (
    <div className="page">
      <SiteHeader />

      <main className="main">
        <Outlet />
      </main>

      <SiteFooter />
    </div>
  );
}
