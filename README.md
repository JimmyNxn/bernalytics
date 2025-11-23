# Bernalytics

Track LinkedIn job postings in Berlin for Data Engineering roles with automated weekly collection and Supabase database storage.

## Features

- 📊 Tracks weekly LinkedIn job postings for Data Engineering roles in Berlin
- 🗄️ Stores historical data in Supabase PostgreSQL database
- 🤖 Automated collection via GitHub Actions (runs every Monday at 9 AM UTC)
- 📈 Query and analyze trends over time

## What It Tracks

Three search categories from the **past week**:
- **"Data Engineer"** - All Data Engineer positions (~419/week)
- **"Junior Data Engineer"** - Entry-level positions (~74/week)
- **"Senior Data Engineer"** - Senior-level positions (~115/week)

## Quick Start

### 1. Install Dependencies

```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repo and install
git clone <your-repo-url>
cd bernalytics
uv sync
```

### 2. Get API Key

1. Sign up at [serpapi.com](https://serpapi.com) (free tier: 100 searches/month)
2. Copy your API key from the dashboard

### 3. Configure Environment

```bash
cp .env.example .env
nano .env
```

Add your SERP API key:
```env
SERP_API_KEY=your_serp_api_key_here
LOCATION=Berlin, Germany
TIME_PERIOD=week
```

### 4. Run It

```bash
# Display results only (no database)
uv run python -m bernalytics.main

# Or use just commands
just run
```

Expected output:
```
============================================================
Week Starting: 2025-11-17
Location: Berlin, Germany
------------------------------------------------------------
"Data Engineer":           419 results
"Junior Data Engineer":     74 results
"Senior Data Engineer":    115 results
============================================================
```

## Database Setup (Optional)

To store and track historical data:

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Click **"New Project"**
3. Fill in:
   - Name: `bernalytics`
   - Database Password: (generate and save it)
   - Region: `eu-central-1` (or closest to you)
4. Wait ~2 minutes for setup

### 2. Create Database Table

1. In Supabase dashboard: **SQL Editor** → **New Query**
2. Copy the contents of `sql/schema.sql` from this repo
3. Paste and click **"Run"**

### 3. Get Credentials

1. In Supabase: **Settings** → **API**
2. Copy these values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhbGc...` (long string)

### 4. Update Environment

Add to your `.env` file:
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...your_anon_key_here
```

### 5. Test Database Connection

```bash
# Run with database write
uv run python -m bernalytics.main --write-to-db

# Or use just command
just run-db

# View stored data
uv run python -m bernalytics.view_data
```

You should see:
```
====================================================================================================
Job Count History for Berlin, Germany
====================================================================================================
Week Starting     Data Engineer     Junior     Senior      Total Collected At
----------------------------------------------------------------------------------------------------
2025-11-17                  419         74        115        608 2025-11-23
====================================================================================================
```

## GitHub Actions Automation

Automatically collect data every week:

### 1. Add GitHub Secrets

In your GitHub repo:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"** and add:
   - `SERP_API_KEY` = your SERP API key
   - `SUPABASE_URL` = your Supabase URL
   - `SUPABASE_KEY` = your Supabase anon key

### 2. Test the Workflow

1. Go to **Actions** tab in your repo
2. Select **"Collect Job Data"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait ~30 seconds for completion
5. Check your Supabase table for new data

### 3. Schedule

The workflow runs automatically:
- **When**: Every Monday at 9:00 AM UTC
- **What**: Collects job counts and saves to Supabase
- **Cost**: Free (uses ~12 of 100 monthly SERP API calls)

## Commands Reference

```bash
# Display job counts (no database)
just run
uv run python -m bernalytics.main

# Collect and save to database
just run-db
uv run python -m bernalytics.main --write-to-db

# View historical data
uv run python -m bernalytics.view_data

# Run tests
just test

# Clean build artifacts
just clean

# Install/update dependencies
uv sync
```

## Project Structure

```
bernalytics/
├── .github/workflows/
│   └── collect-job-data.yml    # GitHub Actions automation
├── sql/
│   ├── schema.sql              # Database schema
│   └── queries.sql             # Sample analytical queries
├── src/bernalytics/
│   ├── api/
│   │   └── serp_client.py      # SERP API client
│   ├── utils/
│   │   └── config.py           # Configuration management
│   ├── database.py             # Supabase database client
│   ├── main.py                 # Main entry point
│   ├── models.py               # Pydantic data models
│   └── view_data.py            # View stored data
├── .env.example                # Example environment file
├── pyproject.toml              # Python dependencies
├── justfile                    # Command shortcuts
└── README.md                   # This file
```

## Database Schema

The `job_counts` table stores:
- `id` - Unique identifier
- `collected_at` - Timestamp of collection
- `week_starting` - Monday of the week (used for grouping)
- `location` - Location string (e.g., "Berlin, Germany")
- `data_engineer` - Total Data Engineer count
- `junior_data_engineer` - Junior Data Engineer count
- `senior_data_engineer` - Senior Data Engineer count

**Unique constraint**: `(week_starting, location)` prevents duplicates

## Sample Queries

Query your data in Supabase SQL Editor:

```sql
-- View all data
SELECT * FROM job_counts ORDER BY week_starting DESC;

-- Week-over-week change
SELECT 
  week_starting,
  data_engineer,
  data_engineer - LAG(data_engineer) OVER (ORDER BY week_starting) as weekly_change
FROM job_counts
ORDER BY week_starting DESC;

-- Monthly averages
SELECT 
  DATE_TRUNC('month', week_starting) as month,
  ROUND(AVG(data_engineer)) as avg_data_engineer,
  ROUND(AVG(junior_data_engineer)) as avg_junior,
  ROUND(AVG(senior_data_engineer)) as avg_senior
FROM job_counts
GROUP BY month
ORDER BY month DESC;
```

More queries available in `sql/queries.sql`.

## Troubleshooting

### "Missing Supabase credentials"
Add `SUPABASE_URL` and `SUPABASE_KEY` to your `.env` file or GitHub Secrets.

### "SERP API key required"
Add `SERP_API_KEY` to your `.env` file or GitHub Secrets.

### GitHub Action fails
1. Check **Actions** tab for detailed logs
2. Verify all three secrets are set correctly
3. Test locally first with `just run-db`

### No data in Supabase
1. Verify table exists: **Table Editor** → `job_counts`
2. Re-run `sql/schema.sql` if needed
3. Check Supabase **Logs** → **Postgres Logs**

## API Usage & Costs

### SERP API (Free Tier)
- **Limit**: 100 searches/month
- **Usage**: 3 searches per run
- **Weekly automation**: ~12 searches/month
- **Headroom**: 88 searches/month for testing

### Supabase (Free Tier)
- **Database**: 500 MB
- **Bandwidth**: 5 GB/month
- **Our usage**: <1 MB/year
- **Effectively unlimited** for this use case

### GitHub Actions (Free Tier)
- **Limit**: 2,000 minutes/month
- **Usage**: ~2 minutes/month
- **Effectively unlimited**

**Total monthly cost: $0** (all free tiers)

## How It Works

1. **Data Collection**: Uses SERP API to search Google for LinkedIn job postings
2. **Time Filter**: Only counts jobs posted in the past week
3. **Location Filter**: Specific to Berlin, Germany
4. **Storage**: Saves results to Supabase with timestamp
5. **Automation**: GitHub Actions runs every Monday at 9 AM UTC

### The Search Query

The tool searches Google with:
```
"Data Engineer" Berlin site:linkedin.com/jobs
```

With a time filter for the past week (`tbs=qdr:w`).

### API Quirk

Google's API has a quirk: it returns `total_results` more reliably with `num=10` than `num=100`. The code uses `num=10` to get accurate counts.

## Development

### Running Tests
```bash
pytest
# or
just test
```

### Code Quality
```bash
# Format code
black src/

# Lint
ruff check src/

# Type checking
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- Check logs in GitHub Actions for automation issues
- Review Supabase logs for database issues
- Test locally with `just run-db` before debugging automation

## Future Enhancements

Ideas for extending this project:
- 📊 Build a dashboard (Streamlit, Grafana, Metabase)
- 🌍 Track multiple cities
- 💼 Track additional job titles
- 🔔 Add alerts for significant changes
- 📧 Email weekly summary reports
- 📈 Add data visualizations

---

**Made with ❤️ for the Berlin tech community**
## Frontend Dashboard

A React dashboard is included for visualizing your job data:

### Quick Start

```bash
cd frontend
npm install
npm run dev
```

Dashboard opens at `http://localhost:3000`

### Deploy to GitHub Pages

See [DEPLOY_GITHUB_PAGES.md](DEPLOY_GITHUB_PAGES.md) for complete deployment instructions.

**Quick deploy:**
1. Enable GitHub Pages: Settings → Pages → Source: GitHub Actions
2. Add Environment Secrets to the **github-pages** environment:
   - Go to Settings → Environments → github-pages
   - Add secret: `VITE_SUPABASE_URL` (value from your `.env` file)
   - Add secret: `VITE_SUPABASE_ANON_KEY` (value from your `.env` file)
3. Push to main branch - auto-deploys!

Your dashboard will be live at: `https://your-username.github.io/bernalytics/`

**Note:** The secrets must be added to the **github-pages environment**, not just repository secrets, for the deployment to work correctly.

