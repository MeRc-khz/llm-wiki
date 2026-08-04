---
title: LawnCzar Auto Region Provisioning
created: 2026-08-02
updated: 2026-08-02
type: concept
tags: [lawnczar, osrm, osm, provisioning, infrastructure, automation]
sources: [js/region-provisioner.js, js/route-proxy.js, js/referral-system.js, server.js]
confidence: high
contested: false
contradictions: []
status: working
---

# LawnCzar Auto Region Provisioning

When a new affiliate signs up with a zip code, the system **automatically provisions a self-hosted OSRM routing server** for their geographic area. No manual setup, no Overpass API dependency at runtime.

---

## 🔄 Pipeline

```
Affiliate Signup (zip code)
  ↓
Geocode zip → lat/lng (zippopotam.us)
  ↓
Calculate bbox (zip center ± 0.05° ≈ 3.5mi radius)
  ↓
Step 1: osmium extract --strategy=simple
  Slice bbox from pre-downloaded California OSM PBF (1.3GB)
  → Produces ~5-11MB .osm file per zip region
  (~60 seconds)
  ↓
Step 2: docker run osrm-extract
  Process .osm → routing graph (.osrm)
  (~15 seconds, ~100K edges)
  ↓
Step 3: docker run osrm-contract
  Build contraction hierarchies
  (~50 seconds, 277K contracted edges)
  ↓
Step 4: docker run -d osrm-routed
  Start persistent OSRM server container
  (port 5100+, auto-assigned)
  ↓
Dynamic registration in route-proxy.js
  → New region immediately available for routing
  → No server restart needed
```

**Total time: ~75-120 seconds per region**

---

## 🏗️ Architecture

### State Extracts (one-time download)
```
/srv/projects/lawnmap/osrm/california.osm.pbf  (1.3GB, Geofabrik)
```
Downloaded once via `curl` from Geofabrik's CDN. Each new zip code slices a bbox from this file — no per-region download needed. Add more state extracts as rollout expands:
- `texas.osm.pbf` → 7xxxx zip codes
- `new-york.osm.pbf` → 10xxx zip codes

### Per-Region Files
```
/srv/projects/lawnmap/osrm/regions/{zip}/
  data.osm          ← osmium slice output
  data.osrm         ← osrm-extract output
  data.osrm.*       ← contraction hierarchy files
```

### Docker Containers
```
osrm-{zip}  →  port {5100+N}:5000  →  osrm-routed --algorithm CH
```
Each region gets its own persistent Docker container. Auto-assigned port starts at 5100.

---

## 🧩 Code Flow

### `js/region-provisioner.js`
- `provisionRegion(zip, lat, lng)` — entry point, non-blocking async
- `runCommand(cmd, args, opts)` — async spawn wrapper (replaced `execSync`)
- `acquireOSMData(bbox, path, zip)` — tries state extract slice first, falls back to Overpass API
- `processAndStartRegion(zip, bbox, dir, port)` — 4-step pipeline
- `setRegisterCallback(fn)` — bridge to route-proxy for dynamic registration

### `js/referral-system.js`
- On `signUp()`: geocodes zip via zippopotam.us, calls `provisionRegion(zip, lat, lng)`
- Non-blocking — signup response returns immediately, provisioning runs in background

### `js/route-proxy.js`
- `addDynamicRegion(region)` — called when provisioning completes
- `findRegionForCoords()` — checks static + dynamic regions
- New routes automatically use the self-hosted OSRM instead of demo/Mapbox

### `server.js` endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/region/provision` | POST | Manually trigger provisioning |
| `/api/region/status/:zip` | GET | Check provisioning status |
| `/api/region/list` | GET | List all regions |

---

## ✅ Tested (2026-08-02)

### Manual provisioning (zip 92101)
- osmium slice: 11MB from California PBF in ~60s ✅
- osrm-extract: 100,947 edges, 60,648 coordinates in ~15s ✅
- osrm-contract: 277,760 contracted edges in ~50s ✅
- osrm-routed container: live on port 5100 ✅
- Route test: 3 stops, 432 geometry points, 15 min, 4.3 mi ✅
- Provider: `osrm`, Region: `zip-92101` ✅

### Auto-provisioning via signup (zip 92104)
- Affiliate signed up → provisioning auto-triggered ✅
- Region ready in ~120s ✅
- Docker container `osrm-92104` live on port 5101 ✅
- Route health shows 2 dynamic regions ✅

### async spawn fix
- Replaced all `execSync` with async `spawn` wrapper
- No more `ETIMEDOUT` errors
- Non-blocking — Node event loop free during osmium/OSRM processing
- Progress tracking via region status field

---

## 🚀 Scaling Plan

| Phase | States | Storage | Regions | Notes |
|-------|--------|---------|---------|-------|
| Current | California | 1.3GB | ~2 (92101, 92104) | Working |
| Regional | +TX, +NY, +FL | ~5GB | <100 | Add state PBFs as needed |
| National | All 50 states | ~60GB | Thousands | Download all state extracts |
| Global | Planet | ~70GB | Worldwide | Single planet.osm.pbf |

### State Extract Download
```bash
# Download a new state extract (one-time per state)
curl -sL "https://download.geofabrik.de/north-america/us/{state}-latest.osm.pbf" \
  -o /srv/projects/lawnmap/osrm/{state}.osm.pbf
```
Add to `STATE_EXTRACTS` in `region-provisioner.js` and update `getExtractForZip()` zip prefix map.

---

## 🔗 Cross-References
- [[lawnczar]] — main platform
- [[lawnczar-agentic-route-planning]] — route proxy with hybrid fallback chain
- [[lawnczar-qr-referral-network]] — affiliate signup triggers provisioning