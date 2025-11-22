# Bernalytics

Track LinkedIn job postings in Berlin for Data Engineering roles.

## What It Does

Counts three LinkedIn search terms and displays results:
- `"Data Engineer"` 
- `"Junior Data Engineer"`
- `"Senior Data Engineer"`

## Setup

```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
just setup

# Configure (add your SERP API key)
cp .env.example .env
nano .env
```

Get free SERP API key at: https://serpapi.com (100 searches/month)

## Usage

```bash
just run
```

Or:
```bash
python -m bernalytics.main
```

## Output

```
============================================================
Week Starting: 2025-11-17
Location: Berlin, Germany
------------------------------------------------------------
"Data Engineer":           237 results
"Junior Data Engineer":     10 results
"Senior Data Engineer":    191 results
============================================================
```

## Configuration

Edit `.env`:
```env
SERP_API_KEY=your_key_here
LOCATION=Berlin, Germany
TIME_PERIOD=week
```

## API Usage

- 3 searches per run
- Free tier: 100 searches/month
- Check usage: https://serpapi.com/dashboard

## License

MIT
