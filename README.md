# Nandini Mehta — Portfolio

A responsive, interactive project-roadmap portfolio for Nandini Mehta, Software Engineer. The site is built with React, TypeScript, Three.js, and vinext, and is configured for GitHub Pages.

## Local development

Requires Node.js 22 or newer.

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Quality checks

```bash
npm run lint
npm test
```

## Publish with GitHub Pages

1. Push the repository to GitHub using the `main` branch.
2. Open **Settings → Pages** in the GitHub repository.
3. Under **Build and deployment**, choose **GitHub Actions** as the source.
4. The included workflow builds and publishes the portfolio automatically after every push to `main`.

The workflow supports both a user site such as `username.github.io` and a project site such as `username.github.io/portfolio`.

## Main files

- `app/page.tsx` — portfolio content and page structure
- `app/ThreeRoadmap.tsx` — animated Three.js project journey
- `app/globals.css` — visual system and responsive layouts
- `app/layout.tsx` — metadata and typography
- `.github/workflows/deploy-pages.yml` — GitHub Pages deployment
