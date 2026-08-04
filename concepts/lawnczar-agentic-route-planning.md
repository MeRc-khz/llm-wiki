---
title: LawnCzar Agentic Route Planning
created: 2026-08-02
updated: 2026-08-02
type: concept
tags: [lawnczar, routing, agent, map, itinerary]
sources: [js/saved-sales.js, js/lawn-map.js, js/app-toolbar.js, js/location-prompt.js, js/app.js, server.js]
confidence: high
contested: false
contradictions: []
status: phase-1-complete
---

# LawnCzar Agentic Route Planning

**Agentic route planning** for [[lawnczar]] — replacing the current "open in Google Maps" deeplink with an in-app, LLM-optimized multi-stop itinerary that renders directly on the Leaflet map.

---

## 📊 Current State (as of 2026-08-02)

### Seed Data
- **23 markers** in MongoDB `lawnczar.markers`, centered on **San Diego / 91950** (National City area)
- Neighborhoods: National City, Chula Vista, Paradise Hills, Imperial Beach, San Ysidro, Otay Mesa, Lincoln Acres, City Heights, Hillcrest, Mission Hills, Old Town, Little Italy, Bankers Hill, Pacific Beach, La Jolla
- Types: `truck` (5), `garage` (4), `estate` (3), `yard` (2), `moving` (2), `market` (2), `block` (1), `thrift` (1), `craft` (1), `antique` (1), `community` (1)

### Infrastructure
- **MongoDB 7** running in Docker container `lawnczar-mongo` on port `27017` with persistent volume `lawnczar-mongo-data`
- **Express backend** on port `3000` serving `/api/markers` + static files
- **Nginx reverse proxy** in front (reloaded 2026-08-02)

### Components Modified (this session)
| File | Change |
|------|--------|
| `data/markers.json` | Rewrote: 3 London markers → 23 San Diego markers |
| `seed.js` | Unchanged — loads `data/markers.json` into Mongo |
| `.env` | Created: `MONGODB_URI=mongodb://127.0.0.1:27017/lawnczar` |
| `js/lawn-map.js` | Added `centerOn(lat, lng)` method; default center changed from London `[51.505, -0.09]` to SD `[32.6783, -117.0992]`; reads saved zip from localStorage |
| `js/app-toolbar.js` | Shop button now dispatches `shop-zip-prompt` event |
| `js/location-prompt.js` | Added `show()` / `hide()` methods for on-demand modal |
| `js/app.js` | Added `shop-zip-prompt` listener → shows location modal |
| `server.js` | Fixed race condition: 503 guard when db not yet connected |

### Current Routing (Basic)
- `saved-sales.js` → `openRoute()` builds a Google Maps directions URL with waypoints and opens in a new tab
- No in-app route rendering, no optimization, no turn-by-turn

---

## 🎯 What Agentic Route Planning Requires

### Phase 1: In-Map Route Rendering ✅ COMPLETE
**Goal:** Draw the optimized route polyline on the Leaflet map via a backend proxy with hybrid provider fallback (Option 4).

**Architecture — Route Proxy (`js/route-proxy.js`):**
```
Client (saved-sales.js)
  → POST /api/route { stops: [{lat, lng}, ...] }
  → Backend proxy tries in order:
      1. Self-hosted regional OSRM (if coords fall in a configured region bbox)
      2. Mapbox Directions API (planet-wide fallback for new zip codes)
      3. OSRM public demo (dev-only safety net)
  → Returns: { geometry, duration, distance, provider, region }
  → Client dispatches route-ready event → lawn-map renders polyline + numbered stops
```

**Implementation:**
- `js/route-proxy.js` (new) — provider fallback chain with regional bbox detection
- `server.js` — added `POST /api/route`, `POST /api/route/matrix`, `GET /api/route/health`
- `js/saved-sales.js` — calls `/api/route` instead of OSRM directly; shows provider tag in button
- `.env` — routing config: `OSRM_SD_URL`, `OSRM_LA_URL`, `OSRM_BAY_URL`, `MAPBOX_TOKEN`
- `js/lawn-map.js` — `renderRoute(geometry, stops)` draws teal polyline + numbered stop markers
- `js/app.js` — wires `route-ready` event → `map.renderRoute()`

**Regional Rollout Plan:**
| Phase | Regions | Provider Priority |
|-------|---------|-------------------|
| Dev (current) | San Diego only | OSRM demo fallback |
| Regional launch | SD + LA + Bay Area | Self-hosted OSRM per region, Mapbox for out-of-region |
| National | All major US metros | Regional OSRM fleet + Mapbox for rural/long-tail |
| Global | US + international | Regional OSRM fleet + Mapbox planet-wide fallback |

**Configured Regions (in `route-proxy.js` REGIONS array):**
- `san-diego`: bbox `[-117.6, 32.4, -116.0, 33.5]`
- `los-angeles`: bbox `[-119.0, 33.5, -117.6, 34.9]`
- `bay-area`: bbox `[-122.8, 37.0, -121.5, 38.5]`

**Matrix Endpoint (Phase 2 prep):**
- `POST /api/route/matrix` — returns NxN duration matrix via same fallback chain
- Will feed the LLM agent for stop-order optimization

**Tested:**
- 3-stop SD route: 189 geometry points, 8 min, 3.0 mi via OSRM demo ✅
- 3x3 distance matrix: correct pairwise durations ✅
- Out-of-region NYC route: correctly falls through to demo ✅
- Error handling: single-stop returns 400 ✅
- Health endpoint: shows provider/region status ✅

### Phase 2: Agentic Optimization
**Goal:** LLM agent optimizes stop order based on user constraints, not just nearest-neighbor.

1. **Distance matrix** — compute pairwise distances between all saved sales:
   - OSRM table API: `GET /table/v1/driving/{coords}` → returns NxN duration/distance matrix
   - Or Valhalla matrix API
2. **Agent prompt** — feed the matrix + sale metadata to an LLM:
   ```
   You are a route optimizer. Given these yard sales with distances:
   - Stop A: "Estate Sale, La Jolla" (type: estate, est. 45min visit)
   - Stop B: "Taco Truck, National City" (type: truck, est. 15min)
   ...
   Distance matrix (minutes): [[0, 12, 25], [12, 0, 18], [25, 18, 0]]
   Constraints: user starts at 91950, wants estate sales first (high value),
   food trucks between stops, done by 3pm.
   Return the optimal stop order as a JSON array of indices.
   ```
3. **Agent backend endpoint** — add to `server.js`:
   - `POST /api/route/optimize` — accepts `{origin, stops[], constraints}`
   - Calls OSRM table API for distance matrix
   - Calls LLM (via OpenRouter / local model) with optimization prompt
   - Returns `{orderedStops, routeGeometry, estimatedTime}`
4. **Constraint types the agent can handle:**
   - Time windows (sale hours: 8am-2pm)
   - Visit duration estimates by sale type
   - Priority weighting (estate > garage > yard)
   - User preferences ("avoid highways", "walkable cluster first")
   - Lunch break insertion ("taco truck at noon")

### Phase 3: Route Interaction
**Goal:** Make the route interactive and re-routable.

1. **Drag-to-reorder** — in the itinerary sidebar, let users drag stops to reorder; agent re-optimizes on drop
2. **Skip/delete stop** — remove a stop, agent recalculates
3. **Add detour** — user taps a non-itinerary marker → "add to route" → agent inserts optimally
4. **Live ETA** — each stop shows estimated arrival time based on cumulative travel + visit duration
5. **Turn-by-turn** (optional) — integrate OSRM turn-by-turn geometry with Leaflet

### Phase 4: Proactive Agent Suggestions
**Goal:** Agent proactively suggests route improvements.

1. **Cluster detection** — "You have 3 sales within 2 blocks of each other — start here"
2. **Time-sensitivity** — "This estate sale ends at 1pm, prioritize it"
3. **Weather-aware** — check forecast, suggest indoor sales (estate/antique) during rain windows
4. **Discovery** — "Based on your swiped-right sales, you like estate sales. 2 unvisited ones are near your route."

---

## 🏗️ Architecture (Proposed)

```
User saves sales → Itinerary sidebar
                   ↓
            POST /api/route/optimize
                   ↓
        ┌──────────────────────┐
        │  Express backend    │
        │  1. OSRM table API  │ → distance matrix
        │  2. LLM agent call  │ → optimized stop order
        │  3. OSRM route API  │ → polyline geometry
        └──────────────────────┘
                   ↓
            {orderedStops, geometry, etas}
                   ↓
        lawn-map.js renders polyline
        saved-sales.js shows ordered list with ETAs
```

### New/Modified Files
| File | Role |
|------|------|
| `server.js` | Add `POST /api/route/optimize` endpoint |
| `js/saved-sales.js` | Replace `openRoute()` with `optimizeRoute()` calling the backend |
| `js/lawn-map.js` | Add `renderRoute(geometry)` and `clearRoute()` methods |
| `js/app.js` | Wire `route-ready` event from saved-sales to lawn-map |
| `js/route-agent.js` (new) | Client-side route state management + re-optimization triggers |

### Infrastructure Additions
- **OSRM Docker container** — `osrm/osrm-backend` with San Diego OSM extract
  ```
  docker run -d --name osrm -p 5000:5000 \
    -v osrm-data:/data osrm/osrm-backend osrm-routed \
    --algorithm mld /data/san-diego.osrm
  ```
- **LLM endpoint** — reuse existing OpenRouter provider or local model for optimization calls

---

## 🔗 Cross-References
- [[lawnczar]] — main entity, architecture, component inventory
- [[rag]] — distance matrix as structured retrieval for the agent
- [[aieos-integration]] — agent identity for route optimization calls
