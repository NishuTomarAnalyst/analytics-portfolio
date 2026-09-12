# Validation and cost controls

- Use dry runs and record estimated bytes before execution.
- Compare source and target counts by partition date.
- Test uniqueness at the declared target grain.
- Confirm query plans apply partition pruning.
- Measure runtime across repeated runs; do not compare one warm run with one cold run.
- Store query job IDs, bytes billed and dates before publishing performance claims.
- Use least-privilege service accounts and never commit credentials.
