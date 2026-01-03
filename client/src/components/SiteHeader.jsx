import React from "react";
import { NavLink } from "react-router-dom";

export default function SiteHeader() {
  return (
    <header className="header">
      <div className="header__inner">
        <div className="brand">X</div>

        <nav className="nav">
          <NavLink to="/">Home</NavLink>
          {/* <a href="#projects">Projects</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a> */}
        </nav>
      </div>
    </header>
  );
}
