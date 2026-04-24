---
name: pypdf-form-filling
description: Inspecting and filling interactive PDF forms (AcroForms) using the pypdf library. Crucial for automating the population of government or legal PDF documents.
---

# Filling PDF Forms with `pypdf`

When automating the filling of PDF forms (like court documents), you must first discover the internal field names embedded in the PDF, and then map your data to those fields using the `pypdf` library. 

## Step 1: Inspect the Form Fields

PDF form fields rarely match their visual labels exactly. They often have internal names like `form1[0].#subform[0].TextField1[0]`. **Always inspect the PDF first** to get the exact field names and types.

Write and run a script like this to discover the fields:

```python
from pypdf import PdfReader

reader = PdfReader("path/to/blank.pdf")
fields = reader.get_fields()

if fields:
    for field_name, field_data in fields.items():
        # /FT indicates Field Type (e.g., /Tx for Text, /Btn for Button/Checkbox)
        field_type = field_data.get('/FT')
        print(f"Field Name: {field_name}")
        print(f"Type: {field_type}")
        print("-" * 30)
else:
    print("No interactive form fields found.")
```

*Note: For complex forms with hundreds of fields, it's often best to save this output to a text file and grep/search through it to find the relevant fields.*

## Step 2: Fill the Form and Save

Once you have identified the correct field names, use `PdfWriter` to update the form field values. 

```python
from pypdf import PdfReader, PdfWriter
from pypdf.generic import BooleanObject, NameObject

# 1. Read the blank PDF
reader = PdfReader("path/to/blank.pdf")
writer = PdfWriter()

# 2. Append all pages to the writer
writer.append(reader)

# 3. Define the data mapping
# Use the exact field names discovered in Step 1.
# Checkboxes typically take '/Yes', '/On', or the specific export value defined in the PDF.
form_data = {
    "Internal_Text_Field_Name": "Jane Doe",
    "Internal_Date_Field": "2026-01-19",
    "Internal_Checkbox_Field": "/Yes"
}

# 4. Update the values on all pages
for page in writer.pages:
    writer.update_page_form_field_values(page, form_data)

# 5. Force PDF viewers to render the new text 
# (Highly recommended for court forms so the text actually appears when printed)
if "/AcroForm" in writer.root_object:
    writer.root_object["/AcroForm"][NameObject("/NeedAppearances")] = BooleanObject(True)

# 6. Save the filled PDF
with open("path/to/filled.pdf", "wb") as output_stream:
    writer.write(output_stream)
```

## Best Practices
1. **Iterative Mapping:** Map only the required fields. Leave optional/unmentioned fields out of your `form_data` dictionary.
2. **Date Formats:** Always respect the specific date format requested by the prompt (e.g., `xxxx-xx-xx`).
3. **Checkbox Values:** If `/Yes` doesn't check a box, you may need to inspect the `/Opt` or `/V` arrays in the field data during Step 1 to find the exact string the PDF expects (e.g., `/1`, `/Choice1`).