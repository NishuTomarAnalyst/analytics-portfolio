# Validation

- Confirm NPS scores are integers from 0 through 10.
- Deduplicate repeat submissions according to the agreed survey rule.
- Reconcile call attempts with source-system totals by date.
- Compare event-level counts with distinct-customer counts.
- Test dealers with no responses and protect every denominator with `NULLIF`.
- Confirm dealer-to-region mapping is one-to-one for each effective period.
- Treat recommendations and outcome movement as association unless an experiment establishes causality.
