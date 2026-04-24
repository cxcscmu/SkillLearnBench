---
name: run-simpo-with-python310-and-log
description: Use this skill to execute the SimPO unit test with Python 3.10, save the loss results to /root/loss.npz, and log Python version and package info to /root/python_info.txt using the correct Python 3.10 executable.
---

## Run SimPO Unit Test with Python 3.10 and Log Environment

### Step 1: Confirm Python 3.10 executable path

```bash
PYTHON310=$(which python3.10 2>/dev/null || echo "/usr/bin/python3.10")
echo "Using Python: $PYTHON310"
$PYTHON310 --version
```

### Step 2: Log Python version and packages to /root/python_info.txt

```bash
PYTHON310=$(which python3.10 2>/dev/null || echo "/usr/bin/python3.10")

# Overwrite python_info.txt with python3.10 info
$PYTHON310 -VV > /root/python_info.txt 2>&1
echo "---" >> /root/python_info.txt
$PYTHON310 -m pip freeze >> /root/python_info.txt 2>&1

echo "Logged to /root/python_info.txt"
cat /root/python_info.txt | head -5
```

### Step 3: Run the unit test with Python 3.10

```bash
PYTHON310=$(which python3.10 2>/dev/null || echo "/usr/bin/python3.10")
cd /root/SimPO
$PYTHON310 /root/SimPO/unit_test/unit_test_1.py
```

### Step 4: Verify the output file

```bash
PYTHON310=$(which python3.10 2>/dev/null || echo "/usr/bin/python3.10")
$PYTHON310 -c "
import numpy as np
data = np.load('/root/loss.npz')
print('Keys:', list(data.keys()))
print('Losses:', data['losses'])
"
```

### Important Notes
- Always use `python3.10` (or the resolved path) — never use `python` or `python3` which may resolve to 3.12
- The `python -VV` and `pip freeze` in `python_info.txt` must come from the 3.10 binary
- If `python3.10 -m pip` fails, first run: `python3.10 -m ensurepip --upgrade`