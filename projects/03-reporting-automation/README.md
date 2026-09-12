# Automated Student Reporting System

![Dashboard](../../assets/reporting-automation-dashboard.jpg)

## Business decision

Give operations teams one controlled process for preparing, validating and delivering recurring center-level reports.

## Workflow

```text
Extract -> Standardize -> Validate -> Apply rules -> Build reports -> Deliver -> Log exceptions
```

## Data model

The demonstration input is one row per student and center snapshot with score, attendance rate and mentor score. Outputs preserve a student-level priority table and create a separate center-level summary.

## Controls

- Required-column and null validation
- Duplicate-key detection
- Valid-range checks
- Center-level record reconciliation
- Delivery log with success and failure status

## Validation

The pipeline stops on missing required columns, invalid score ranges or invalid attendance rates and writes an inspectable validation report before producing outputs.

## Implementation

- [Python pipeline](src/pipeline.py)
- [Validation guide](docs/validation.md)

Run against your own approved CSV:

```bash
python projects/03-reporting-automation/src/pipeline.py \
  projects/03-reporting-automation/examples/sample_input.csv outputs/
```

The input requires: `student_id, center_id, score, attendance_rate, mentor_score`.

## Evidence status

Portfolio reconstruction based on reporting-automation experience. No employer data or original automation script is included. The dashboard's report count, rule count and time-saving values are representative, not independently verified measurements.
