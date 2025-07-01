#!/usr/bin/env python3
"""QuantForge Data Fetcher

Fetch historical OHLCV data using yfinance and optionally resample it.
"""
import argparse
from pathlib import Path
import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'


def fetch_data(ticker: str, start: str, end: str, interval: str) -> pd.DataFrame:
    """Fetch OHLCV data via yfinance.

    The ``yfinance.download`` API can return a multi-index column layout. Using
    ``Ticker.history`` keeps the output flat which simplifies downstream
    processing.
    """
    history = yf.Ticker(ticker).history(
        start=start,
        end=end,
        interval=interval,
        auto_adjust=False,
        actions=False,
    )
    df = history[['Open', 'High', 'Low', 'Close', 'Volume']]
    if df.empty:
        raise ValueError(
            f"No data returned for {ticker} {start} {end} {interval}"
        )
    return df


def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    print(f"Saved {len(df)} rows to {path}")


def resample_data(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    agg = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
    }
    resampled = df.resample(interval).agg(agg)
    resampled = resampled.dropna()
    return resampled


def default_raw_path(ticker: str, start: str, end: str) -> Path:
    fname = f"{ticker}_{start}_{end}.csv"
    return RAW_DIR / fname


def default_processed_path(raw_path: Path, interval: str) -> Path:
    fname = raw_path.stem + f"_{interval}.csv"
    return PROCESSED_DIR / fname


def cmd_fetch(args: argparse.Namespace) -> None:
    df = fetch_data(args.ticker, args.start, args.end, args.interval)
    csv_path = Path(args.output) if args.output else default_raw_path(args.ticker, args.start, args.end)
    save_csv(df, csv_path)
    if args.resample:
        r_df = resample_data(df, args.resample)
        r_path = default_processed_path(csv_path, args.resample)
        save_csv(r_df, r_path)


def cmd_resample(args: argparse.Namespace) -> None:
    csv_path = Path(args.input)
    df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
    r_df = resample_data(df, args.interval)
    out_path = Path(args.output) if args.output else default_processed_path(csv_path, args.interval)
    save_csv(r_df, out_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='QuantForge data utilities')
    sub = parser.add_subparsers(dest='command', required=True)

    f = sub.add_parser('fetch', help='Fetch data from yfinance')
    f.add_argument('ticker', help='Ticker symbol')
    f.add_argument('--start', required=True, help='Start date YYYY-MM-DD')
    f.add_argument('--end', required=True, help='End date YYYY-MM-DD')
    f.add_argument('--interval', default='1d', help='Data interval, e.g., 1d, 1h')
    f.add_argument('--output', help='Output CSV file')
    f.add_argument('--resample', help='Resample interval (e.g., 1h, 1wk)')

    r = sub.add_parser('resample', help='Resample an existing CSV')
    r.add_argument('input', help='Path to CSV file')
    r.add_argument('--interval', required=True, help='New interval like 1h, 1wk')
    r.add_argument('--output', help='Output CSV file')

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == 'fetch':
        cmd_fetch(args)
    elif args.command == 'resample':
        cmd_resample(args)


if __name__ == '__main__':
    main()
