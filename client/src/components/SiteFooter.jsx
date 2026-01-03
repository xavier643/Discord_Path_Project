import React from "react";

export default function SiteFooter() {
  return (
    <footer className="footer">
      <div className="footer__inner">
        <div className="footer__left">
          <div className="brand" aria-label="Site logo">
            X
          </div>

          <div className="footer__icons">
            <a
              className="iconlink"
              href="https://github.com/YOUR_GITHUB"
              target="_blank"
              rel="noreferrer"
              aria-label="GitHub"
              title="GitHub"
            >
              GH
            </a>
            <a
              className="iconlink"
              href="https://www.linkedin.com/in/YOUR_LINKEDIN"
              target="_blank"
              rel="noreferrer"
              aria-label="LinkedIn"
              title="LinkedIn"
            >
              in
            </a>
          </div>
        </div>

        <div className="footer__middle">
          <div className="muted footer__label">Built with</div>
          <div className="footer__stack">
            <span className="chip">React</span>
            <span className="chip">Vite</span>
            <span className="chip">React Router</span>
            <span className="chip">SCSS</span>
          </div>
        </div>

        <div className="footer__right muted">
          © {new Date().getFullYear()} Xavier
        </div>
      </div>
    </footer>
  );
}
