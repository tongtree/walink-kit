# WhatsApp Chat Button (HTML widget)

A dependency-free floating chat button you can drop into any website.

## Usage

1. Copy `widget.js` next to your page (or host it anywhere).
2. Add this snippet before the closing `</body>` tag:

```html
<script>
  window.waLinkWidget = {
    phone: "15551234567",
    message: "Hello, I have a question",
    label: "Chat with us",
    position: "right"
  };
</script>
<script src="/path/to/widget.js" defer></script>
```

Open `index.html` to see a live demo.

For a hosted, analytics-enabled chat widget see the [WALink online generator](https://walink.wadesk.io).
