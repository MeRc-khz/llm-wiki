---
title: Domain Portfolio
created: 2026-05-29
updated: 2026-05-29
type: entity
tags: [agentic, orchestration, workflow]
sources: [raw/articles/aieos-specification.md]
confidence: high
contested: false
contradictions: []
---

# Domain Portfolio

The **Domain Portfolio** is the complete registry of network coordinates and web domains owned, managed, and routed by **[[the-conglomerate-group|The Conglomerate Group]]**. These domains point to our high-utility Progressive Web Applications (PWAs), interactive games, and Web3 asset portals.

Most of our consumer domains are managed via **GoDaddy**, while our specialized web-gated portal domain is managed via **AWS Route 53**.

---

## 🌐 The Conglomerate Domain Registry

| Brand / Project | Domain Name | Registrar | Target Root / Directory | Nginx Config |
| :--- | :--- | :--- | :--- | :--- |
| **[[makeufamous|MakeUFamo.us]]** | `makeufamo.us` | GoDaddy | `/var/www/makeufamous/html` | `makeufamous.conf` |
| **[[ballademix|Ballademix NFT]]** | `bzzrrr.link` | AWS | `/var/www/bzzrrr.link/html` | `bzzrrr.link.conf` |
| **[[ballademix|Ballademikz Catalog]]** | `ballademicz.com` <br> `ballademicz.net` <br> `ballademicz.store` <br> `ballademicz.shop` <br> `ballademicz.us` | GoDaddy | `/var/www/ballademicz/html` | `ballademicz.conf` |
| **[[czarui|czarui Sales Engine]]** | `czarui.game4real.us` | GoDaddy | `/var/www/czarui/html` (Frontend) <br> Port `3001` (Backend) | `czarui.conf` |
| **[[roachcoach|RoachCoach PWA]]** | `roachcoach.store` <br> `roachcoach.shop` | GoDaddy | `/var/www/roachcoach/html` | `roachcoach.conf` |
| **[[lawnczar|LawnCzar PWA]]** | `lawnczar.com` <br> `lawnczar.shop` <br> `lawnczar.store` | GoDaddy | `/var/www/lawnczar-react` (React) <br> Port `3000` (Native) | `lawnczar.conf` |
| **[[the-science-of-getting-rich|Savage Dad / svgdad]]** | `svgdad.store` <br> `svgdad.shop` | GoDaddy | `/var/www/svgdad/html` | `svgdad.conf` |
| **LateNiteSnaps** | `latenitesnaps.com` <br> `latenitesnaps.store` <br> `latenitesnaps.shop` <br> `latenitesnaps.us` | GoDaddy | `/var/www/latenitesnaps/html` | `latenitesnaps.conf` |
| **Game4Real** | `game4real.us` <br> `game4real.store` <br> `game4real.shop` | GoDaddy | `/var/www/game4real/html` | `game4real.conf` |

---

## ⚙️ Nginx Server Routing Architecture

All domain groups are routed through the central Nginx reverse proxy on the master deployment host:

### 1. The G-Funk Portal (`bzzrrr.link`)
- **Config:** `/etc/nginx/sites-available/bzzrrr.link.conf`
- **Routing:** Directs HTTP traffic to the Web3 gated holder portal root at `/var/www/bzzrrr.link/html`.

### 2. RoachCoach Locator (`roachcoach.store` / `roachcoach.shop`)
- **Config:** `/etc/nginx/sites-available/roachcoach.conf`
- **Routing:** Directs food-finder and swiping traffic to the PWA assets at `/var/www/roachcoach/html`.

### 3. Ballademikz Audio Repository (`ballademicz.*`)
- **Config:** `/etc/nginx/sites-available/ballademicz.conf`
- **Routing:** Handles standard web inquiries and points them to the media-holding directories at `/var/www/ballademicz/html`.

### 4. LawnCzar geocentric app (`lawnczar.*`)
- **Config:** `/etc/nginx/sites-available/lawnczar.conf`
- **Routing:** Fuses both our **React PWA** served from `/var/www/lawnczar-react` and our **Native Node/Express backend** reverse-proxied from port `3000`. It redirect standard HTTP to HTTPS (TLS certificates managed via Let's Encrypt).

### 5. Savage Dad apparel storefront (`svgdad.*`)
- **Config:** `/etc/nginx/sites-available/svgdad.conf`
- **Routing:** Routes to `/var/www/svgdad/html` where the main retail storefront asset index lives.

### 6. czarui Sales Engine (`czarui.game4real.us`)
- **Config:** `/etc/nginx/sites-available/czarui.conf`
- **Routing:** Serves the Stripe-integrated landing page and demo components from `/var/www/czarui/html`. Reverse-proxies `/api/`, `/webhook`, and `/download/` paths to the Node.js backend running on port `3001` (managed via `czarui.service` systemd unit).

### 7. LateNiteSnaps photoblog (`latenitesnaps.*`)
- **Config:** `/etc/nginx/sites-available/latenitesnaps.conf`
- **Routing:** Serves dark-mode midnight photo logs and urban snaps from `/var/www/latenitesnaps/html`.

### 8. Game4Real gaming catalog (`game4real.*`)
- **Config:** `/etc/nginx/sites-available/game4real.conf`
- **Routing:** Routes to `/var/www/game4real/html` for indie gameplay showcases and simulator widgets. 
- *Note:* Removed port-conflict rules with `code-server.conf` to isolate `code.game4real.us` to our IDE service while returning full site resolution for the apex domains.
