import React from "react";
import PropTypes from "prop-types";

export default function LoadingCard({
  title = "Loading…",
  message = "Please wait.",
}) {
  return (
    <div className="card">
      <h1>{title}</h1>
      <p className="muted">{message}</p>
      <div className="loading-dots" aria-label="Loading" />
    </div>
  );
}

LoadingCard.propTypes = {
  title: PropTypes.string,
  message: PropTypes.string,
};
