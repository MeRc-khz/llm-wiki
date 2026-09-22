# Savage Dad / SvgDad (svgdad)

Entity: Savage Dad apparel storefront brand of The Conglomerate Group.

## Domains & Deploy
- `svgdad.store`, `svgdad.shop` (GoDaddy) → nginx `svgdad.conf` → `/var/www/svgdad/html`
- App repo: `/srv/projects/REPOS/svgdad` (Angular CLI PWA + Material 3, NgRx, lazy features, service worker)
- Shopify store: `if3711-4m.myshopify.com` (Shop name: svgXdad), org 236229955
- See [[domain-portfolio]] for registry entry.

## Design System — Savage Dad dark theme (source: repo `src/assets/styles.scss` + `The Savage Dad Style Guide.md`)
- Background street black `#1F1B16`, surfaces `#2B2723`/`#25211D`, borders `#3E372E`
- Primary Sunburn Orange: `#FFB683` (dark) / `#A63E00` (light)
- Secondary Earthy Tan `#DBC0A3`; text `#EBE1D9`, muted `#A89F95`
- Success `#A8D773`, error `#FFB4AB`; CTA `#FFB683` on `#1F1B16`
- Fonts: Bangers (display H1 48 / H2 32), Roboto (body 16, CTA 14 bold)
- Imagery: high-contrast desaturated street photography, charcoal/black product backgrounds
- NOT indigo/pink Material defaults — do not use #3f51b5 / #f44336 / #ff4081.

## Shopify integration
- Dev Dashboard app client_id `491cb6e7...` → client-credentials grant (24h tokens, `write_products`)
- Theme/file scopes (`read_themes`, `write_themes`, `read_files`) not yet granted — store theme work blocked on that
- Products standardized: Vendor `SvgDad`, T-Shirt, $40, sizes S–2XL, tags `svgdad, streetwear, <drop>`
