from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", default="reports/metrics.json")
    parser.add_argument("--out", default="reports/final_report.md")
    args = parser.parse_args()

    # Read student master report if available, else template
    master_path = Path("reports/final_report_student.md")
    if master_path.exists():
        content = master_path.read_text(encoding="utf-8")
    else:
        content = Path("reports/report_template.md").read_text(encoding="utf-8")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
