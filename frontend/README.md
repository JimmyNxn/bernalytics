# Bernalytics Dashboard

React frontend for visualizing LinkedIn Data Engineering job posting trends in Berlin.

## Features

- 📊 **Real-time Charts** - Line charts showing job posting trends over time
- 📈 **Statistics Cards** - Current week's stats with week-over-week changes
- 📋 **Data Table** - Detailed view of recent weeks
- 🔄 **Auto-refresh** - Fetch latest data from Supabase
- 🎨 **Modern UI** - Built with React, Tailwind CSS, and Recharts

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Supabase** - Database and backend
- **Recharts** - Data visualization
- **Tailwind CSS** - Styling

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Add your Supabase credentials:

```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_public_key_here
```

Get these from your Supabase dashboard:
- Go to **Settings** → **API**
- Copy the **Project URL** and **anon/public key**

### 3. Run Development Server

```bash
npm run dev
```

The app will open at `http://localhost:3000`

## Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── JobTrendsChart.jsx    # Line chart component
│   │   └── StatsCards.jsx        # Stats cards component
│   ├── lib/
│   │   └── supabase.js           # Supabase client config
│   ├── App.jsx                   # Main application
│   ├── main.jsx                  # Entry point
│   └── index.css                 # Global styles
├── public/                       # Static assets
├── index.html                    # HTML template
├── vite.config.js               # Vite configuration
├── tailwind.config.js           # Tailwind configuration
├── postcss.config.js            # PostCSS configuration
└── package.json                 # Dependencies
```

## Components

### JobTrendsChart

Line chart showing weekly job posting trends for:
- Total Data Engineer positions (blue line)
- Junior positions (green line)
- Senior positions (amber line)

### StatsCards

Three cards showing:
- Total Data Engineer count with week-over-week change
- Junior positions with change
- Senior positions with change

### Data Table

Sortable table showing:
- Week starting date
- Data Engineer count
- Junior count
- Senior count
- Total count

## Deployment

### Option 1: Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Add environment variables in Vercel dashboard:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

### Option 2: Netlify

```bash
# Build
npm run build

# Deploy dist/ folder to Netlify
```

Add environment variables in Netlify dashboard.

### Option 3: GitHub Pages

```bash
# Update vite.config.js with base path
base: '/bernalytics/'

# Build
npm run build

# Deploy dist/ to gh-pages branch
```

## Supabase Configuration

### Enable Row Level Security

The dashboard uses the `anon` key, so you need proper RLS policies.

In Supabase SQL Editor:

```sql
-- Allow anonymous read access
CREATE POLICY "Enable read access for all users" 
ON job_counts FOR SELECT 
USING (true);
```

This is already set up if you ran `sql/schema.sql`.

### CORS Settings

Supabase automatically handles CORS for your frontend domain. No additional configuration needed.

## Customization

### Change Colors

Edit `tailwind.config.js`:

```js
colors: {
  primary: {
    500: '#3b82f6',  // Change this to your brand color
  }
}
```

### Add More Charts

Create new components in `src/components/` and import them in `App.jsx`.

Example - Bar chart for senior vs junior ratio:

```jsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function RatioChart({ data }) {
  // Transform data
  const chartData = data.map(item => ({
    week: new Date(item.week_starting).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    'Junior': item.junior_data_engineer,
    'Senior': item.senior_data_engineer,
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="week" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="Junior" fill="#10b981" />
        <Bar dataKey="Senior" fill="#f59e0b" />
      </BarChart>
    </ResponsiveContainer>
  )
}
```

### Modify Data Fetching

Edit `App.jsx` - `fetchJobData()` function:

```jsx
// Change limit
.limit(24) // Last 24 weeks instead of 12

// Add filters
.eq('location', 'Berlin, Germany')
.gte('week_starting', '2024-01-01')
```

## Troubleshooting

### "Missing Supabase environment variables"

Make sure you:
1. Created `.env` file
2. Added `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`
3. Restarted the dev server

### No data showing

1. Check if data exists in Supabase:
   - Go to Supabase → **Table Editor** → `job_counts`
2. Check browser console for errors
3. Verify RLS policies allow read access

### Charts not rendering

1. Clear browser cache
2. Check if data is being fetched (Network tab)
3. Verify `recharts` is installed: `npm list recharts`

## Performance

- **Initial load**: ~100-200ms
- **Data fetch**: ~50-100ms
- **Chart render**: ~30-50ms

For large datasets (>100 weeks), consider:
- Pagination in the data table
- Virtual scrolling
- Data aggregation on the backend

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT

---

Built with ❤️ for the Berlin tech community