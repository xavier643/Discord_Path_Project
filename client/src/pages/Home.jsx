import React from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <section className="hero" id="hero">
      <div className="hero__inner">
        <h1 className="hero__title">Hi, I'm Xavier</h1>
        <p className="hero__subtitle">
          I build backend systems and I'm leveling up my front end. This site is
          my playground and portfolio.
        </p>

        <div className="hero__actions">
          <button
            className="btn btn-primary"
            onClick={() => navigate("/app/dashboard")}
          >
            View App
          </button>
          {/* <a className="btn btn-secondary" href="#projects">
            Projects
          </a> */}
        </div>

        <p className="hero__note muted">
          Work in progress — I'm actively improving layout, styling, and
          content.
        </p>
      </div>
    </section>
  );
}
