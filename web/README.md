# Web

## Project Structure

```text
homebrain/
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
├── next-env.d.ts             // Auto-generated TypeScript support for Next.js; do not edit
├── package.json              // App's installed packages/scripts and commands like npm run dev
├── package-lock.json         // Locks exact npm package versions
├── README.md
└── tsconfig.json             // TypeScript settings
```

**Possible Future Additions:**

| File | Description |
| ---- | ----------- |
| next.config.ts | Special settings file for Next.js app |
| postcss.config.mjs | Settings to helps process CSS/Tailwind<br> If Tailwind is ever used/needed in the future |

