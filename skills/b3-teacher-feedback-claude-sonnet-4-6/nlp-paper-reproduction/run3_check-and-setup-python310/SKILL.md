---
name: check-and-setup-python310
description: Use this skill when you need to find, install, or configure a Python 3.10 environment on the system. Checks for existing python3.10 binary, installs if missing, and sets up pip for that version.
---

## Check and Setup Python 3.10

### Step 1: Check if Python 3.10 already exists

```bash
ls /usr/bin/python3.10 2>/dev/null && echo "FOUND at /usr/bin/python3.10" || echo "NOT FOUND"
which python3.10 2>/dev/null || echo "python3.10 not in PATH"
python3.10 --version 2>/dev/null || echo "python3.10 not executable"
```

### Step 2: If not found, install Python 3.10 via deadsnakes PPA or uv

```bash
# Option A: via uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
uv python install 3.10

# Option B: via apt (Ubuntu/Debian)
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install -y python3.10 python3.10-venv python3.10-distutils
```

### Step 3: Ensure pip is available for python3.10

```bash
python3.10 -m ensurepip --upgrade 2>/dev/null || \
  curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
python3.10 -m pip --version
```

### Step 4: Verify

```bash
python3.10 -VV
```