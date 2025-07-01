# QuantForge

QuantForge is a cross-language quant trading research platform. This repository
currently implements **Phase 1**: data ingestion and management using Python.

## Structure

```
quantforge/
├── cmd/              # Go clients (future phases)
├── data/
│   ├── processed/    # Output of resampling
│   └── raw/          # Raw historical data
├── scripts/          # Python utilities
│   ├── fetch_data.py # Fetch and resample data
│   └── preprocess.py # Standalone resampling helper
├── sim/              # Fortran simulation engine (future)
├── main.py           # Entry point running fetch_data
├── Makefile          # Convenience tasks
```

## Phase 1 Usage

1. Install dependencies:

```bash
pip install -r requirements.txt  # currently requires pandas and yfinance
```

2. Fetch historical data:

```bash
python scripts/fetch_data.py fetch AAPL --start 2020-01-01 --end 2020-12-31 --interval 1d
```

This saves data to `data/raw/AAPL_2020-01-01_2020-12-31.csv`.

3. Resample existing CSV:

```bash
python scripts/fetch_data.py resample data/raw/AAPL_2020-01-01_2020-12-31.csv --interval 1h
```

Resampled output is written to `data/processed/`.

The `Makefile` includes a `fetch` target as a shorthand for running the
fetcher. Future phases will add Fortran backtesting and Go real-time
components.
