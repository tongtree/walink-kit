(function () {
  "use strict";

  var config = window.waLinkWidget || {};

  if (!config.phone) {
    return;
  }

  var digits = String(config.phone).replace(/\D/g, "");
  var text = config.message ? "?text=" + encodeURIComponent(config.message) : "";
  var url = "https://wa.me/" + digits + text;

  var button = document.createElement("a");
  button.href = url;
  button.target = "_blank";
  button.rel = "noopener";
  button.setAttribute(
    "style",
    [
      "position:fixed",
      "bottom:24px",
      (config.position === "left" ? "left:24px" : "right:24px"),
      "display:inline-flex",
      "align-items:center",
      "gap:8px",
      "background:#25d366",
      "color:#073b24",
      "font-weight:700",
      "font-size:15px",
      "font-family:system-ui,sans-serif",
      "text-decoration:none",
      "padding:12px 18px",
      "border-radius:999px",
      "box-shadow:0 6px 20px rgba(0,0,0,.18)",
      "z-index:999999",
    ].join(";")
  );

  var icon = document.createElement("span");
  icon.textContent = "\uD83D\uDCAC";
  var label = document.createElement("span");
  label.textContent = config.label || "Chat on WhatsApp";

  button.appendChild(icon);
  button.appendChild(label);

  function mount() {
    document.body.appendChild(button);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
