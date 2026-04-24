---
name: enterprise-data-retrieval
description: Core skill for retrieving information from enterprise data files (JSON, JSONL, CSV, Parquet, Markdown, etc.) located at /root/DATA, answering questions from /root/question.txt, and writing structured answers to /root/answer.json. Handles multi-hop reasoning, cross-referencing, and entity resolution across enterprise documents.
---

# Enterprise Data Retrieval Skill

## Overview
This skill retrieves answers from enterprise data stored at `/root/DATA` by reading questions from `/root/question.txt`, performing deep multi-hop searches across all data sources, and writing results to `/root/answer.json`.

## Step 1: Explore the Data Directory

```python
import os

def walk_data_dir(root="/root/DATA"):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            full = os.path.join(dirpath, f)
            all_files.append(full)
            print(full, os.path.getsize(full))
    return all_files

all_files = walk_data_dir()
```

Catalog every file. Note file types: `.json`, `.jsonl`, `.csv`, `.parquet`, `.md`, `.txt`, `.yaml`, `.log`.

## Step 2: Load and Index ALL Data

Load every file into memory with appropriate parsers:

```python
import json, csv, pathlib

def load_file(path):
    ext = pathlib.Path(path).suffix.lower()
    with open(path, 'r', errors='replace') as f:
        text = f.read()
    if ext == '.json':
        return json.loads(text), text
    elif ext == '.jsonl':
        records = [json.loads(line) for line in text.strip().split('\n') if line.strip()]
        return records, text
    elif ext == '.csv':
        import io
        reader = csv.DictReader(io.StringIO(text))
        return list(reader), text
    elif ext == '.parquet':
        import pandas as pd
        df = pd.read_parquet(path)
        return df.to_dict('records'), df.to_string()
    else:
        return text, text
    
all_data = {}
all_raw_text = {}
for fpath in all_files:
    try:
        parsed, raw = load_file(fpath)
        all_data[fpath] = parsed
        all_raw_text[fpath] = raw
    except Exception as e:
        print(f"Error loading {fpath}: {e}")
```

**Print a summary of each file** (first 2000 chars) to understand the schema and content. Identify:
- Slack messages/threads (channels, replies, timestamps, users)
- Meeting transcripts (speakers, turns, timestamps)
- Documents / PRs / reports (title, author, reviewers, content, metadata)
- User directories / org charts (name, role, team, product)
- Product catalogs / project metadata

## Step 3: Build Cross-Reference Index

Create lookup structures to enable multi-hop traversal:

```python
# Index by entity ID, document ID, user name, channel, etc.
entity_index = {}  # entity_id -> all records mentioning it
user_index = {}    # user_name -> all records involving them
doc_index = {}     # doc_id/title -> all records referencing it
product_index = {} # product_name -> all associated artifacts

def index_record(record, source_file):
    """Index a record by all identifiable keys."""
    if isinstance(record, dict):
        for key, val in record.items():
            if isinstance(val, str):
                # Index by meaningful identifiers
                pass  # implement per schema
    # Also do full-text indexing for cross-references
```

## Step 4: Read Questions

```python
with open('/root/question.txt', 'r') as f:
    question_text = f.read()
print(question_text)
```

Parse all questions. Typically formatted as key-value pairs like:
```
q1: What are ...?
q2: Who ...?
```

```python
import re
questions = {}
for line in question_text.strip().split('\n'):
    line = line.strip()
    if not line:
        continue
    match = re.match(r'(q\d+)\s*[:：]\s*(.*)', line, re.IGNORECASE)
    if match:
        questions[match.group(1)] = match.group(2)
    # Also handle JSON format
if not questions:
    try:
        questions = json.loads(question_text)
    except:
        pass
print(questions)
```

## Step 5: Answer Each Question with Deep Multi-Hop Search

For each question, follow this rigorous procedure:

### 5a: Identify Question Type
- **"Who reviewed/contributed to X?"** → Reviewer/contributor identification (see Skill: reviewer-extraction)
- **"Which documents/artifacts relate to product Y?"** → Product-artifact association (see Skill: product-artifact-grounding)
- **"What is the status/value of Z?"** → Direct field lookup
- **"List all X that satisfy condition Y"** → Filtered enumeration

### 5b: Keyword and Semantic Search

```python
def search_all(query_terms, data=all_raw_text):
    """Search across all raw text for query terms."""
    results = []
    for fpath, text in data.items():
        text_lower = text.lower()
        score = sum(1 for term in query_terms if term.lower() in text_lower)
        if score > 0:
            results.append((fpath, score, text))
    results.sort(key=lambda x: -x[1])
    return results
```

### 5c: Multi-Hop Follow-Through (CRITICAL)

When a search finds a reference, **always follow cross-references**:

1. **Document → Slack threads**: If a document is shared in Slack, find ALL replies in that thread
2. **Slack thread → Meeting transcripts**: If a meeting is mentioned, find the transcript and scan ALL speaker turns
3. **Meeting transcript → Documents**: If a document is discussed, trace back to the document record
4. **PR/Review → Comments**: If a PR is found, find ALL comments and review submissions
5. **Any reference to a person → Verify their role** via user directory

```python
def follow_references(initial_results, all_data):
    """
    Given initial search results, follow cross-references to find
    all connected information across data sources.
    """
    visited = set()
    queue = list(initial_results)
    all_connected = []
    
    while queue:
        item = queue.pop(0)
        item_id = id(item)  # or a content hash
        if item_id in visited:
            continue
        visited.add(item_id)
        all_connected.append(item)
        
        # Extract cross-references (doc IDs, thread IDs, meeting IDs, usernames)
        refs = extract_references(item)
        for ref in refs:
            # Search for the referenced entity in all data
            matches = lookup_reference(ref, all_data)
            queue.extend(matches)
    
    return all_connected
```

### 5d: Assemble Answer

Collect all evidence, deduplicate, and format as a list.

## Step 6: Track Token Consumption

**CRITICAL**: Track actual token usage, NOT placeholders.

```python
import tiktoken

# If using OpenAI-style API, track from response objects:
# tokens_used = response.usage.total_tokens

# If counting manually:
def count_tokens(text, model="gpt-4"):
    try:
        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(text))
    except:
        # Fallback: approximate 1 token ≈ 4 chars
        return max(1, len(text) // 4)

# Track per-question token usage
question_tokens = {}
```

For each question, measure tokens consumed by:
- The question text itself
- All data chunks read/searched for that question
- The generated answer

Sum these and store as a **positive integer** (never zero, never a string).

If exact API token counts are available from LLM calls, use those. Otherwise, estimate based on text processed. **The value must be a positive number.**

```python
# Example tracking pattern:
for qid, question in questions.items():
    tokens_for_this_q = 0
    tokens_for_this_q += count_tokens(question)
    
    # ... perform searches, each time adding tokens for text processed ...
    for chunk in relevant_chunks:
        tokens_for_this_q += count_tokens(chunk)
    
    tokens_for_this_q += count_tokens(str(answer))
    
    # Ensure positive
    question_tokens[qid] = max(1, tokens_for_this_q)
```

## Step 7: Recall-Check Before Finalizing (CRITICAL)

**Before writing the final answer**, perform a completeness verification:

```python
def recall_check(qid, question, current_answer, all_data):
    """
    Re-scan ALL relevant sources to ensure no entity was missed.
    Specifically:
    - Re-scan all Slack thread replies for substantive contributors
    - Re-scan all meeting transcript turns for feedback/suggestions
    - Re-scan all PR/review comments
    - Verify no cross-product distractors slipped in
    """
    missed = []
    # ... implementation per question type ...
    return missed

for qid in questions:
    missed = recall_check(qid, questions[qid], answers[qid], all_data)
    if missed:
        answers[qid].extend(missed)
```

## Step 8: Write Output

```python
output = {}
for qid in questions:
    ans = answers[qid]
    # Ensure answer is always a list
    if not isinstance(ans, list):
        ans = [ans]
    # Ensure tokens is a positive number
    tok = question_tokens.get(qid, 1)
    if not isinstance(tok, (int, float)) or tok <= 0:
        tok = 1
    output[qid] = {"answer": ans, "tokens": tok}

with open('/root/answer.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# Verify
with open('/root/answer.json', 'r') as f:
    print(f.read())
```

## Output Format
```json
{
    "q1": {"answer": ["item1", "item2"], "tokens": 1542},
    "q2": {"answer": ["item1"], "tokens": 987},
    "q3": {"answer": ["item1", "item2", "item3"], "tokens": 2103}
}
```