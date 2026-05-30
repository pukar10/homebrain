# Web

## Getting Started

```bash
# 1. Clone repo
git clone https://github.com/pukar10/homebrain.git

# 2. Install dependencies
cd web/
npm install

# 3. Start dev server
npm run dev

# 4. Run checks (TypeScript check, ESLint, Prettier, Build)
npm run check

# 5. Format code
npm run format

# 6 Re-run checks from 5. if needed
```

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

