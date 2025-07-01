#!/usr/bin/env python3
"""Data preprocessing utilities for QuantForge."""
from pathlib import Path
import argparse
import pandas as pd

from fetch_data import resample_data, default_processed_path


def preprocess(csv_path: Path, interval: str, output: Path | None = None) -> Path:
    df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
    resampled = resample_data(df, interval)
    out_path = output if output else default_processed_path(csv_path, interval)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    resampled.to_csv(out_path)
    print(f"Saved resampled data to {out_path}")
    return out_path


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description='Resample existing CSV data')
    parser.add_argument('csv', help='Path to raw CSV data')
    parser.add_argument('--interval', required=True, help='New interval e.g., 1h')
    parser.add_argument('--output', help='Output CSV path')
    args = parser.parse_args(argv)
    preprocess(Path(args.csv), args.interval, Path(args.output) if args.output else None)


if __name__ == '__main__':
    main()
