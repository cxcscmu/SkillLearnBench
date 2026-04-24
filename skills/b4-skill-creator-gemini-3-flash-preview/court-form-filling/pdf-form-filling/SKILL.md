name: pdf-form-filling
description: How to programmatically fill PDF forms with fillable fields. Use this skill whenever you need to fill a PDF that has fillable form fields (checkboxes, text fields, etc.).

# PDF Form Filling Skill

This skill provides a structured workflow for filling PDF forms that contain fillable fields.

## Workflow

1.  **Extract Field Information**:
    Use the `extract_form_field_info.py` script to get a JSON representation of all fillable fields in the PDF.
    ```bash
    python3 /root/.agents/skills/pdf/scripts/extract_form_field_info.py <input.pdf> <field_info.json>
    ```

2.  **Analyze Fields (Optional but Recommended)**:
    Convert the PDF to images to visually map field IDs to the form's labels if the field IDs are not descriptive.
    ```bash
    python3 /root/.agents/skills/pdf/scripts/convert_pdf_to_images.py <input.pdf> <output_directory>
    ```

3.  **Prepare Field Values**:
    Create a `field_values.json` file containing the values for each field you want to fill.
    Format:
    ```json
    [
      {
        "field_id": "field_name",
        "description": "Short description",
        "page": 1,
        "value": "Value to fill"
      }
    ]
    ```
    *   **Checkboxes**: Use the `checked_value` (often `/Yes` or `/On`) or `unchecked_value` (often `/Off`).
    *   **Radio Groups**: Use the specific `value` from `radio_options`.
    *   **Text Fields**: Provide the string to be entered.

4.  **Fill the Form**:
    Run the `fill_fillable_fields.py` script to generate the filled PDF.
    ```bash
    python3 /root/.agents/skills/pdf/scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>
    ```

## Field Value Mapping Table

| Type | How to fill |
| :--- | :--- |
| text | Direct string value |
| checkbox | Use `checked_value` from info |
| radio_group | Use one of the `radio_options` values |
| choice | Use one of the `choice_options` values |
