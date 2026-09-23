import { useEffect, useState } from "react";

const STORAGE_KEY = "towerCookiesAccepted";

export default function CookieModal({ cookies, font, buttonConfig }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const accepted = localStorage.getItem(STORAGE_KEY);
    if (!accepted) setVisible(true);
  }, []);

  function handleChoice(value) {
    localStorage.setItem(STORAGE_KEY, value);
    setVisible(false);
  }

  if (!visible) return null;

  const buttonVars = {
    "--button-gradient-start": buttonConfig.gradientStart,
    "--button-gradient-end": buttonConfig.gradientEnd,
    "--button-border-color": buttonConfig.borderColor,
  };

  return (
    <div
      className="cookie-overlay"
      onClick={(e) => e.stopPropagation()}
      style={{
        background: cookies.backgroundColor || "#1e293b",
        fontFamily: font,
      }}
    >
      <div className="legal-card">
        <div className="cookie-body">
          <p className="content">{cookies.text}</p>
          <div className="legal-btn-row">
            <button
              className="legal-btn legal-btn-primary"
              style={buttonVars}
              onClick={() => handleChoice("all")}
            >
              {cookies.acceptAllLabel || "Accept All"}
            </button>
            <button
              className="legal-btn legal-btn-secondary"
              onClick={() => handleChoice("necessary")}
            >
              {cookies.acceptNecessaryLabel || "Necessary Only"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
