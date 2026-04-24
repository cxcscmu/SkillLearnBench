name: california-small-claims-sc100
description: Guidance on filling the California Small Claims Court form (SC-100). Use this skill when you need to accurately map case details to the fields of the SC-100 form.

# California Small Claims SC-100 Form Filling

This skill provides domain-specific knowledge for the SC-100 form (Plaintiff's Claim and ORDER to Go to Small Claims Court).

## Core Information Sections

1.  **Plaintiff Details**: Name, address, and contact info of the person suing.
2.  **Defendant Details**: Name, address, and contact info of the person being sued.
3.  **Claim Amount**: The specific dollar amount requested.
4.  **Reason for Claim**: A concise explanation of why the defendant owes the money.
5.  **Dates**: When the event occurred and the filing date.
6.  **Jurisdiction**: Why the case is being filed in this specific court (e.g., defendant lives there, event happened there).

## Mapping Case Details

| Form Field (Conceptual) | Case Description Key Info |
| :--- | :--- |
| Plaintiff Name | "I am [Name]" |
| Plaintiff Address | "I live in [Address]" |
| Defendant Name | "I want to sue [Name]" |
| Defendant Address | "[Name] in [Address]" |
| Claim Amount | "security deposit of amount $[Amount]" |
| Claim Reason | "failed to return... based on the signed... contract" |
| Dates of Event | "happened from [Start Date] until [End Date]" |
| Filing Date | "Please file it with date: [Date]" |

## Best Practices

*   **Brevity**: Keep reasons for claim concise but complete.
*   **Precision**: Ensure addresses and phone numbers are exact.
*   **Date Format**: Follow the user-specified date format (e.g., xxxx-xx-xx).
*   **Legal Consistency**: Use the terminology provided in the case description (e.g., "signed roommate sublease contract").
