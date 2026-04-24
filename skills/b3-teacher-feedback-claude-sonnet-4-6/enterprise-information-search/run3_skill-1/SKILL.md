[SKILL]
---
name: enterprise-data-retrieval
description: Use this skill to retrieve information from enterprise data files located at /root/DATA and answer questions from /root/question.txt, writing results to /root/answer.json. Handles nested structures, multi-file traversal, and product-scoped filtering.
---

# Enterprise Data Retrieval Skill

## Overview
This skill reads questions from `/root/question.txt`, searches enterprise data files under `/root/DATA/` in a targeted, hierarchical manner, and writes answers to `/root/answer.json`.

## Step-by-Step Process

### Step 1: Read Questions
```python
import json, os, re

with open('/root/question.txt', 'r') as f:
    content = f.read()

# Parse questions - handle both JSON and key: value formats
try:
    questions = json.loads(content)
except:
    questions = {}
    for line in content.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            questions[k.strip()] = v.strip()
```

### Step 2: Explore Data Directory Structure
```python
import subprocess

# Get full directory tree first
result = subprocess.run(['find', '/root/DATA', '-type', 'f'], 
                       capture_output=True, text=True)
all_files = result.stdout.strip().split('\n')

# Also get directory structure
dir_result = subprocess.run(['find', '/root/DATA', '-type', 'd'],
                            capture_output=True, text=True)
all_dirs = dir_result.stdout.strip().split('\n')

print("Files found:", len(all_files))
print("Sample files:", all_files[:20])
print("Directories:", all_dirs)
```

### Step 3: Load Data Hierarchically (Per File, No Truncation)
```python
def load_file(filepath):
    """Load a single file fully without truncation."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        if filepath.endswith('.json'):
            try:
                return json.loads(content), content
            except:
                return None, content
        return None, content
    except Exception as e:
        return None, f"ERROR: {e}"

def load_all_files():
    """Load all files, keeping filepath as context key."""
    data_by_file = {}
    for fp in all_files:
        if fp.strip():
            parsed, raw = load_file(fp.strip())
            data_by_file[fp.strip()] = {
                'parsed': parsed,
                'raw': raw,
                'path': fp.strip()
            }
    return data_by_file

all_data = load_all_files()
```

### Step 4: Product-Scoped File Selection
```python
def get_product_files(product_name, all_files):
    """Find files likely belonging to a specific product using 2+ signals."""
    product_lower = product_name.lower()
    # Normalize: remove spaces, hyphens for fuzzy match
    product_slug = re.sub(r'[\s\-_]+', '', product_lower)
    
    matched = []
    for fp in all_files:
        fp_lower = fp.lower()
        fp_slug = re.sub(r'[\s\-_]+', '', fp_lower)
        
        signals = 0
        # Signal 1: product name in directory path
        if product_lower in fp_lower or product_slug in fp_slug:
            signals += 1
        # Signal 2: parent directory matches product
        parts = fp_lower.split('/')
        for part in parts:
            if product_lower in part or product_slug in re.sub(r'[\s\-_]+','',part):
                signals += 1
                break
        
        if signals >= 1:
            matched.append(fp)
    
    return matched

def get_relevant_files_for_question(question_text, all_files, all_data):
    """Identify files most relevant to answering a question."""
    q_lower = question_text.lower()
    
    # Extract potential product names from question
    # Look for capitalized phrases or quoted names
    product_candidates = re.findall(r'"([^"]+)"', question_text)
    product_candidates += re.findall(r"'([^']+)'", question_text)
    # Also try capitalized words
    caps = re.findall(r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b', question_text)
    product_candidates += caps
    
    relevant_files = set()
    
    # Always include files that match product names found in question
    for pc in product_candidates:
        matched = get_product_files(pc, all_files)
        relevant_files.update(matched)
    
    # Add files whose content contains keywords from question
    keywords = [w for w in q_lower.split() if len(w) > 4 and w not in 
                ('what', 'which', 'where', 'there', 'their', 'about', 'with', 'from', 'that', 'this', 'have', 'were')]
    
    for fp, fdata in all_data.items():
        raw_lower = fdata['raw'].lower()
        matches = sum(1 for kw in keywords if kw in raw_lower)
        if matches >= 2:
            relevant_files.add(fp)
    
    return list(relevant_files) if relevant_files else all_files
```

### Step 5: Reviewer Extraction (Strict, No Participant Fallback)
```python
def extract_reviewers_strict(record, filepath=''):
    """
    Extract reviewers from explicit reviewer fields only.
    NO participant fallback — only use evidence-backed reviewer signals.
    """
    reviewers = set()
    
    REVIEWER_FIELDS = [
        'reviewers', 'reviewer', 'reviewed_by', 'approvers', 'approver',
        'approved_by', 'feedback_by', 'reviewed_by', 'review_comments',
        'pr_reviewers', 'code_reviewers', 'document_reviewers',
        'requested_reviewers', 'review_requested_from'
    ]
    
    def extract_names_from_value(val):
        names = set()
        if isinstance(val, str) and val.strip():
            names.add(val.strip())
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, str) and item.strip():
                    names.add(item.strip())
                elif isinstance(item, dict):
                    # Extract name fields from reviewer objects
                    for nk in ('name', 'username', 'user', 'login', 'display_name', 'full_name', 'email'):
                        if nk in item and item[nk]:
                            names.add(str(item[nk]).strip())
                            break
        elif isinstance(val, dict):
            for nk in ('name', 'username', 'user', 'login', 'display_name'):
                if nk in val and val[nk]:
                    names.add(str(val[nk]).strip())
                    break
        return names
    
    def traverse(obj, depth=0):
        if depth > 10:
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                k_lower = k.lower().replace('-', '_').replace(' ', '_')
                if any(rf == k_lower or k_lower.endswith('_' + rf) or k_lower.startswith(rf + '_') 
                       for rf in REVIEWER_FIELDS):
                    reviewers.update(extract_names_from_value(v))
                # Also check for feedback/review in nested structures
                elif k_lower in ('feedback', 'review', 'comments', 'approval'):
                    if isinstance(v, dict):
                        for subk, subv in v.items():
                            subk_lower = subk.lower().replace('-','_').replace(' ','_')
                            if any(rf in subk_lower for rf in ('reviewer','approver','by','from','author')):
                                reviewers.update(extract_names_from_value(subv))
                    traverse(v, depth+1)
                elif k_lower in ('messages', 'threads', 'transcript', 'entries', 'comments'):
                    # In Slack threads / meeting transcripts, look for review-signaling messages
                    traverse_transcript_for_reviewers(v)
                else:
                    traverse(v, depth+1)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item, depth+1)
    
    def traverse_transcript_for_reviewers(obj):
        """Extract reviewers from message/transcript structures based on content signals."""
        REVIEW_SIGNAL_PHRASES = [
            'reviewed', 'approved', 'lgtm', 'looks good', 'my review',
            'review complete', 'i reviewed', 'feedback on', 'my feedback',
            'reviewed by', 'approve', 'requesting review'
        ]
        
        entries = obj if isinstance(obj, list) else [obj]
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            
            # Get message text
            text = ''
            for tk in ('text', 'message', 'content', 'body'):
                if tk in entry and isinstance(entry[tk], str):
                    text = entry[tk].lower()
                    break
            
            # Check if message indicates a review action
            is_review = any(phrase in text for phrase in REVIEW_SIGNAL_PHRASES)
            
            if is_review:
                # Extract the author/sender of this review message
                for ak in ('author', 'sender', 'user', 'from', 'name', 'username', 'speaker'):
                    if ak in entry and entry[ak]:
                        val = entry[ak]
                        if isinstance(val, str):
                            reviewers.add(val.strip())
                        elif isinstance(val, dict):
                            for nk in ('name', 'username', 'display_name', 'full_name'):
                                if nk in val and val[nk]:
                                    reviewers.add(str(val[nk]).strip())
                                    break
                        break
            
            # Recurse into nested messages
            for nk in ('replies', 'thread', 'messages', 'comments'):
                if nk in entry:
                    traverse_transcript_for_reviewers(entry[nk])
    
    if isinstance(record, dict):
        traverse(record)
    elif isinstance(record, list):
        for item in record:
            traverse(item)
    
    return list(reviewers)
```

### Step 6: Multi-Hop Artifact Resolution
```python
def resolve_linked_artifacts(record, all_data, visited=None):
    """
    Follow IDs/references in a record to linked artifacts (PRs, meetings, Slack threads).
    Returns all linked records found.
    """
    if visited is None:
        visited = set()
    
    linked = []
    
    LINK_FIELDS = [
        'pr_id', 'pull_request_id', 'meeting_id', 'slack_channel', 'thread_id',
        'document_id', 'doc_id', 'artifact_id', 'review_id', 'pr_url', 'pr_link',
        'related_prs', 'related_meetings', 'related_docs', 'references', 'links'
    ]
    
    def find_ids(obj, depth=0):
        if depth > 5:
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                k_lower = k.lower().replace('-','_').replace(' ','_')
                if any(lf in k_lower for lf in LINK_FIELDS):
                    ids_to_check = []
                    if isinstance(v, str):
                        ids_to_check = [v]
                    elif isinstance(v, list):
                        ids_to_check = [str(x) for x in v if x]
                    
                    for ref_id in ids_to_check:
                        if ref_id and ref_id not in visited:
                            visited.add(ref_id)
                            # Search all files for this ID
                            for fp, fdata in all_data.items():
                                if ref_id.lower() in fdata['raw'].lower():
                                    if fdata['parsed']:
                                        linked.append({
                                            'source_file': fp,
                                            'data': fdata['parsed'],
                                            'matched_id': ref_id
                                        })
                else:
                    find_ids(v, depth+1)
        elif isinstance(obj, list):
            for item in obj:
                find_ids(item, depth+1)
    
    find_ids(record)
    return linked
```

### Step 7: Answer Each Question
```python
def build_context_for_question(question_text, all_data, all_files):
    """Build targeted context for a specific question."""
    relevant_files = get_relevant_files_for_question(question_text, all_files, all_data)
    
    context_parts = []
    for fp in relevant_files:
        if fp in all_data:
            fdata = all_data[fp]
            # Include full raw content per file — no truncation
            context_parts.append(f"=== FILE: {fp} ===\n{fdata['raw']}\n")
    
    return '\n'.join(context_parts), relevant_files


def answer_questions_with_llm(questions, all_data, all_files):
    """Answer each question using targeted file loading and LLM."""
    from openai import OpenAI
    client = OpenAI()
    
    answers = {}
    
    for q_key, q_text in questions.items():
        print(f"\nAnswering {q_key}: {q_text}")
        
        # Build targeted context
        context, used_files = build_context_for_question(q_text, all_data, all_files)
        print(f"  Using {len(used_files)} files for context")
        
        # If context is very large, split into chunks and do multi-turn
        MAX_CONTEXT = 400000  # characters — much larger than before
        
        if len(context) <= MAX_CONTEXT:
            # Single call
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """You are an enterprise data analyst. 
Extract precise answers from the provided data.

CRITICAL RULES:
- For reviewer questions: ONLY count people in explicit reviewer/approver fields OR people whose messages clearly indicate they performed a review (said 'LGTM', 'approved', 'I reviewed', etc.)
- Do NOT include general participants or meeting attendees as reviewers unless they explicitly reviewed
- If multiple products exist, only return data for the specific product mentioned in the question
- Confirm artifact belongs to the target product via path, title, or channel name before extracting
- Return answers as a JSON object with key "answer" containing a list of strings
- If a single answer, still return as list of length 1
- Be thorough — check all provided files"""},
                    {"role": "user", "content": f"Question: {q_text}\n\nData:\n{context}"}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            try:
                result = json.loads(result_text)
                answer_list = result.get('answer', result.get('answers', []))
                if isinstance(answer_list, str):
                    answer_list = [answer_list]
                elif not isinstance(answer_list, list):
                    answer_list = [str(answer_list)]
            except:
                answer_list = [result_text.strip()]
            
        else:
            # Context too large: chunk and aggregate
            chunks = [context[i:i+MAX