# Setting Up the React Dashboard

## Overview

You now have a complete React dashboard that connects to your Supabase database and visualizes your job data with beautiful charts and statistics.

## What You Get

- 📊 Line chart showing job trends over time
- 📈 Stat cards with week-over-week changes
- 📋 Data table with all historical data
- 🔄 Real-time data refresh
- 📱 Fully responsive design

## Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

This installs:
- React & React DOM
- Supabase JS client
- Recharts (for charts)
- Tailwind CSS (for styling)
- Vite (dev server)

### Step 2: Configure Supabase

Create `.env` file in the `frontend/` directory:

```bash
cd frontend
cp .env.example .env
nano .env
```

Add your Supabase credentials (same as your main project):

```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_public_key_here
```

### Step 3: Run It!

```bash
npm run dev
```

The dashboard will open at `http://localhost:3000`

## What You'll See

### 1. Header
- Project title
- Refresh button to fetch latest data

### 2. Stats Cards
Three cards showing:
- **Total Data Engineer** - All DE jobs this week
- **Junior Positions** - Entry-level jobs
- **Senior Positions** - Senior-level jobs

Each card shows:
- Current week's count
- Week-over-week change (+/- percentage)

### 3. Line Chart
Beautiful visualization showing trends over the last 12 weeks:
- Blue line = Total Data Engineer
- Green line = Junior positions
- Amber line = Senior positions

### 4. Data Table
Scrollable table with all your historical data

## Deploying to Production

### Option 1: Vercel (Easiest - Free)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel
```

Follow the prompts and add your environment variables when asked.

**Live in 2 minutes!** 🚀

### Option 2: Netlify (Also Free)

```bash
# Build
cd frontend
npm run build

# Drag and drop the dist/ folder to netlify.com/drop
```

Or connect your GitHub repo to Netlify for auto-deploys.

### Option 3: GitHub Pages

Add to `vite.config.js`:
```js
base: '/bernalytics/'
```

Build and deploy:
```bash
npm run build
# Deploy dist/ folder to gh-pages branch
```

## Customization Ideas

### Change Colors

Edit `tailwind.config.js`:
```js
colors: {
  primary: {
    500: '#your-color',
  }
}
```

### Add More Data

Edit `App.jsx`:
```js
.limit(24) // Show last 24 weeks instead of 12
```

### Add New Charts

Examples:
- Bar chart comparing junior vs senior
- Pie chart showing distribution
- Area chart for total market size
- Growth rate indicators

## Troubleshooting

### Port already in use
```bash
# Change port in vite.config.js
server: {
  port: 3001,  // Use different port
}
```

### Data not showing
1. Check if data exists in Supabase
2. Check browser console for errors
3. Verify `.env` has correct credentials
4. Make sure you ran the data collection script

### Build errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## What's Next?

Once your dashboard is running:

1. **Share it** - Deploy to Vercel and share the URL
2. **Monitor trends** - Check weekly to see job market changes
3. **Expand tracking** - Add more cities or job titles
4. **Add alerts** - Get notified of big changes
5. **Export data** - Add CSV download feature

## File Structure

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── JobTrendsChart.jsx
│   │   └── StatsCards.jsx
│   ├── lib/
│   │   └── supabase.js   # Supabase config
│   ├── App.jsx           # Main app
│   ├── main.jsx          # Entry point
│   └── index.css         # Styles
├── index.html            # HTML template
├── vite.config.js        # Vite config
├── tailwind.config.js    # Tailwind config
└── package.json          # Dependencies
```

## Commands Reference

```bash
# Development
npm run dev          # Start dev server

# Production
npm run build        # Build for production
npm run preview      # Preview production build

# Maintenance
npm install          # Install dependencies
npm update           # Update dependencies
npm audit            # Check for vulnerabilities
```

## Resources

- [React Docs](https://react.dev)
- [Supabase Docs](https://supabase.com/docs)
- [Recharts Docs](https://recharts.org)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [Vite Docs](https://vitejs.dev)

---

**Need help?** Check the browser console for errors or open an issue on GitHub.
