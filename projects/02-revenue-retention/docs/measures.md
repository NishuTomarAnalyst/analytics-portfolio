# Power BI measures

```DAX
Recognized Revenue :=
CALCULATE(
    SUM(Enrollment[Fee Amount]),
    Enrollment[Status] IN {"Active", "Completed"}
)

Active Students :=
CALCULATE(
    DISTINCTCOUNT(Enrollment[Student ID]),
    Enrollment[Status] = "Active"
)

Retention Rate :=
DIVIDE([Active Students], [Starting Cohort Students])

Batch Utilization :=
DIVIDE([Active Students], SUM(Batch[Operational Capacity]))
```

The starting cohort must be fixed by enrollment period. It should not change when new students join later, and operational capacity must follow an approved effective-date rule.
