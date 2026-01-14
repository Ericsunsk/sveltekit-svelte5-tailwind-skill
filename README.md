# SvelteKit 2 + Svelte 5 + Tailwind v4 Integration Skill

[![SvelteKit 2](https://img.shields.io/badge/SvelteKit-2.x-ff3e00?logo=svelte&logoColor=white)](https://kit.svelte.dev/)
[![Svelte 5 Stable](https://img.shields.io/badge/Svelte-5.x_Stable-ff3e00?logo=svelte&logoColor=white)](https://svelte.dev/)
[![Tailwind CSS v4 Stable](https://img.shields.io/badge/Tailwind_CSS-v4.x_Stable-06b6d4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A premium, comprehensive Claude skill for building modern web applications with the latest stable versions of SvelteKit 2, Svelte 5 (Runes), and Tailwind CSS v4.

> **✨ Update (January 2026):** Fully audited and updated to reflect the stable release standards of Svelte 5 and Tailwind CSS v4. All references to "preview" or "@next" have been removed in favor of stable production patterns.

## Overview

This skill provides searchable, curated documentation for building full-stack web applications using the modern SvelteKit + Svelte 5 + Tailwind v4 stack. It addresses the unique integration challenges when using these three frameworks together, with a special focus on Svelte 5's runes system and its interaction with server-side rendering.

**Integration Stack:**
- **SvelteKit 2.12+**: Full-stack framework featuring `$app/state`, file-based routing, and idiomatic error/redirect handling.
- **Svelte 5 (Stable)**: Modern reactivity with runes (`$state`, `$derived`, `$effect`, `$props`) and snippets.
- **Tailwind CSS v4 (Stable)**: CSS-first configuration engine with high-performance Vite integration.

## Key Features

- **24 Comprehensive Guides**: Curated deep-dives into setup, architecture, patterns, and troubleshooting.
- **Stable Production Patterns**: Code examples updated to use `$app/state` and snippet-based layouts.
- **Problem-Focused Approach**: Clear ❌ vs ✅ comparisons to prevent common integration pitfalls.
- **Search-Optimized**: Fully indexed sections for instant retrieval by Claude and other AI agents.
- **Research-First Methodology**: Built-in workflows to ensure implementation follows the latest standards.

## Documentation Collections

### `references/` - Problem-Focused Guides (17 files)

Curated guides addressing specific integration challenges:

**Setup & Configuration:**
- `getting-started.md` - Quick start and initial setup
- `project-setup.md` - Complete project configuration

**Core Concepts:**
- `svelte5-runes.md` - Svelte 5 runes system and SSR constraints
- `routing-patterns.md` - File-based routing and layouts
- `server-rendering.md` - SSR/SSG patterns
- `data-loading.md` - Load functions and data flow

**Forms & Styling:**
- `forms-and-actions.md` - Progressive enhancement with form actions
- `styling-with-tailwind.md` - Component styling patterns
- `styling-patterns.md` - Advanced styling techniques

**Deployment & Migration:**
- `deployment-guide.md` - Platform-specific deployment (Vercel, Cloudflare, Node, static)
- `migration-svelte4-to-5.md` - Upgrading from Svelte 4 to 5
- `tailwind-v4-migration.md` - Upgrading from Tailwind v3 to v4

**Optimization & Best Practices:**
- `best-practices.md` - Architecture and conventions
- `performance-optimization.md` - Bundle size, loading, Core Web Vitals

**Troubleshooting:**
- `common-issues.md` - Quick fixes for frequent problems
- `troubleshooting.md` - Systematic debugging methodology

**Search System:**
- `documentation-search-system.md` - Complete search methodology

### `docs/` - Comprehensive Reference (7 files)

Complete API reference and configuration guides:

- `sveltekit-configuration.md` - Complete svelte.config.js and Vite configuration
- `svelte5-api-reference.md` - All Svelte 5 runes and template syntax
- `tailwind-configuration.md` - Tailwind v4 configuration options
- `adapters-reference.md` - Deployment adapter specifications
- `advanced-routing.md` - Advanced SvelteKit routing patterns
- `advanced-ssr.md` - SSR hooks, streaming, optimization
- `integration-patterns.md` - Complete integration examples

## Quick Start

### Installation

```bash
# 1. Create SvelteKit project
npm create svelte@latest my-app
cd my-app
npm install

# 2. Add Tailwind v4
npm install -D tailwindcss @tailwindcss/vite

# 3. Configure Vite (vite.config.js)
import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';

export default {
  plugins: [
    tailwindcss(),  // MUST be before sveltekit()
    sveltekit()
  ]
};

# 4. Create app.css with Tailwind imports
@import "tailwindcss";

# 5. Import CSS in root layout (src/routes/+layout.svelte)
<script>
  let { children } = $props();
  import '../app.css';
</script>

{@render children()}

# 6. Start development server
npm run dev
```

**Critical Configuration Points:**
- Tailwind plugin MUST come before SvelteKit plugin in `vite.config.js`.
- Import CSS in root `+layout.svelte`, not in `app.html`.
- Use the stable `tailwindcss` and `@tailwindcss/vite` packages.
- Migrate from `$app/stores` to `$app/state` for reactive page data.

For complete setup instructions, see `references/getting-started.md`.

## Usage with Claude

This skill is designed to be used with Claude's research-first methodology:

1. **Research First**: Search the documentation to understand the recommended approach
2. **Then Execute**: Implement the solution using discovered patterns and best practices

### How to Search Documentation

The skill uses a 5-stage search process:

**Stage 0: Discover** - Find available indexes
```bash
find . -name "index.jsonl" -type f
```

**Stage 1: Load** - Read relevant index files
```
Read references/index.jsonl  # For how-to guides
Read docs/index.jsonl        # For API reference
```

**Stage 2: Reason** - Identify 3-4 most relevant files based on summaries

**Stage 3: Get Sections** - Read `sections.jsonl` for detailed section metadata

**Stage 4: Read** - Load only relevant sections using offset/limit

**Stage 5: Synthesize** - Combine information and provide complete answer

For complete search methodology, see `references/documentation-search-system.md`.

## Common Integration Challenges

### Svelte 5 Runes in SSR Context

```svelte
<!-- ❌ DON'T: Using $state() in SSR component -->
<script>
  export let data;
  let count = $state(data.count);  // Error: $state not available in SSR
</script>

<!-- ✅ DO: Use client-only component -->
<script>
  export let data;
</script>
<ClientCounter initialCount={data.count} />
```

See: `references/svelte5-runes.md` - Server-Side Constraints

### Progressive Enhancement with Forms

```svelte
<script>
  import { enhance } from '$app/forms';
  let submitting = $state(false);
</script>

<form method="POST" use:enhance={() => {
  submitting = true;
  return async ({ result, update }) => {
    submitting = false;
    await update();
  };
}}>
  <button disabled={submitting}>Submit</button>
</form>
```

See: `references/forms-and-actions.md` - Handling use:enhance Reactivity

### Tailwind Class Purging

```svelte
<!-- ✅ GOOD: Full class names -->
<div class:bg-blue-500={active} class:bg-gray-200={!active}>

<!-- ❌ BAD: Dynamic class parts get purged -->
<div class="bg-{active ? 'blue' : 'gray'}-500">
```

See: `references/styling-with-tailwind.md` - Content Detection and Purging

## Common Issues

**CSS not loading in production**
→ Check: Vite plugin order, CSS import location
→ See: `references/common-issues.md` - CSS Loading Issues

**Runes causing SSR errors**
→ Don't use `$state()` or `$effect()` in SSR components
→ See: `references/svelte5-runes.md` - Server-Side Constraints

**Form losing state on submit**
→ Use manual `enhance()` callback
→ See: `references/forms-and-actions.md` - Handling use:enhance Reactivity

**HMR breaking**
→ Check: Vite plugin order and file watch settings
→ See: `references/common-issues.md` - Hot Module Reload Problems

For systematic troubleshooting, see `references/troubleshooting.md`.

## Version Information

**Supported Versions:**
- **SvelteKit**: 2.x (latest stable)
- **Svelte**: 5.x (with runes)
- **Tailwind CSS**: 4.x (CSS-first configuration)

All code examples and patterns are tested with these versions.

## Distribution Mode

This skill uses **author-only** distribution:
- All content is newly authored original work
- No verbatim copying from vendor documentation
- Source materials used for reference only
- All guides cite influences via `adapted_from` frontmatter

**Referenced Repositories:**
- [sveltejs/kit](https://github.com/sveltejs/kit)
- [sveltejs/svelte](https://github.com/sveltejs/svelte)
- [tailwindlabs/tailwindcss](https://github.com/tailwindlabs/tailwindcss)
- [tailwindlabs/tailwindcss.com](https://github.com/tailwindlabs/tailwindcss.com)

See `provenance.jsonl` for complete source attribution.

## Repository Structure

```
sveltekit-svelte5-tailwind-skill/
├── README.md                          # This file
├── SKILL.md                           # Skill usage guide
├── skill.manifest.json                # Skill metadata
├── provenance.jsonl                   # Source attribution
├── references/                        # Problem-focused guides (17 files)
│   ├── index.jsonl                    # Search index (17 entries)
│   ├── sections.jsonl                 # Section metadata
│   ├── index.meta.json               # Collection metadata
│   └── *.md                           # Guide files
└── docs/                              # Comprehensive references (7 files)
    ├── index.jsonl                    # Search index (7 entries)
    ├── sections.jsonl                 # Section metadata
    ├── index.meta.json               # Collection metadata
    └── *.md                           # Reference files
```

## Statistics

- **Total Files**: 34 committed files
- **Documentation Files**: 24 Markdown guides
- **Total Lines**: 18,881 lines of documentation
- **Indexed Entries**: 24 searchable documents
- **Collections**: 2 (references + docs)
- **Search Depth**: H2-level sections for efficient retrieval

## Getting Help

1. **Start with search**: Use the 5-stage search process in SKILL.md
2. **Check common issues**: `references/common-issues.md` for quick fixes
3. **Systematic debugging**: `references/troubleshooting.md` for methodology
4. **Consult references**: Problem-focused guides for specific topics
5. **Check API docs**: Comprehensive references for configuration details

## License

This skill contains original authored content created for educational purposes. Source repositories were consulted for reference only and are not redistributed. See individual repository licenses for upstream projects:

- SvelteKit: [MIT License](https://github.com/sveltejs/kit/blob/main/LICENSE)
- Svelte: [MIT License](https://github.com/sveltejs/svelte/blob/main/LICENSE.md)
- Tailwind CSS: [MIT License](https://github.com/tailwindlabs/tailwindcss/blob/main/LICENSE)

## Contributing

This skill was generated using the Claude Skill Builder. To report issues or suggest improvements, please open an issue on the skill repository.

## Changelog

### v1.1.0 (2026-01-14)
- **Stable Migration**: Removed all `@next` and "preview" references for Svelte 5 and Tailwind v4.
- **Svelte 5 Snippets**: Updated all layout examples from `<slot />` to `{@render children()}`.
- **SvelteKit 2.12+ State**: Migrated `$app/stores` page usage to `$app/state` for better rune compatibility.
- **Idiomatic Handling**: Removed `throw` from `redirect()` and `error()` calls across the documentation.
- **Comprehensive Audit**: Verified 24 guides for consistency with January 2026 stable standards.

### v1.0.0 (2025-10-28)
- Initial release
- 17 problem-focused guides in `references/`
- 7 comprehensive references in `docs/`
- Complete search indexes for both collections
- Integration-specific patterns and troubleshooting
- Migration guides for Svelte 4→5 and Tailwind v3→v4
