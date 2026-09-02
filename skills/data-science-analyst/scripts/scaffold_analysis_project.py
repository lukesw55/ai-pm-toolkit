#!/usr/bin/env python3
"""
Create a reproducible data analysis project skeleton.

Usage:
    python3 scripts/scaffold_analysis_project.py my-analysis-project
"""

from __future__ import annotations

import argparse
from pathlib import Path


README = """# {name}

Reproducible data analysis project.

## Objective

Describe the decision or question this project supports.

## Data Sources

| Source | Path | Owner | Grain | Notes |
|---|---|---|---|---|

## Reproduce

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Project Structure

- `data/raw`: original data; never overwrite
- `data/interim`: temporary intermediate files
- `data/processed`: cleaned/model-ready outputs
- `notebooks`: narrative exploration
- `src`: reusable logic
- `sql`: queries and metric definitions
- `reports/figures`: saved charts
- `reports/final`: final reports
- `models`: model artifacts and metrics
- `tests`: data and unit tests
"""

REQUIREMENTS = """pandas
numpy
matplotlib
scikit-learn
jupyter
"""

GITIGNORE = """.venv/
__pycache__/
.ipynb_checkpoints/
.DS_Store
data/raw/*
data/interim/*
data/processed/*
models/*
reports/figures/*
!data/raw/.gitkeep
!data/interim/.gitkeep
!data/processed/.gitkeep
!models/.gitkeep
!reports/figures/.gitkeep
"""

ANALYSIS_TEMPLATE = """# Analysis Notebook Template

## Objective

## Data Sources

## Assumptions

## Data Audit

## Analysis

## Validation Checks

## Findings

## Limitations

## Next Steps
"""

SRC_INIT = '"""Reusable analysis functions."""\n'


def touch(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def scaffold(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)

    dirs = [
        "data/raw",
        "data/interim",
        "data/processed",
        "notebooks",
        "src",
        "sql",
        "reports/figures",
        "reports/final",
        "models",
        "tests",
    ]

    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)
        touch(root / d / ".gitkeep")

    touch(root / "README.md", README.format(name=root.name))
    touch(root / "requirements.txt", REQUIREMENTS)
    touch(root / ".gitignore", GITIGNORE)
    touch(root / "notebooks" / "00_analysis_template.md", ANALYSIS_TEMPLATE)
    touch(root / "src" / "__init__.py", SRC_INIT)
    touch(root / "sql" / "README.md", "# SQL\n\nStore metric definitions and validation queries here.\n")
    touch(root / "reports" / "final" / "README.md", "# Final Reports\n\nStore decision-ready reports here.\n")
    touch(root / "tests" / "README.md", "# Tests\n\nStore data quality and unit tests here.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a data analysis project skeleton.")
    parser.add_argument("project_dir", type=Path)
    args = parser.parse_args()
    scaffold(args.project_dir)
    print(f"Created project skeleton at {args.project_dir}")


if __name__ == "__main__":
    main()
