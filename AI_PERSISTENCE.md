# AI Persistence Notes — St. James’ Dispatch

This file is a handoff for future AI sessions. It explains how the project works, where key elements live, and how to update it safely.

## Project Overview
- Static site for Newcastle United match reviews.
- Core pages:
  - `index.html` — latest review only.
  - `archive.html` — list of past reviews (clickable rows).
  - `about.html` — about text + contact email.
  - `reviews/` — individual review pages, one per match.
- Styling: Tailwind via CDN + `styles.css` for custom styles (grid background, rules, typography, etc.).
- No framework / build step.

## Design Principles
- “Black & White Reviews // without the noise.”
- Minimal, editorial, collectible layout.
- No cards, shadows, or clutter.
- Subtle checkered background (very light grid).
- Use restrained spacing and strong typography hierarchy.

## Key UI Elements
- Masthead (all pages):
  - Title: **St. James’ Dispatch** (bold).
  - Tagline line beneath: `Black & White Reviews // without the noise`.
  - Nav is on its own row below masthead.
- Horizontal rules are inset on mobile (`mx-6`) and centered on desktop (`sm:mx-auto`).
- Footer includes:
  - `A No Noise Review • Printed in Newcastle`.
  - Social icons (X, Instagram, RSS) as inline SVGs.

## File Map
- `index.html`
  - Contains `<!-- LATEST_REVIEW_START -->` and `<!-- LATEST_REVIEW_END -->` markers.
  - Latest review content must sit between those markers.
- `archive.html`
  - Contains `<!-- ARCHIVE_LIST_START -->` and `<!-- ARCHIVE_LIST_END -->` markers.
  - Archive list lives between those markers; rows are fully clickable.
- `reviews/2026-02-04.html`
  - Example review layout. New reviews should follow this format.
- `styles.css`
  - Fonts: Space Grotesk (main), IBM Plex Mono (labels).
  - `.paper-grid` for background.
  - `.rule` and `.rule-light` for dividers.

## Review Sections (latest + review pages)
- Main narrative paragraphs.
- Goalscorers (bold title).
- Player of the Match (bold title).
- “Final Whistle” label is bold inside the last paragraph.

## Update Workflow (Manual)
1. Update `index.html` latest review between markers.
2. Create new review file in `reviews/` (copy existing review).
3. Add new entry to `archive.html` between markers.

## Update Workflow (Script)
- Script: `scripts/new_review.py`
- Template: `reviews/template.html`
- Run:
  ```bash
  python3 scripts/new_review.py
  ```
- Behavior:
  - Creates a new review page from template.
  - Updates latest review in `index.html` (replaces marker block).
  - Prepends new archive entry without deleting old ones.
  - Skips duplicate if date slug or match title already exists.

## Notes / Gotchas
- No Edition box in the header anymore.
- Archive entry row is fully clickable (date + dash + match).
- If links or headers look wrong, check for stray markup edits around the masthead.

## If You Need to Revert After Script Test
```bash
git reset --hard HEAD
rm -f reviews/<test-file>.html
```

