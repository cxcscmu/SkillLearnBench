---
name: data_format_validation
description: Ensures the generated output strictly adheres to the required JSON schema.
---
Before finalizing the task, write the results to `/root/answers.json`. Verify the structure matches:
```json
{
    "q1_answer": number,
    "q2_answer": number,
    "q3_answer": ["stock_cusip1", "stock_cusip2", "stock_cusip3", "stock_cusip4", "stock_cusip5"],
    "q4_answer": ["fund1", "fund2", "fund3"]
}
```
Ensure all monetary figures are represented as integers or floats consistent with the validated units (e.g., if the raw data is in thousands, the final `q1_answer` must be multiplied by 1,000).