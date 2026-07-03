#!/usr/bin/env python3
"""
Quick dataset profiler for CSV/TSV files.

Usage:
    python scripts/profile_dataset.py data/raw/customers.csv --out reports/dataset_profile.md
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def sniff_dialect(path: Path, sample_size: int = 4096) -> csv.Dialect:
    sample = path.read_text(encoding="utf-8", errors="replace")[:sample_size]
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;|")
    except csv.Error:
        class DefaultDialect(csv.excel):
            delimiter = "\t" if path.suffix.lower() in {".tsv", ".tab"} else ","
        return DefaultDialect


def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip() == "" or value.strip().lower() in {"na", "n/a", "null", "none", "nan"}


THOUSANDS_RE = re.compile(r"^-?\d{1,3}(,\d{3})+(\.\d+)?$")


def try_float(value: str) -> float | None:
    if is_missing(value):
        return None
    text = value.strip()
    # Only strip commas that match the US thousands pattern ("1,234.5").
    # A blanket strip would silently turn European decimals ("1,5") into 15
    # and misclassify the column as numeric.
    if THOUSANDS_RE.match(text):
        text = text.replace(",", "")
    try:
        x = float(text)
        if math.isfinite(x):
            return x
    except ValueError:
        return None
    return None


def profile(path: Path, max_rows: int | None = None) -> dict[str, Any]:
    dialect = sniff_dialect(path)

    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f, dialect=dialect)
        fieldnames = reader.fieldnames or []
        row_count = 0
        missing = Counter()
        uniques: dict[str, set[str]] = defaultdict(set)
        samples: dict[str, list[str]] = defaultdict(list)
        numeric_values: dict[str, list[float]] = defaultdict(list)
        duplicate_row_counter = Counter()

        for row in reader:
            row_count += 1
            row_signature = tuple((col, row.get(col, "")) for col in fieldnames)
            duplicate_row_counter[row_signature] += 1

            for col in fieldnames:
                raw = row.get(col)
                if is_missing(raw):
                    missing[col] += 1
                    continue

                value = str(raw).strip()
                if len(uniques[col]) < 10000:
                    uniques[col].add(value)
                if len(samples[col]) < 5:
                    samples[col].append(value)

                numeric = try_float(value)
                if numeric is not None:
                    numeric_values[col].append(numeric)

            if max_rows is not None and row_count >= max_rows:
                break

    duplicate_rows = sum(count - 1 for count in duplicate_row_counter.values() if count > 1)

    columns = []
    for col in fieldnames:
        nums = numeric_values[col]
        numeric_ratio = len(nums) / max(row_count - missing[col], 1)
        inferred_type = "numeric" if numeric_ratio >= 0.9 and nums else "text/category"

        stats: dict[str, Any] = {}
        if inferred_type == "numeric":
            sorted_nums = sorted(nums)
            stats = {
                "min": sorted_nums[0],
                "median": statistics.median(sorted_nums),
                "mean": statistics.fmean(sorted_nums),
                "max": sorted_nums[-1],
            }

        columns.append({
            "column": col,
            "inferred_type": inferred_type,
            "missing": missing[col],
            "missing_pct": missing[col] / row_count if row_count else 0,
            "n_unique_sampled": len(uniques[col]),
            "sample_values": samples[col],
            "stats": stats,
        })

    return {
        "path": str(path),
        "rows_profiled": row_count,
        "columns": len(fieldnames),
        "delimiter": getattr(dialect, "delimiter", ","),
        "duplicate_rows": duplicate_rows,
        "column_profiles": columns,
        "sample_limited": max_rows is not None,
    }


def fmt_num(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:,.4g}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def to_markdown(result: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Dataset Profile: `{result['path']}`")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Rows profiled | {result['rows_profiled']:,} |")
    lines.append(f"| Columns | {result['columns']:,} |")
    lines.append(f"| Delimiter | `{result['delimiter']}` |")
    lines.append(f"| Duplicate rows | {result['duplicate_rows']:,} |")
    lines.append(f"| Sample limited | {result['sample_limited']} |")
    lines.append("")
    lines.append("## Column Profiles")
    lines.append("")
    lines.append("| Column | Type | Missing | Missing % | Unique sampled | Sample values | Numeric stats |")
    lines.append("|---|---|---:|---:|---:|---|---|")

    for c in result["column_profiles"]:
        samples = ", ".join(str(x).replace("|", "\\|") for x in c["sample_values"])
        if c["stats"]:
            stats = ", ".join(f"{k}={fmt_num(v)}" for k, v in c["stats"].items())
        else:
            stats = ""
        lines.append(
            f"| `{c['column']}` | {c['inferred_type']} | {c['missing']:,} | "
            f"{c['missing_pct']:.1%} | {c['n_unique_sampled']:,} | {samples} | {stats} |"
        )

    lines.append("")
    lines.append("## Recommended Next Checks")
    lines.append("")
    lines.append("- Confirm row grain and primary key.")
    lines.append("- Investigate columns with high missingness.")
    lines.append("- Validate duplicates against business rules.")
    lines.append("- Check numeric outliers and impossible values.")
    lines.append("- Identify PII before sharing outputs.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile a CSV/TSV dataset and emit Markdown.")
    parser.add_argument("path", type=Path, help="Path to CSV/TSV file.")
    parser.add_argument("--out", type=Path, default=None, help="Output Markdown path.")
    parser.add_argument("--max-rows", type=int, default=None, help="Optional row limit for large files.")
    args = parser.parse_args()

    if not args.path.exists():
        raise SystemExit(f"File not found: {args.path}")

    result = profile(args.path, max_rows=args.max_rows)
    markdown = to_markdown(result)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(markdown, encoding="utf-8")
        print(f"Wrote profile to {args.out}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
