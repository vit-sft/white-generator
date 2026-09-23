import { useState } from "react";
import LegalModal from "./LegalModal";

export default function StartScreen({ legal, font, onStart, buttonConfig }) {
  const [showLegal, setShowLegal] = useState(false);

  const buttonVars = {
    "--button-gradient-start": buttonConfig.gradientStart,
    "--button-gradient-end": buttonConfig.gradientEnd,
    "--button-border-color": buttonConfig.borderColor,
  };

  return (
    <div
      className="start-overlay"
      onClick={(e) => e.stopPropagation()}
      style={{ fontFamily: font }}
    >
      {showLegal ? (
        <LegalModal
          legal={legal}
          font={font}
          onClose={() => setShowLegal(false)}
          showResume={false}
          buttonConfig={buttonConfig}
        />
      ) : (
        <div className="legal-card start-card">
          <h2 className="start-title">{legal.gameTitle}</h2>
          <button
            className="legal-btn legal-btn-primary start-play-btn"
            style={buttonVars}
            onClick={onStart}
          >
            {buttonConfig.startLabel || "Start"}
          </button>
          <button className="start-link" onClick={() => setShowLegal(true)}>
            Terms & Rules
          </button>
        </div>
      )}
    </div>
  );
}
