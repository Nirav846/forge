# FORGE - GitHub Pages Deployment Guide

## Overview
FORGE is now configured for deployment to GitHub Pages. The application builds as a static site that can be hosted directly on GitHub.

## ✅ What's Been Configured

### 1. **Exercise Library Button on Home Page**
- Added prominent "Exercise Library" button on the Entry Screen
- Styled with emerald/teal gradient for visibility
- Displays: "Browse 334+ exercises with coaching cues, faults & alternatives"
- Direct access to the full exercise library without creating a program first

### 2. **GitHub Pages Deployment**
- **Vite Configuration**: Updated `vite.config.ts` with `base: '/forge/'`
- **GitHub Actions Workflow**: Created `.github/workflows/deploy-pages.yml`
- **Build Process**: Production build generates static files in `forge_web/dist/`

### 3. **Branding Updates**
- Updated page title: "FORGE - Elite Strength & Conditioning Coach Console"
- Added meta description for SEO

## 🚀 Deployment Steps

### Step 1: Push to GitHub
```bash
cd /workspace
git add .
git commit -m "Add Exercise Library button and GitHub Pages config"
git push origin main
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

## 📁 Build Output
After running `npm run build`, the `dist/` folder contains:
```
dist/
├── index.html              # Main HTML entry point
└── assets/
    ├── index-[hash].css   # Compiled styles
    └── index-[hash].js    # Compiled JavaScript
```

## 🔧 Local Testing
Test the production build locally:
```bash
cd forge_web
npm run build
npx serve dist
```
Then visit: `http://localhost:3000/forge/`

## 🎯 Key Features Available

### Exercise Library (Now on Home Page!)
- **334 exercises** across 21 movement families
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

## 🐛 Troubleshooting

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

## 📝 Next Steps

1. **Push code to GitHub**
2. **Enable GitHub Pages** in repository settings
3. **Wait for deployment** (~2-5 minutes)
4. **Share the URL** with coaches and athletes

---

**Forge Philosophy**: *AI Enhanced, Never AI Dependent*  
All features work without cloud connectivity, ensuring reliability and data integrity.
