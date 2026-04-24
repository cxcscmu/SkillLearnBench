---
name: Format and Write CSV with Proper Escaping
description: Write CSV output with correct field quoting and escaping for special characters, using standard CSV formatting.
---

## CSV Writing Process

1. **Use Python csv module correctly**
   ```
   Use csv.DictWriter with:
   - fieldnames in exact order: 
     ['Package', 'Version', 'CVE_ID', 'Severity', 'CVSS_Score', 'Fixed_Version', 'Title', 'Url']
   - quoting=csv.QUOTE_MINIMAL (or QUOTE_ALL if safety needed)
   - Allow csv module to handle special characters
   ```

2. **Field preparation before writing**
   - Ensure all fields are strings
   - Do NOT manually quote fields
   - Let csv.DictWriter handle escaping

3. **Handle special characters**
   - Commas in Title/Url: csv module auto-escapes
   - Newlines in Title: csv module auto-escapes
   - Quotes in fields: csv module auto-escapes with doubling

4. **File write settings**
   - Open file in text mode: `open(..., 'w', newline='')`
   - Use UTF-8 encoding if needed
   - Flush and close properly

5. **Validation**
   - Manually verify CSV can be parsed
   - Check row count matches expected
   - Verify no truncated fields