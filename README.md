# All-In Bali Website

Static website for All-In Bali, built with HTML and Tailwind CSS (local build).

## Local development

Prerequisites:
- Node.js (LTS recommended)
- npm

Install dependencies:
```bash
npm install
```

Build Tailwind CSS (one-off):
```bash
npm run build:css
```

Watch Tailwind CSS during development:
```bash
npm run watch:css
```

Open any of the HTML files directly in your browser:
- `index.html`
- `services.html`
- `gallery.html`

## Project structure

- `src/input.css` — Tailwind entry file
- `assets/tailwind.css` — compiled CSS (committed for GitHub Pages)
- `tailwind.config.js` — Tailwind config

## GitHub Pages

This site is hosted on GitHub Pages. Since Pages only serves static files, the compiled CSS file is committed:

- Run `npm run build:css` before pushing updates
- Commit `assets/tailwind.css` along with any HTML/CSS changes

