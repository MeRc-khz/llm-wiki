---
title: "MakeUFamo.us - Raw Landing Page"
source_url: "https://www.makeufamo.us"
ingested: 2026-05-25
sha256: 615c2d28d1f3454b7aa6ae7abea6ab0215deaff89ac38b1b01033d600b41f4e4
media_type: article
---

# MakeUFamo.us (www.makeufamo.us) Landing Page Raw Data

A single-page interactive application representing "the world's most democratic online talent show" coming in Fall 2026.

## Page Content Overview

### Header
- Brand Logo: **MAKEUFAMO.US**
- Slogan: "Your Talent is Real. Get Ready to Get Famous."
- Navigation links:
  - The Countdown (#countdown-section)
  - How It Works (#how-it-works)
  - AI Audition Coach (Sandbox) (#critic)
- Action: "Join VIP Waitlist" button (scrolls to hero/CTA)

### Hero Section & VIP Waitlist CTA
- Headline: "Your Talent is Real. Get Ready to Get Famous."
- Sub-slogan: "The world's most democratic online talent show arrives this Fall. Submit a 60-second video, rally global votes, and compete for a life-changing $100,000 Grand Prize."
- Launch Timeline Badge: "Coming Fall 2026 — Secure Early Audition Access"
- Launch Date: September 22, 2026 (Autumn Equinox S1 Release)
- Waitlist Stats displayed:
  - "Over 140,000+ Pre-Registered"
  - "192 Countries Joining"
- Form options for category:
  - Singer (Microphone icon)
  - Dancer (Dancer icon)
  - Musician (Guitar icon)
  - Variety Act (Wand magic sparkles icon)
- Waitlist Data Capture inputs:
  - Stage Name / Band Name
  - Email Address
- Actions: "Claim My VIP Ticket" (saves registration to Firestore under `waitlist` collection)
- Custom Waitlist Ticket (Step 2 visual mockup):
  - Formats ticket with VIP Artist Name, Talent Class, and unique Waitlist ID (e.g., `MUF-WAIT-XXXXX`).

### Triple Highlight Metrics
1. **$100,000** Grand Prize Pool (Secured directly via smart escrows)
2. **100% Online** Zero Travel Costs (Record & upload from your phone)
3. **Direct Casting** A&R Scout Partners (Immediate review from global agents)

### "How It Works" Timeline
1. **Claim Waitlist VIP Ticket**: Save your place in line today. Founding Waitlist members get early preview features and initial audition priority.
2. **Pitch Your 60s Clip**: When Fall 2026 rolls in, easily drop a raw 60-second video of your talent right on the dashboard.
3. **Earn Live Fan Votes**: Leverage real-time viral voting mechanics. Keep track of your score on our state-of-the-art live leaderboard.
4. **Go Live for Grand Prize**: The highest-scoring creators head to our exclusive, broadcasted Grand Jury live series to choose the global winner.

### AI Audition Critic (Pre-Launch Training Simulator)
Allows users to enter a planned audition concept and choose an AI Executive Producer Judge to get instant feedback powered by **Gemini 2.5 Flash** (using a direct REST API call to Google Generative Language API with fallback mock simulation).
- **Simon Direct (The Tough Critic - Cowell style)**: Brutally honest, industry realness.
- **Queen Sparkle (The Encouraging Superstar - RuPaul/Cher style)**: High energy, inspirational, fabulous.
- **The Viral Scout (The Modern Label Scout - Tech/Viral perspective)**: TikTok viral potential, hook-obsessed.

### Technical & Platform Integrations Found in Code
- **Firebase integration**:
  - `apiKey`: "AIzaSy...F7A4"
  - `authDomain`: "makeufamous-61150.firebaseapp.com"
  - `projectId`: "makeufamous-61150"
  - `storageBucket`: "makeufamous-61150.firebasestorage.app"
  - `messagingSenderId`: "48180578676"
  - `appId`: "1:48180578676:web:a829b6b0bed46a3af8c421"
  - `measurementId`: "G-BFZNR7T8HH"
  - Firestore collection used: `waitlist`
- **Gemini API Integration**:
  - Model: `gemini-2.5-flash-preview-09-2025`
  - Mode: `generateContent` via direct fetch REST endpoint (`https://generativelanguage.googleapis.com/...`)
  - Backoff pattern: Exponential backoff with up to 5 attempts on API errors/network failures.
  - Fallback logic: Under `simulateMockAICritique`, triggers predefined judge-specific templates if API key is missing or calls fail.
- **Tailwind CSS**: Leverages script-based Tailwind v3 configuration with custom branding colors:
  - `#8B5CF6` (brand-purple)
  - `#EC4899` (brand-pink)
  - `#0B0914` (brand-darkBg)
  - `#151226` (brand-cardBg)
  - `#FBBF24` (brand-gold)
- **External assets**:
  - Background Video: `https://assets.mixkit.co/videos/preview/mixkit-crowd-raising-their-hands-at-a-concert-11654-large.mp4`
  - FontAwesome & Google Fonts: Space Grotesk, Syne.
