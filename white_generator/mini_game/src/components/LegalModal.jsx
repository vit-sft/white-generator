import { useState } from "react";

export default function LegalModal({
  legal,
  font,
  onClose,
  showResume,
  onResume,
  buttonConfig,
}) {
  const [tab, setTab] = useState("terms");

  const buttonVars = buttonConfig
    ? {
        "--button-gradient-start": buttonConfig.gradientStart,
        "--button-gradient-end": buttonConfig.gradientEnd,
        "--button-border-color": buttonConfig.borderColor,
      }
    : {};

  return (
    <div
      className="legal-overlay"
      onClick={(e) => e.stopPropagation()}
      style={{ fontFamily: font }}
    >
      <div className="legal-card legal-card-tall">
        <div className="legal-tabs">
          <button
            className={tab === "terms" ? "legal-tab active" : "legal-tab"}
            style={buttonVars}
            onClick={() => setTab("terms")}
          >
            Terms and Policies
          </button>
          <button
            className={tab === "rules" ? "legal-tab active" : "legal-tab"}
            style={buttonVars}
            onClick={() => setTab("rules")}
          >
            Rules
          </button>
          {onClose && (
            <button className="legal-close" onClick={onClose}>
              ✕
            </button>
          )}
        </div>

        <div className="legal-body">
          {tab === "terms" ? (
            <>
            <h3>Privacy</h3>
            <p className="content">
              {legal.termsAndPolicies.privacyText}
              {legal.termsAndPolicies.privacyPolicyLinkText && (
                <>
                  {" "}
                  <a
                    href={legal.termsAndPolicies.privacyPolicyUrl || "#"}
                    target={legal.termsAndPolicies.privacyPolicyUrl ? "_blank" : "_self"}
                    rel="noopener noreferrer"
                    className="legal-link"
                    onClick={(e) => {
                      if (!legal.termsAndPolicies.privacyPolicyUrl) {
                        e.preventDefault();
                      }
                    }}
                  >
                    {legal.termsAndPolicies.privacyPolicyLinkText}
                  </a>
                </>
              )}
            </p>
              <h3>Contact</h3>
              <p className="content">{legal.termsAndPolicies.contactText}</p>
              <h3>Responsible Use</h3>
              <p className="content">
                {legal.termsAndPolicies.responsibleUseText}
              </p>
              <h3>Terms</h3>
              <p className="content">{legal.termsAndPolicies.termsText}</p>
            </>
          ) : (
            <>
              <h3>Rules</h3>
              <p className="content">{legal.rules.text}</p>
            </>
          )}
        </div>

        {showResume && (
          <div className="legal-footer">
            <button
              className="legal-btn legal-btn-primary"
              style={buttonVars}
              onClick={onResume}
            >
              {buttonConfig.resumeLabel || "Resume"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
