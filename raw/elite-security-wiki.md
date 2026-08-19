# Elite Security Team Management System — Wiki

> **Vision**: SaaS platform for security staffing agencies to schedule, certify, dispatch, and communicate with guards across multi-venue events — from parking lots to 70,000-seat ballparks.

---

## 1. Problem Statement

**Current Process (Manual, Painful):**
- Guard calls dispatch → "I want Wed, Thu, Sat, Sun afternoons"
- Dispatcher manually checks: venue needs × guard certifications × availability
- Dispatcher reads back options → guard accepts/declines per shift
- No real-time visibility, no notifications, no audit trail
- Schedule changes = phone tag chaos

**Scale:**
- 500+ guards
- Multiple concurrent venues (parking lots, schools, construction, 3K-seat amphitheaters, 20K-seat arenas, 70K-seat ballparks)
- Contracts: long-term (season) + short-term (single event)
- Event duration: hours → multi-day

---

## 2. Domain Model

### 2.1 Personnel

| Role (Shirt Color) | Responsibilities | Typical Certifications Required |
|---|---|---|
| **Event Patrol (Red)** | General patrol, crowd management | Guard Card |
| **Supervisor (Blue)** | Oversee red shirts, incident escalation | Guard Card + Supervisor Cert |
| **Alcohol Abuse Prevention (Green)** | Monitor alcohol areas, intervention | Guard Card + TIPS/Alcohol Cert |
| **Site Manager (Black)** | Venue command, client liaison, staffing decisions | Guard Card + Management Cert + exp. |
| **Traffic Guard** | Vehicle/pedestrian flow, parking | Guard Card + Traffic Cert |
| **Specialized** | Handcuff, Firearm, Vehicle Patrol, K9, etc. | Guard Card + specific endorsement |

**Guard Profile:**
- State Guard Card (mandatory, expiration tracked)
- Multiple certifications (traffic, handcuff, firearm, vehicle patrol, CPR, etc.)
- Availability preferences (days, times, venue types, travel radius)
- Employment status (full-time, part-time, on-call)
- Performance history (reliability, incidents, client feedback)

### 2.2 Venues & Events

**Venue:**
- Schematic/layout (uploaded PDF/image/GeoJSON)
- Defined patrol zones with metadata (indoor/outdoor, risk level, capacity)
- Permanent attributes (address, capacity, parking, access points)

**Event:**
- Venue + date/time range (single day or multi-day)
- Required staffing matrix per zone per time block
- Client requirements (special certs, min supervisors, alcohol zones)
- Contract type: long-term (recurring) vs. short-term (one-off)

**Shift:**
- Event + zone + time window + role + required certifications
- Assigned guard (or open/unfilled)
- Status: open → offered → accepted → confirmed → completed → disputed

### 2.3 Certifications & Compliance

- **Guard Card**: State-issued, expiration date, renewal tracking
- **Endorsements**: Traffic, Firearm, Handcuff, Vehicle Patrol, Baton, OC Spray, CPR/First Aid, TASER, K9, Supervisor, Alcohol/TIPS, Crowd Management
- **Venue-specific**: Some venues require additional badges (e.g., stadium credential)
- **Expiration alerts**: 90/60/30/7 day warnings to guard + admin

---

## 3. Core Workflows

### 3.1 Shift Publishing & Self-Selection (Replaces Phone Calls)
1. **Admin creates event** → defines shifts per zone/role/cert
2. **System auto-matches** eligible guards (certs + availability + no conflicts)
3. **Notifications sent** (push/SMS/email/app) to matched guards: "Shift available: [Venue] [Date] [Time] [Role] - Tap to claim"
4. **Guard claims** → instant confirmation, calendar sync
4. **Waitlist** if oversubscribed; auto-promote on dropout

### 3.2 Dispatcher-Assisted Assignment (For Complex Events)
1. Dispatcher views **real-time eligibility matrix**: guards × shifts
2. Filters: certs, availability, seniority, travel distance, overtime risk
3. **Drag-drop assign** or bulk-offer to filtered group
4. Guard accepts/declines in app → dispatcher sees live status

### 3.3 Schedule Changes & Communication
- **Change types**: time shift, zone swap, role upgrade/downgrade, cancellation, new shift added
- **Instant notification** to affected guards + supervisors + site manager
- **Acknowledgment required** (guard taps "Seen" or auto-escalates after 15 min)
- **Audit log**: who changed what, when, why (reason code required)

### 3.4 Check-in/Check-out & Accountability
- GPS/geofence check-in at venue (or QR code at check-in point)
- Live roster view for site manager: who's on site, who's late, who's missing
- Incident reporting tied to shift/guard/zone
- Post-shift: hours verified → payroll export

---

## 4. Software Strategy & Architecture

### 4.1 Recommended Tech Stack

| Layer | Recommendation | Rationale |
|---|---|---|
| **Frontend (Web)** | React + TypeScript + Vite | Team familiarity, rich ecosystem, PWA support |
| **Mobile** | React Native (Expo) or Capacitor wrapper | Single codebase, push notifications, offline-first |
| **Backend** | Node.js (NestJS/Fastify) or Go | TypeScript end-to-end, good for real-time |
| **Real-time** | WebSockets (Socket.io) or Server-Sent Events | Live roster, shift claims, notifications |
| **Database** | PostgreSQL + PostGIS | Relational integrity + geospatial for venues/zones |
| **Auth** | OAuth2/OIDC (Keycloak/Auth0/Clerk) | SSO, MFA, role-based access, org multi-tenancy |
| **File Storage** | S3-compatible (MinIO/Tigris/AWS) | Schematics, certs, incident photos |
| **Search** | PostgreSQL FTS or Meilisearch | Guard search, shift search, audit log search |
| **Scheduling Engine** | Custom (rule-based) or OptaPy/OR-Tools | Constraint solving for auto-assignment |
| **Notifications** | Firebase/OneSignal (push) + Twilio (SMS) + SendGrid (email) | Multi-channel, templates, delivery receipts |
| **Payroll Export** | CSV/ADP/Paycom/API integration | Flexible for different payroll providers |

### 4.2 Multi-Tenancy (SaaS for Other Agencies)
- **Organization** = top-level tenant (Elite, Agency B, Agency C)
- **Data isolation**: Row-level security (RLS) in Postgres or separate schemas
- **Customization per tenant**: branding, cert types, shift rules, notification templates
- **Super-admin** (Elite) manages platform; **org-admins** manage their agency

### 4.3 Key Modules (Build Order)

| Phase | Module | Description |
|---|---|---|
| **1** | **Auth & Org Setup** | Multi-tenant auth, roles, guard card tracking |
| **1** | **Venue & Schematic Manager** | Upload layouts, define zones, geo-fences |
| **1** | **Guard Directory & Certifications** | Profiles, certs, expirations, availability preferences |
| **2** | **Event & Shift Builder** | Create events, define staffing matrix, recurring templates |
| **2** | **Smart Matching & Publishing** | Auto-match guards → shifts, publish with notifications |
| **2** | **Guard Mobile App** | Claim shifts, view schedule, check-in, notifications |
| **3** | **Dispatcher Dashboard** | Real-time matrix, drag-drop, bulk actions, waitlists |
| **3** | **Site Manager Live View** | On-site roster, GPS check-ins, incident logging |
| **3** | **Schedule Changes & Comms** | Change engine, acknowledgment tracking, audit log |
| **4** | **Payroll & Hours Export** | Verified hours → payroll formats, overtime calc |
| **4** | **Reporting & Analytics** | Fill rates, no-shows, cert gaps, labor cost per event |
| **5** | **Client Portal (Optional)** | Venue clients view staffing, approve invoices |

### 4.4 Scheduling Intelligence (The Differentiator)

**Rule Engine Inputs:**
- Guard: certs, availability, max hours/week, travel radius, preferences
- Shift: required certs, role, zone, time, venue, client requirements
- Constraints: no double-booking, min rest between shifts (e.g., 8h), overtime limits, supervisor:guard ratios

**Outputs:**
- **Auto-fill %**: Target >90% of shifts pre-filled before dispatcher touches
- **Fairness**: Rotate desirable shifts, track seniority
- **Cost optimization**: Minimize overtime, travel pay, last-minute premiums

**Algorithm Approach:**
- Start with **constraint satisfaction** (OR-Tools CP-SAT) for feasible assignments
- Add **scoring** (preference match, seniority, cost) for ranking
- **Human-in-the-loop**: Dispatcher reviews/overrides before publish

### 4.5 Notification Strategy

| Channel | Use Case | Delivery Guarantee |
|---|---|---|
| **Push (App)** | Shift offers, changes, check-in reminders | High (retry + fallback) |
| **SMS** | Critical: shift cancelled, emergency, no-show escalation | Highest (carrier receipt) |
| **Email** | Weekly schedule digest, cert expirations, payroll summaries | Standard |
| **In-App Banner** | Non-urgent: new cert available, policy updates | N/A |

**Templates**: Per-org, per-event-type, multi-language (Spanish common in security)

---

## 5. Data Model Sketch (PostgreSQL)

```sql
-- Core tables
organizations (id, name, slug, settings_json, branding_json)
users (id, org_id, email, phone, password_hash, role, mfa_enabled)
guards (id, org_id, user_id, employee_id, guard_card_num, guard_card_exp, status, hire_date)
certifications (id, org_id, name, code, requires_renewal, validity_months)
guard_certifications (guard_id, cert_id, issued_date, expires_date, status, document_url)
venues (id, org_id, name, address, capacity, geojson_boundary, schematic_url)
venue_zones (id, venue_id, name, zone_type, risk_level, geojson_polygon, capacity)
events (id, org_id, venue_id, name, client_name, contract_type, start_dt, end_dt, status)
event_shifts (id, event_id, zone_id, role, required_cert_ids[], start_dt, end_dt, min_staff, max_staff)
shift_assignments (id, shift_id, guard_id, status, assigned_at, assigned_by, acknowledged_at)
availability (id, guard_id, day_of_week, start_time, end_time, venue_type_pref[], travel_radius_mi)
notifications (id, org_id, guard_id, shift_id, type, channel, payload_json, sent_at, delivered_at, acknowledged_at)
audit_logs (id, org_id, actor_id, action, entity_type, entity_id, old_json, new_json, reason_code, created_at)
```

---

## 6. MVP Scope (8–12 Weeks)

| Week | Deliverable |
|---|---|
| 1–2 | Multi-tenant auth, org setup, guard directory, cert tracking |
| 3–4 | Venue/zone manager with schematic upload + zone drawing (Mapbox/Leaflet) |
| 5–6 | Event builder + shift matrix (recurring templates for long-term contracts) |
| 7–8 | Smart matching (rule-based v1) + shift publishing + push/SMS notifications |
| 9–10 | Guard mobile app (React Native/Expo): claim shifts, schedule view, check-in |
| 11–12 | Dispatcher dashboard: live matrix, drag-drop, waitlist, change management |
| **Launch** | Beta with Elite's 500 guards → iterate → onboard Agency #2 |

---

## 7. Operational Strategies for Elite (Day-One Improvements)

### 7.1 Quick Wins (No Code / Low Code)
- **Google Forms + Sheets → AppScript**: Guard availability intake → auto-email dispatcher summary
- **Calendly/WhenIWork**: Guards self-book open shifts (link per event)
- **WhatsApp/Slack Broadcast Lists**: Shift alerts by role/cert (manual but faster than calls)
- **Google My Maps**: Plot venues, zones, guard homes → visualize travel radius

### 7.2 Process Changes (Immediate)
1. **Standardize shift definitions**: Every shift = Venue + Zone + Role + Time + Required Certs
2. **Weekly availability form**: Guards submit Mon–Sun preference by Friday 5 PM
3. **Dispatcher "offer board"**: Shared spreadsheet with filters (cert, date, role) → guards reply "claim"
4. **Cert expiration dashboard**: Shared sheet with conditional formatting (red <30 days)

### 7.3 Data Prep for Migration
- Export all guard cards + certs + expirations → CSV
- Digitize venue schematics → PDF + zone annotations
- Document current pay rules (overtime, travel, premiums) for payroll engine

---

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Guard adoption (non-tech-savvy) | Simple mobile app, SMS fallback, in-person training, "claim by replying YES" |
| Complex union/contract rules | Configurable rule engine per org, not hardcoded |
| Last-minute changes (weather, client) | Real-time notifications + acknowledgment required + escalation timer |
| Multi-venue same day | Travel time buffer in scheduler, conflict detection |
| Data privacy (guard PII) | SOC2 path, encryption at rest, RLS, minimal data retention |
| Scale (500+ concurrent at ballpark) | Load test WebSocket layer, horizontal scaling, CDN for static assets |

---

## 9. Competitive Landscape & Differentiation

| Competitor | Focus | Gap We Fill |
|---|---|---|
| **When I Work / Deputy** | General hourly scheduling | Security-specific: certs, zones, schematics, gun/firearm tracking |
| **TrackTik / Silvertrac** | Guard tour / patrol logging | **Scheduling-first**, multi-venue events, agency multi-tenancy |
| **CrewSense / Aladtec** | Public safety (fire/EMS) | Private security workflows, alcohol certs, traffic, client portals |
| **Custom Excel/Sheets** | Most agencies today | **Automation**, real-time, mobile, audit, SaaS resale |

**Our Moat**: Security-agency-native domain model + scheduling intelligence + multi-tenant SaaS for resale.

---

## 10. Next Steps

1. **Validate** this wiki with 3 dispatchers + 5 guards (pain points, wish list)
2. **Prioritize** MVP modules (dispatcher dashboard vs. guard app — which saves more hours?)
3. **Prototype** shift publishing + claim flow in 1 week (no-code: Airtable + Make + Twilio)
4. **Estimate** build cost: ~$150–250K for MVP (2 devs + 1 designer, 3 months)
5. **Decide**: Build in-house vs. partner with dev shop vs. buy + customize

---

*Last updated: 2026-08-15 — Created from ingest session*