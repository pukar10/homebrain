# HomeBrain Web — Agent Instructions

## Purpose

This file gives AI coding agents project-specific instructions for working in the `web/` app. Keep changes simple, modern, and aligned with the existing Next.js App Router structure.

## Current Stack

**Framework**: Next.js
**Router**: App Router
**Language**: TypeScript
**Styling**: Global CSS for now
**Package manager**: npm
**Linting**: ESLint
**Formatting**: Prettier

## Project Structure

```text
web/
├── public/                  # Static files served from the site root
├── src/
│   └── app/
│       ├── globals.css      # Global site styles
│       ├── layout.tsx       # Root layout shared by all pages
│       └── page.tsx         # Home page at "/"
├── .gitignore
├── .prettierignore
├── .prettierrc.json
├── AGENTS.md                # Instructions for AI coding agents working in this app
├── eslint.config.mjs
├── Makefile                 # Shortcut commands for common npm scripts
├── next-env.d.ts            # Auto-generated TypeScript support for Next.js; do not edit
├── package.json
├── package-lock.json
├── README.md
└── tsconfig.json
```

## Commands

```bash
# Setup
# From the repo root
cd web
npm install

# If already inside web/
npm install

# Run dev server (localhost:3000)
npm run dev

# Run lint
npm run lint

# Build
npm run build

# Start production server (localhost:3000)
npm run start
```

## Next.js Guidelines

- This project uses the App Router.
- Use route folders under `src/app`. Examples:
    - `src/app/page.tsx`
    - `src/app/projects/page.tsx`
    - `src/app/experiments/page.tsx`
    - `src/app/blog/page.tsx`

Use the core App Router files correctly:
- `layout.tsx` wraps pages and defines the shared shell.
- `page.tsx` defines the UI for a route.
- `globals.css` contains global styles imported by the root layout.

## Dependencies

- Use `npm` and keep `package-lock.json`.
- Do not use yarn or pnpm unless the project intentionally changes package managers.
- Prefer built-in Next.js, React, and TypeScript features before adding dependencies.
- Ask before adding UI libraries, state libraries, auth libraries, database clients, or testing frameworks.

## Server and Client Components

Prefer Server Components by default.

Only add `"use client"` when the component needs browser-only behavior, such as:
- React state
- Event handlers
- Browser APIs
- Animations that need client-side JavaScript
- Interactive UI controls

## TypeScript Guidelines

- Use TypeScript for app code.
- Prefer .tsx for React components and pages.
- Use simple, readable types.

Good Examples:
```ts
type ButtonProps = { 
  label: string; 
};

function Button({ label }: ButtonProps) { 
  return <button>{label}</button>; 
}
```

### TypeScript Types

- Avoid using `any` unless there is a clear reason.
- Prefer `unknown` when a value’s type is not known yet.
- Narrow `unknown` before using it.
- Use optional props only when the prop is truly optional.

Example:

```ts
type CardProps = {
  title: string;
  description?: string;
};
```

## Components Guidelines

- Keep components small and focused.
- A good pattern as the app grows:

```txt
src/ 
├── app/ 
│   └── page.tsx 
├── components/  
│   ├── site-header.tsx 
│   ├── site-footer.tsx 
│   └── card.tsx 
└── lib/ 
    └── utils.ts
```

- Use `src/components/` for reusable UI components.
- Use `src/lib/` for shared helpers, constants, and utility functions.
- Do not create many folders too early. Add structure when the project actually needs it.

## Styling Guidelines

- Use `src/app/globals.css` for global styles.
- Keep styling simple until the app needs a design system.
- Prefer readable class names and plain CSS for now.
- Do not add Tailwind, shadcn/ui, or another styling library unless requested.

## Performance Guidelines

Keep the app lightweight.

Prefer:
- Server Components
- Static rendering when possible
- Minimal dependencies
- Small client-side bundles
- next/image for important images
- Simple CSS over heavy UI libraries

Avoid:
- Adding large libraries for small features
- Making the whole app client-rendered
- Putting unnecessary state high in the tree
- Fetching data on the client when it can be rendered on the server

## Code Style

Write code that feels boring, clean, and obvious.

Prefer:
- Clear names
- Small functions
- Simple components
- Standard Next.js patterns
- Minimal dependencies
- Readable TypeScript
- Good comments only when helpful

Avoid:
- Clever abstractions
- Premature optimization
- Large framework changes
- Mixing App Router and Pages Router patterns
- Adding tools without a clear benefit

## Comments

Use comments to explain why something exists, not what obvious code does.

Good Example:

```ts
// Keep metadata here so every route gets a useful default title. 
export const metadata = { 
  title: "HomeBrain",
  description: "Personal homelab AI assistant", 
};
```

Bad Example:

```ts
// Return a main element 
return <main>HomeBrain</main>;
```

## Git Workflow

### Branch Naming

```text
<name>/<type>-<ticket_id>-<title>
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):
- `feat:` — New feature
- `fix:` — Bug fix
- `chore:` — Maintenance, deps, config
- `docs:` — Documentation only
- `test:` — Adding or updating tests
- `refactor:` — Code change with no behavior change
- `ci:` — CI/CD pipeline changes

### Merging

Squash and merge. PR title becomes the commit message and must follow Conventional Commits.

## Boundaries

Do NOT:
- Commit directly to `main`; use a branch and pull request.
- Edit `next-env.d.ts`; it is generated by Next.js.
- Edit generated folders such as `.next/`, `node_modules/`, or build output.
- Change package managers; this project uses npm.
- Add dependencies without a clear reason.
- Mix App Router and Pages Router patterns.
- Move routes outside `src/app`.
- Add large abstractions or frameworks before the project needs them.
- Leave unnecessary `console.log()` statements in committed code.
- Keep changes focused and incremental; avoid large, unrelated edits in a single pass.
- Do not add a test framework unless requested.

## Definition of Done

Before considering work complete:

- Run `npm run lint`.
- Run `npm run build`.
- Confirm the app still uses the App Router under `src/app`.
- Confirm no unnecessary dependencies were added.
- Keep changes small and focused.