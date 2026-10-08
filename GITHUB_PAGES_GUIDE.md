# FORGE - GitHub Pages Deployment Guide

## Overview
FORGE is configured for deployment to GitHub Pages. The frontend builds as a
static site hosted directly on GitHub via the `Deploy to GitHub Pages` workflow
(`.github/workflows/deploy-pages.yml`: triggers on push to `main` and manual
dispatch; sets up Node 22, runs `npm ci` and `npm run build` in `forge_web/`,
and uploads `forge_web/dist` as the Pages artifact). As of 2026-09-24.

> Note: the deployed site is the offline-first coach console. It does **not**
> include the Python API server; features requiring `/api/*` need the backend
> running separately (see `README.md`).

## Configuration

- **Vite base path**: `forge_web/vite.config.ts` sets `base: '/forge/'`. This must match the repository name (see Step 3).
- **Build output**: `npm run build` generates static files in `forge_web/dist/`, uploaded as the Pages artifact.
- **Branding**: page title "FORGE - Elite Strength & Conditioning Coach Console" with SEO meta description in `forge_web/index.html`.

## Deployment Steps

### Step 1: Push to GitHub
```bash
git push origin main   # the deploy-pages workflow runs automatically
```

### Step 2: Enable GitHub Pages
1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions** (recommended)
   - OR select **Deploy from a branch** and choose `main` → `/forge_web/dist` folder

### Step 3: Configure Repository Name
The deployment URL will be:
```
https://<your-github-username>.github.io/forge/
```

**Important**: The repository should ideally be named `forge` for this URL structure. If named differently, update the `base` path in `vite.config.ts`:
```typescript
base: '/<repository-name>/',
```

### Step 4: Manual Deployment (Optional)
You can trigger a manual deployment:
1. Go to **Actions** tab in your GitHub repository
2. Select "Deploy to GitHub Pages" workflow
3. Click "Run workflow" → "Run workflow" button

## Build Output
After running `npm run build`, the `dist/` folder contains:
```
dist/
├── index.html              # Main HTML entry point
└── assets/
    ├── index-[hash].css   # Compiled styles
    └── index-[hash].js    # Compiled JavaScript
```

## Local Testing
Test the production build locally:
```bash
cd forge_web
npm run build
npx serve dist
```
Then visit: `http://localhost:3000/forge/`

## Key Features Available

### Exercise Library
- Frontend seed: 537 exercises + 222 complexes; backend engine data: 334
  (authoritative counts and schema: `docs/DATA_MODEL.md`)
- Complete metadata: coaching cues, common faults, contraindications
- Equipment alternatives and progression pathways
- Searchable and filterable interface

### Program Generation
- Sport-specific programming (Cricket, Tennis, Rugby, Basketball, etc.)
- Periodized training blocks
- Position/role-based customization
- Seasonal phase modulation

### Offline-First Philosophy
- "AI Enhanced, Never AI Dependent"
- All core features work without AI
- Rule-based engine produces credible programs

## Troubleshooting

### Build Fails
```bash
cd forge_web
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 404 Errors on GitHub Pages
- Ensure `base: '/forge/'` matches your repository name
- Check that the GitHub Pages workflow completed successfully
- Verify in **Actions** tab that deployment succeeded

### Blank Page After Deployment
- Open browser DevTools Console (F12)
- Check for CORS errors or missing assets
- Ensure repository is public (or GitHub Pages is enabled for private repos)

## Next Steps

1. **Push code to GitHub**
2. **Enable GitHub Pages** in repository settings
3. **Wait for deployment** (~2-5 minutes)
4. **Share the URL** with coaches and athletes

---

**Forge Philosophy**: *AI Enhanced, Never AI Dependent*  
All features work without cloud connectivity, ensuring reliability and data integrity.
