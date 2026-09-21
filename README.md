# WALink Kit

[![License: MIT](https://img.shields.io/badge/license-MIT-25d366.svg)](./LICENSE)

Open-source building blocks for WhatsApp **click-to-chat links**: a zero-dependency
core library, a web generator, a drop-in chat button, and a minimal short-link
backend demo.

**[Free online generator · English](https://walink.wadesk.io)** ·
**[Generador en línea · Español](https://link.wadesk.io)** ·
**[Docs & guide](./examples/fastapi-demo/README.md)**

---

## What is included

| Package / example | Description |
| ----------------- | ----------- |
| [`@walink/core`](./packages/core) | Zero-dependency TypeScript library: phone normalization, validation and `wa.me` / `api.whatsapp.com` link building |
| [`examples/web`](./examples/web) | Vite + Vue single-page generator with copy link and QR code download |
| [`examples/html-widget`](./examples/html-widget) | Dependency-free floating WhatsApp chat button for any website |
| [`examples/fastapi-demo`](./examples/fastapi-demo) | FastAPI + SQLite short links, redirects and per-day click stats with Docker |

## Quick start

### Core library

```ts
import { createWhatsAppLink } from "@walink/core";

createWhatsAppLink({
  phone: "13800138000",
  countryCode: "+86",
  message: "Hello",
});
// => "https://wa.me/8613800138000?text=Hello"
```

### Web generator

```bash
pnpm install
pnpm --filter @walink/example-web dev
```

### Backend demo

```bash
cd examples/fastapi-demo
docker compose up
# API docs at http://localhost:8000/docs
```

## Self-hosted vs WALink Cloud

| Capability | This open-source kit | WALink Cloud |
| ---------- | -------------------- | ------------ |
| Build WhatsApp links | ✅ | ✅ |
| QR codes | ✅ (example) | ✅ |
| Chat button | ✅ | ✅ |
| Short links + basic click counts | ✅ (demo) | ✅ |
| Link rotator / smart rules | ❌ | ✅ |
| Visitor analytics & dashboards | ❌ | ✅ |
| Authentication & team management | ❌ | ✅ |
| Abuse protection & rate limiting | ❌ | ✅ |
| Hosting, uptime & maintenance | Self-managed | ✅ Managed |

Need advanced routing, analytics and zero-maintenance hosting? Try the
**[WALink online generator · English](https://walink.wadesk.io)** or the
**[Versión en español](https://link.wadesk.io)**.

## Development

```bash
pnpm install
pnpm lint
pnpm test          # core library unit tests
pnpm build         # build the core library
```

The backend demo has its own test suite:

```bash
cd examples/fastapi-demo
pytest
```

## License

Released under the [MIT License](./LICENSE). The **WALink** name, logos and
official domains are trademarks and are not covered by the MIT license; see
[TRADEMARK.md](./TRADEMARK.md).
