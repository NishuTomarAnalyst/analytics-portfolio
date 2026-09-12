from pathlib import Path

ROOT = Path(__file__).parent

required = [
    "README.md",
    "PROJECT_EVIDENCE.md",
    "assets/dealer-nps-dashboard.jpg",
    "assets/revenue-retention-dashboard.jpg",
    "assets/reporting-automation-dashboard.jpg",
    "assets/bigquery-optimization-dashboard.jpg",
    "assets/airflow-etl-dashboard.jpg",
]

missing = [path for path in required if not (ROOT / path).is_file()]
if missing:
    raise SystemExit(f"Missing required files: {missing}")

for readme in sorted((ROOT / "projects").glob("*/README.md")):
    text = readme.read_text(encoding="utf-8")
    for section in ("## Business decision", "## Data model", "## Validation", "## Evidence status"):
        if section not in text:
            raise SystemExit(f"{readme}: missing {section}")

print("Portfolio structure checks passed.")
