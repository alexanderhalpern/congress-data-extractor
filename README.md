# Congress Field Hearings

Fetches House Oversight Committee hearing data and populates an Excel spreadsheet using Anthropic API.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set keys in `.env`:
```
ANTHROPIC_API_KEY=...  # https://platform.claude.com/settings/keys
CONGRESS_API_KEY=...  # https://api.congress.gov/sign-up/
ANTHROPIC_MODEL=claude-haiku-4-5
```

## Run

```bash
python main.py
```

Test mode (4 URLs):
```bash
python main.py --test 4
```

> Make sure you're off a VPN — Cloudflare blocks VPN IPs for older hearing pages.

## Output

Results saved to `out/Oversight_YYYYMMDD_HHMMSS.xlsx`. Caches in `out/results_cache.json` and `out/fetch_cache.json` allow resuming interrupted runs.

## Key files

| File | What to change |
|---|---|
| `.env` | API keys, LLM model |
| `in/congress.txt` | URLs to process |
| `in/Oversight.xlsx` | Output spreadsheet template |
| `schema.py` | LLM prompt and output schema |
| `models.py` | Pydantic models for LLM output |
