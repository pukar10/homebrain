# Web

## Getting Started

1. Clone the repo
2. cd web/
3. Install dependencies: `npm install`
4. Start dev server: `npm run dev`  
5. Make edits/changes
6. Run checks before committing: `npm run check`
    - TypeScript check
    - ESLint
    - Prettier format check
    - Production build
7. Format code if needed: `npm run format` and run checks again `npm run check`

- [ ] figure out more useful way to use `Makefile`.

## Stack

- **Framework**: Next.js App Router
- **Language**: TypeScript
- **Package manager**: npm
- **Styling**: Plain CSS for now
- **Linting**: ESLint
- **Formatting**: Prettier

## Project Structure

```text
homebrain/
└── web/
├── public/
    ├── src/
    │   └── app/
    │       ├── globals.css       // Styles for the whole website
    │       ├── layout.tsx        // The main shell that wraps around every page
    │       └── page.tsx          // The homepage you see at "/"
    ├── .gitignore
    ├── .prettierignore           // Files/folders Prettier should not format
    ├── .prettierrc.json          // Prettier formatting rules
    ├── eslint.config.mjs         // Code checker settings
    ├── Makefile                  // Shortcut commands for common npm scripts
    ├── next-env.d.ts             // Auto-generated TypeScript support for Next.js; do not edit
    ├── package.json              // App packages, scripts, and commands
    ├── package-lock.json         // Locks exact npm package versions
    ├── README.md
    └── tsconfig.json             // TypeScript settings
```

**Possible Future Additions:**

| File | Description |
| ---- | ----------- |
| next.config.ts | Special settings file for Next.js app |
| postcss.config.mjs | Settings to helps process CSS/Tailwind<br> If Tailwind is ever used/needed in the future |

