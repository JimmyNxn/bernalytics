# Deploy to GitHub Pages

Complete guide to deploy your Bernalytics React dashboard to GitHub Pages.

## Quick Setup (5 minutes)

### Step 1: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** → **Pages** (in the left sidebar)
3. Under **Source**, select:
   - **Source**: GitHub Actions
4. Click **Save**

That's it! GitHub Pages is now enabled.

### Step 2: Add GitHub Secrets

Your dashboard needs Supabase credentials. Add them as secrets:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add two secrets:

| Secret Name | Value |
|-------------|-------|
| `VITE_SUPABASE_URL` | `https://your-project-id.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | `eyJhbGc...` (your anon key) |

**Where to get these values:**
- In your local `.env` file: `cat .env | grep SUPABASE`
- Or in Supabase dashboard: **Settings** → **API**

### Step 3: Deploy

The workflow is already set up! Just push to main:

```bash
# From the bernalytics directory
git add .
git commit -m "Setup GitHub Pages deployment"
git push origin main
```

The deployment will start automatically!

### Step 4: Check Deployment

1. Go to the **Actions** tab in your repo
2. Look for the "Deploy Frontend to GitHub Pages" workflow
3. Wait ~2 minutes for it to complete
4. Your dashboard will be live at:

```
https://your-username.github.io/bernalytics/
```

For example: `https://jimmynxn.github.io/bernalytics/`

## How It Works

### Automatic Deployments

The workflow (`deploy-frontend.yml`) automatically deploys when:
- ✅ You push changes to `main` branch
- ✅ Changes are in the `frontend/` directory
- ✅ You manually trigger it from Actions tab

### What Happens During Deployment

1. **Checkout** - Pulls your code
2. **Install** - Runs `npm ci` to install dependencies
3. **Build** - Runs `npm run build` with your Supabase credentials
4. **Upload** - Packages the `dist/` folder
5. **Deploy** - Publishes to GitHub Pages

### Build Configuration

The `vite.config.js` is set up with:
```js
base: "/bernalytics/"
```

This ensures all assets load correctly from the subdirectory.

## Manual Deployment (Alternative)

If you prefer to deploy manually:

### Option 1: Using gh-pages package

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Build and deploy
npm run deploy
```

This builds the app and pushes to the `gh-pages` branch.

### Option 2: Using GitHub CLI

```bash
cd frontend

# Build
npm run build

# Deploy with GitHub CLI
gh-pages -d dist
```

## Verify Deployment

After deployment completes:

1. **Check the Actions tab**
   - Should show green checkmark ✅
   - Click on the workflow run to see details

2. **Visit your site**
   - Go to `https://your-username.github.io/bernalytics/`
   - Should see your dashboard with charts and data

3. **Check browser console**
   - Press F12 to open DevTools
   - Check Console tab for any errors
   - Should show successful data fetch from Supabase

## Troubleshooting

### 404 Page Not Found

**Problem**: Site shows 404 error

**Solutions**:
1. Check if GitHub Pages is enabled: Settings → Pages
2. Verify the source is set to "GitHub Actions"
3. Check the workflow completed successfully in Actions tab
4. Wait 2-3 minutes - GitHub Pages can take time to propagate

### Blank Page

**Problem**: Page loads but shows nothing

**Solutions**:
1. Check browser console (F12) for errors
2. Verify `base: "/bernalytics/"` is set in `vite.config.js`
3. Check if secrets are added: Settings → Secrets → Actions
4. Rebuild: Go to Actions → Re-run workflow

### 401 Unauthorized Error

**Problem**: Data doesn't load, shows "Unauthorized" in console

**Solutions**:
1. Verify GitHub Secrets are set correctly:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
2. Check the secret values match your local `.env`
3. Re-run the deployment workflow after fixing secrets

### Assets Not Loading (CSS/JS missing)

**Problem**: Page looks broken, no styles

**Solutions**:
1. Verify `base: "/bernalytics/"` in `vite.config.js`
2. Check if repo name matches the base path
3. Clear browser cache and hard refresh (Ctrl+Shift+R)

### Workflow Fails to Run

**Problem**: Workflow doesn't start or fails immediately

**Solutions**:
1. Check permissions: Settings → Actions → General → Workflow permissions
2. Enable "Read and write permissions"
3. Check if Node.js setup is correct (using v18)
4. Review error logs in Actions tab

## Custom Domain (Optional)

Want to use your own domain instead of `github.io`?

### Step 1: Add CNAME file

Create `frontend/public/CNAME`:
```
yourdomain.com
```

### Step 2: Configure DNS

Add DNS records at your domain provider:
```
Type: CNAME
Host: www
Value: your-username.github.io
```

### Step 3: Enable in GitHub

1. Go to Settings → Pages
2. Under "Custom domain", enter your domain
3. Check "Enforce HTTPS"

More info: [GitHub Docs - Custom Domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## Updating the Site

Every time you push changes to `main` branch:
- GitHub Actions automatically rebuilds
- New version deploys in ~2 minutes
- No manual steps needed!

### Force Rebuild

To trigger a rebuild without code changes:

1. Go to **Actions** tab
2. Select "Deploy Frontend to GitHub Pages"
3. Click **"Run workflow"** → **"Run workflow"**

## Monitoring

### Check Build Status

Add a badge to your README:

```markdown
![Deploy](https://github.com/your-username/bernalytics/actions/workflows/deploy-frontend.yml/badge.svg)
```

### View Deployment History

1. Go to Actions tab
2. Click on "Deploy Frontend to GitHub Pages"
3. See all previous deployments and their status

## Performance

GitHub Pages is optimized for static sites:
- ⚡ Fast CDN delivery
- 🌍 Global edge network
- 📦 Automatic compression
- 🔒 Free HTTPS

Your dashboard should load in:
- **First visit**: ~500ms
- **Return visits**: ~100ms (cached)

## Costs

**GitHub Pages is 100% FREE for public repositories!**

Limits (rarely hit for dashboards):
- 100 GB bandwidth/month
- 1 GB storage
- 10 builds/hour

## Security Notes

✅ **Safe to deploy**:
- Uses `anon` key (public-safe)
- Row Level Security (RLS) enabled in Supabase
- No sensitive data exposed in frontend code

❌ **Never commit**:
- `.env` file (it's gitignored)
- `service_role` key (not used here)

## Alternative: Deploy Elsewhere

If you prefer other platforms:

### Vercel (Recommended)
```bash
cd frontend
vercel
```
- Fastest deployment
- Auto-previews for PRs
- Free tier included

### Netlify
```bash
cd frontend
npm run build
netlify deploy --prod
```
- Drag & drop deployment
- Form handling
- Free tier included

### Cloudflare Pages
- Connect GitHub repo
- Auto-deploys on push
- Free tier included

## Need Help?

Common resources:
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

Check logs:
- **Actions tab** → Click failed workflow → View error details
- **Browser console** (F12) → Look for JavaScript errors
- **Network tab** → Check if assets are loading

---

## Summary Checklist

Before deploying:
- [ ] GitHub Pages enabled (Settings → Pages → GitHub Actions)
- [ ] Secrets added (`VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`)
- [ ] `base: "/bernalytics/"` set in `vite.config.js`
- [ ] Changes committed and pushed to `main` branch

After deploying:
- [ ] Workflow completed successfully (green ✅)
- [ ] Site loads at `https://username.github.io/bernalytics/`
- [ ] Charts display data correctly
- [ ] No errors in browser console

**Your dashboard will be live at:**
```
https://your-username.github.io/bernalytics/
```

🎉 **Happy deploying!**