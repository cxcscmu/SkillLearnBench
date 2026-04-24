---
name: json-data-parsing
description: How to read and extract specific values from employee_data.json to map them to template placeholders.
---

### Extracting Data
To process the offer letter, first read the `employee_data.json` file. Use a JSON parser to load the data into a dictionary or object. 

1. **Load File:** Use `json.load()` (Python) or equivalent to convert the file content.
2. **Access Values:** Retrieve specific keys (e.g., `candidate_name`, `position`, `relocation_package`) which will be injected into the template.
3. **Verification:** Ensure all mandatory fields exist in the JSON object before attempting to fill the template to avoid runtime errors.