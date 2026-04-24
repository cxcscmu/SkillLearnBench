---
name: run2_python-docx
description: Advanced Word document manipulation using raw XML regex replacements to perfectly preserve formatting across split text runs.
---

# Advanced DOCX Templating via Direct XML

While the `python-docx` library is excellent for creating and reading Word documents, it struggles with replacing text placeholders (e.g., `{{PLACEHOLDER}}`) that have been split across multiple Run (`<w:r>`) elements due to formatting or spellcheck artifacts in Word.

## The Problem
When a user types `{{COMPANY_NAME}}`, Word often saves it internally as:
```xml
<w:r><w:t>{{COMP</w:t></w:r><w:r><w:rPr><w:b/></w:rPr><w:t>ANY_NAME}}</w:t></w:r>
```
If you use `python-docx` to read `.text` from the paragraph, you get the full string, but replacing it and assigning back to `paragraph.text` destroys all the `<w:rPr>` (run formatting) properties in that paragraph. 

## The Solution: Regex over XML
By treating the `.docx` as a ZIP file, we can read the `word/document.xml`, `word/header1.xml`, etc., and apply regular expressions that ignore the XML tags interleaved between our placeholder characters.

### 1. Building the Regex
To match a placeholder like `{{VAR}}` regardless of how many tags interrupt it:
```python
import re

def build_regex(var_name):
    # Matches {{var_name}} allowing any <tag> sequences between characters
    pattern = r'\{' + r'(?:<[^>]+>)*' + r'\{' + r'(?:<[^>]+>)*'
    for char in var_name:
        pattern += re.escape(char) + r'(?:<[^>]+>)*'
    pattern += r'\}' + r'(?:<[^>]+>)*' + r'\}'
    return pattern
```

### 2. Safely Replacing Matches
When we find a match, we clear the text content inside the matched block (to remove the old placeholder text) but preserve ALL the XML tags. We then inject the replacement string into the first text node (`<w:t>`). This preserves formatting properties perfectly.

```python
def replace_match(m, replacement=''):
    matched_text = m.group(0)
    # Split text and tags
    parts = re.split(r'(<[^>]+>)', matched_text)
    
    # Clear all actual text fragments
    for i in range(len(parts)):
        if not parts[i].startswith('<'):
            parts[i] = ''
            
    res = ''.join(parts)
    # Inject replacement text just before the first closing text tag (or at start if none)
    if replacement:
        if '</w:t>' in res:
            res = res.replace('</w:t>', replacement + '</w:t>', 1)
        else:
            res = replacement + res
    return res
```

### 3. Handling Conditional Blocks
If you have a conditional block like `{{IF_RELOCATION}}...{{END_IF_RELOCATION}}`:
- **If True:** Find and replace `{{IF_RELOCATION}}` and `{{END_IF_RELOCATION}}` with an empty string using the above method. This removes the markers but keeps the content.
- **If False:** Build a regex that spans from the start marker to the end marker using `.*?` with `re.DOTALL`, and replace the *entire match* with an empty string using `replace_match(m, '')`. This safely empties the text between the markers, leaving the XML structure intact (creating an empty paragraph or section).

```python
# To remove a block completely
block_regex = build_regex('IF_RELOCATION') + r'.*?' + build_regex('END_IF_RELOCATION')
xml_content = re.sub(block_regex, lambda m: replace_match(m, ''), xml_content, flags=re.DOTALL)
```

### 4. Updating the DOCX File
Use `zipfile` to read the template, process `.xml` files, and write to a new `.docx`.

```python
import zipfile

def process_docx(input_path, output_path, variables):
    with zipfile.ZipFile(input_path, 'r') as zin:
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                # Apply replacements to body, headers, and footers
                if item.filename.endswith('.xml') and ('word/document' in item.filename or 'word/header' in item.filename or 'word/footer' in item.filename):
                    content_str = content.decode('utf-8')
                    # Apply your re.sub logic here...
                    content = content_str.encode('utf-8')
                zout.writestr(item, content)
```
This is the most reliable way to maintain corporate branding, strict formatting, and complex tables in templated Word documents!
