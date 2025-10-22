const banner = document.getElementById("cookie-banner");
const settings = document.getElementById("cookie-settings");
const openSettingsBtn = document.getElementById('open-cookie-settings');

function setCookie(name, value, days) {
const d = new Date();
d.setTime(d.getTime() + days * 86400000);
document.cookie = `${name}=${value};expires=${d.toUTCString()};path=/`;
}

function deleteCookie(name) {
document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
}

function saveConsent(consent) {
localStorage.setItem("cookieConsent", JSON.stringify(consent));
}

function getConsent() {
return JSON.parse(localStorage.getItem("cookieConsent") || "{}");
}

function applyConsent(consent) {
if (consent.statistics) setCookie("statistics_enabled", true, 30);
else deleteCookie("statistics_enabled");

if (consent.marketing) setCookie("marketing_enabled", true, 30);
else deleteCookie("marketing_enabled");
}

const consent = getConsent();
if (!consent.decisionMade) banner.classList.remove("hidden");
else banner.classList.add("hidden");
document.getElementById("accept-all").onclick = () => {
const consent = {
    necessary: true,
    preferences: true,
    statistics: true,
    marketing: true,
    decisionMade: true,
};
saveConsent(consent);
applyConsent(consent);
banner.classList.add("hidden");
};

document.getElementById("reject-all").onclick = () => {
const consent = {
    necessary: true,
    preferences: false,
    statistics: false,
    marketing: false,
    decisionMade: true,
};
saveConsent(consent);
applyConsent(consent);
banner.classList.add("hidden");
};

document.getElementById("manage-cookies").onclick = () => {
settings.classList.add("active");
};

document.getElementById("save-preferences").onclick = () => {
const consent = {
    necessary: true,
    preferences: document.getElementById("preferences").checked,
    statistics: document.getElementById("statistics").checked,
    marketing: document.getElementById("marketing").checked,
    decisionMade: true,
};
saveConsent(consent);
applyConsent(consent);
settings.classList.remove("active");
banner.classList.add("hidden");
};
openSettingsBtn.addEventListener('click', () => {
    banner.classList.remove("hidden")
});

document.querySelectorAll('.accordion-header').forEach((header) => {
    header.addEventListener('click', () => {
    const expanded = header.getAttribute('aria-expanded') === 'true';
    document.querySelectorAll('.accordion-header').forEach(h => h.setAttribute('aria-expanded', 'false'));
    header.setAttribute('aria-expanded', !expanded);
    });
});