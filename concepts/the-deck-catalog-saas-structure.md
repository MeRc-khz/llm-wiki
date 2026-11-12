---
title: The Deck — Catalog SaaS Product Structure
created: 2026-11-12
updated: 2026-11-12
type: concept
tags: [music, monetization, solana, community, workflow, infrastructure]
sources: []
confidence: high
contested: false
contradictions: []
---

# The Deck — Catalog SaaS Product Structure

This page defines the **project structure** for [[the-deck-saas-platform]]: how a musician's work is
organized, discovered, favorited, arranged, and sold. It turns the single-song reassembly deck
([[ballademix-reassembly-deck]]) into a multi-tenant social music SaaS.

## The hierarchy

```
User
└── Catalog            the user's public profile for the site
    └── Album          a collection of songs
        └── Song       one deck: tempo + master + melody + drums + stems
            ├── Master track      the full song (buy)
            └── Stems             the individual clips (unlock / buy)
```

A **song is a deck**. It carries the same 92-bar package the current Paperchasers deck ships:
`tempo`, `master`, `melody`, `drums`, `stems`, and the chopped sample pads. The master track is the
timeline reference; the stems are the clips a listener can rearrange.

## The catalog is the profile

A user's **catalog** is their site profile — `/{handle}`. It shows their albums, songs, bio, avatar, and
followers. A catalog is public by default; an album or song can be private or unlisted.

* **Albums** group songs. An album has a title, cover, release date, and description.
* **Songs** are the discoverable unit. Each song has a master track and a set of stems.
* **Catalog visibility** — public, unlisted (link-only), private.

## Discovery: the feed

Songs are discoverable on **other users' feeds**. The feed is a reverse-chronological (and optionally
ranked) stream of newly published songs and albums across catalogs. Each feed card carries:

* cover art, title, artist handle, album, tempo, bars, duration
* a **play** action that streams the master (or a preview)
* a **favorite** action
* a **load into deck** action

The feed is the acquisition surface. Every song in it is a potential arrangement.

## Favorites: the listener's library

A listener **favorites** songs they want to load into the deck. Favorites are the bridge between
discovery and arrangement:

1. Browse the feed.
2. Favorite a song.
3. Open the deck, where favorited songs are listed.
4. Load a song's **unlocked clips** and start an arrangement.

A favorite is not an unlock. Favoriting is free; unlocking or buying is what grants audio.

## The deck is the arrangement workspace

The listener opens the deck and loads a favorited song. The deck:

* lists the song's stems as lanes
* **unlocks the clips the listener owns** (or previews locked ones)
* lets the listener slide, trim, and extend clips on the bar:beat:tick grid
* saves the arrangement as a **deck** owned by the listener

The current deck's admin **Deck Builder** (per-lane `at`/`dur`/`offset`, extend front/back, save to the
autosave payload) is the prototype for this workspace. See [[the-deck-saas-platform]] for the shipped
controls.

## Ownership and monetization

Two purchase paths per song:

| Purchase | What it grants | Gate |
|---|---|---|
| **Buy the master track** | The full song as one audio asset | Master NFT / license |
| **Unlock / buy stems** | One or more individual clips | Per-stem NFT (existing `nft/gate.js`) |

The existing per-stem NFT gate already reads ownership from the chain and seals unowned lanes before
the audio loader fetches them. The catalog layer extends that model:

* **Master track NFT** — one mint per song master.
* **Stem NFTs** — one mint per stem, already modeled in `nft/stems.json`.
* **Bundle** — album-level purchase that grants all stems in the album.
* **Campaign** — the artist's social release schedule; each release ties a stem to a photo, lyrics,
  video, and an NFT drop.

Revenue streams: master sales, stem unlocks, album bundles, campaign NFT drops, and secondary
royalties. The catalog is the storefront; the feed is the funnel; the deck is the retention loop.

## Data model

```
users        id, handle, display_name, avatar, bio, created_at
catalogs     id, user_id, title, description, visibility
albums       id, catalog_id, title, cover, release_date, description
songs        id, album_id, title, tempo, bars, duration, key,
             master_asset_id, melody_asset_id, drums_asset_id,
             price_master, license
stems        id, song_id, label, asset_id, bars, lead, offset,
             price, mint
assets       id, kind (master|stem|melody|drums|photo|video),
             url, duration, bytes, checksum
decks        id, user_id, song_id, title, created_at, updated_at
clips        id, deck_id, stem_id, at, dur, offset, muted, solo, vol, pan
favorites    id, user_id, song_id, created_at
follows      id, follower_id, artist_id
unlocks      id, user_id, song_id, stem_id, kind (master|stem),
             price, tx, mint, created_at
campaigns    id, user_id, song_id, start_date, frequency, releases,
             social, template
releases     id, campaign_id, song_id, stem_id, date,
             photo, lyrics, video, mint
```

`clips.at/dur/offset` are the same fields the deck already persists. The admin's Deck Builder writes
them; the catalog layer just owns the `deck` record instead of a single browser's autosave slot.

## Routes

| Route | Surface |
|---|---|
| `/{handle}` | Catalog / profile |
| `/{handle}/{album}` | Album |
| `/{handle}/{album}/{song}` | Song |
| `/feed` | Discoverable feed |
| `/favorites` | Listener library |
| `/deck/{id}` | Deck arrangement workspace |
| `/admin` | Artist admin (campaign, stems, manifest, deck builder) |

## Build order

1. **Catalog + albums + songs** — data model and read routes. The current static deck becomes one song
   in one album in one catalog.
2. **Feed** — publish action + reverse-chronological stream + play/favorite/load actions.
3. **Favorites + deck workspace** — favorite a song, load its unlocked clips, arrange, save.
4. **Ownership gate** — master NFT + stem NFTs, reusing `nft/gate.js` and the `/solrpc` proxy.
5. **Campaign** — the admin's campaign + manifest becomes the artist's release scheduler.
6. **Multi-tenant auth** — artist accounts, catalog ownership, listener accounts.

## Open decisions

1. **Catalog ownership** — one catalog per user, or multiple catalogs per user (label / side project)?
   Default: one catalog per user, albums under it.
2. **Feed ranking** — reverse-chronological first; ranked later. Default: chronological.
3. **Master pricing** — fixed price per song, or artist-set? Default: artist-set with a platform floor.
4. **Stem ownership model** — NFT per stem (current) vs. license key vs. both. Default: NFT + license
   record.
5. **Arrangement ownership** — can a listener sell or share an arrangement? Default: share link only;
   no resale until the licensing model is settled.
6. **Private catalogs** — does a private catalog hide its songs from the feed? Default: yes, unless the
   song is explicitly published.

## Related

* [[the-deck-saas-platform]] — the shipped product, admin dashboard, and Deck Builder.
* [[ballademix-reassembly-deck]] — the single-file deck engine this SaaS runs on.
* [[ballademix]] — the parent NFT collection and Solana mechanics.
* [[tokenized-equity]] — the ownership/tokenization framework if catalog equity is fractionalized.
