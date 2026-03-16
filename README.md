# sveltekit-svelte5-tailwind-skill

Comprehensive skill for building with SvelteKit 2, Svelte 5, and Tailwind CSS v4.

## Status

- Current version: `1.2.0`
- Last updated: `2026-03-16`
- Targets: `@sveltejs/kit 2.x`, `svelte 5.x`, `tailwindcss 4.x`

## What This Skill Contains

- `SKILL.md`: integration workflow and usage guidance
- `agents/openai.yaml`: UI metadata for skill pickers
- `scripts/rebuild_search_indexes.py`: rebuilds `index.jsonl` and `sections.jsonl`
- `references/`: 17 problem-focused guides
- `docs/`: 7 reference guides
- Search indexes (`index.jsonl`, `sections.jsonl`) for both collections

## Key Updates in v1.2.0

- Aligned `SKILL.md` frontmatter with the current skill spec (`name` + `description` only)
- Added `agents/openai.yaml` for UI metadata
- Refreshed Tailwind v4 guidance around automatic source detection, `@source`, `@source inline()`, and CSS-driven dark mode
- Updated primary examples to prefer `$props()` and Svelte class objects/arrays in main guidance
- Prefer `npx sv add tailwindcss` in quick start, while keeping manual setup as fallback
- Added a local script to rebuild search indexes and synced metadata/offsets

## Quick Start

```bash
# 1) scaffold
npx sv create my-app
cd my-app

# 2) add tailwind through the official Svelte addon
npx sv add tailwindcss

# 3) fallback manual path when you need explicit wiring
# npm install -D tailwindcss @tailwindcss/vite
# vite.config.js -> tailwindcss() must be before sveltekit()
# src/app.css -> @import "tailwindcss";
# src/routes/+layout.svelte -> import '../app.css'

# 4) run
npm run dev
```

## SSR Notes

- Do not call browser APIs directly during SSR render.
- Keep browser-only work inside `browser` checks and/or `$effect()`.
- Prefer `load` + `$props()` to hydrate page state.

## Repository Layout

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/rebuild_search_indexes.py`
- `skill.manifest.json`
- `references/`
- `docs/`

## License

MIT
