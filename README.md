# sveltekit-svelte5-tailwind-skill

Comprehensive skill for building with SvelteKit 2, Svelte 5, and Tailwind CSS v4.

## Status

- Current version: `1.1.1`
- Last updated: `2026-02-26`
- Targets: `@sveltejs/kit 2.x`, `svelte 5.x`, `tailwindcss 4.x`

## What This Skill Contains

- `SKILL.md`: integration workflow and usage guidance
- `references/`: 17 problem-focused guides
- `docs/`: 7 reference guides
- Search indexes (`index.jsonl`, `sections.jsonl`) for both collections

## Key Updates in v1.1.1

- Updated scaffold command to `npx sv create`
- Removed old Tailwind `@next`/alpha wording
- Corrected SSR guidance:
  - `$effect()` is browser-only
  - browser APIs (`window`, `document`, `localStorage`) must be guarded in SSR
  - `$state()` and `$derived()` can participate in SSR render output in components
- Synced index metadata and section offsets

## Quick Start

```bash
# 1) scaffold
npx sv create my-app
cd my-app
npm install

# 2) install tailwind v4
npm install -D tailwindcss @tailwindcss/vite

# 3) configure vite plugins
# tailwindcss() must be before sveltekit()

# 4) add src/app.css
@import "tailwindcss";

# 5) import css in src/routes/+layout.svelte
# import '../app.css'

# 6) run
npm run dev
```

## SSR Notes

- Do not call browser APIs directly during SSR render.
- Keep browser-only work inside `browser` checks and/or `$effect()`.
- Prefer `load` + `$props()` to hydrate page state.

## Repository Layout

- `SKILL.md`
- `skill.manifest.json`
- `references/`
- `docs/`

## License

MIT
