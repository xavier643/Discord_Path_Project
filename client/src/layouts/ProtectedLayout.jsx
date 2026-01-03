import React from "react";
import { Outlet } from "react-router-dom";

export default function ProtectedLayout({ me }) {
  // put your shared app shell here later (nav, header, etc)
  return <Outlet context={{ me }} />;
}
