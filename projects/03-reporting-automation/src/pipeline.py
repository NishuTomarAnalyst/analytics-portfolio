"""Small, auditable reporting pipeline for approved CSV inputs."""
from __future__ import annotations

import json
import sys
from pathlib import Path
import pandas as pd

REQUIRED = {"student_id", "center_id", "score", "attendance_rate", "mentor_score"}


def validate(df: pd.DataFrame) -> dict:
    missing_columns = sorted(REQUIRED - set(df.columns))
    duplicate_ids = int(df.duplicated(["student_id", "center_id"]).sum()) if not missing_columns else None
    invalid_scores = int((~df["score"].between(0, 100)).sum()) if "score" in df else None
    invalid_attendance = int((~df["attendance_rate"].between(0, 1)).sum()) if "attendance_rate" in df else None
    return {
        "rows": len(df),
        "missing_columns": missing_columns,
        "duplicate_student_center_keys": duplicate_ids,
        "invalid_scores": invalid_scores,
        "invalid_attendance_rates": invalid_attendance,
    }


def transform(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["potential_score"] = (
        result["score"] * 0.35
        + result["attendance_rate"] * 100 * 0.35
        + result["mentor_score"] * 0.30
    )
    result["priority"] = pd.cut(
        result["potential_score"],
        bins=[-1, 60, 85, 101],
        labels=["P2", "P1", "P0"],
    )
    return result


def run(input_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_path)
    report = validate(df)
    (output_dir / "validation.json").write_text(json.dumps(report, indent=2))
    if report["missing_columns"] or report["invalid_scores"] or report["invalid_attendance_rates"]:
        raise ValueError(f"Validation failed: {report}")
    transformed = transform(df)
    transformed.to_csv(output_dir / "student_priority.csv", index=False)
    transformed.groupby("center_id", as_index=False).agg(
        students=("student_id", "nunique"),
        average_score=("score", "mean"),
        average_attendance=("attendance_rate", "mean"),
        p0_students=("priority", lambda value: int((value == "P0").sum())),
    ).to_csv(output_dir / "center_summary.csv", index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: pipeline.py INPUT.csv OUTPUT_DIR")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
