#!/usr/bin/env python3
from pathlib import Path

import numpy as np


def main() -> None:
    npz_path = Path(__file__).resolve().parent / "loss.npz"
    data = np.load(npz_path, allow_pickle=True)

    print(f"File: {npz_path}")
    print(f"Keys: {list(data.files)}")
    print("-" * 60)

    for key in data.files:
        value = data[key]
        print(f"[{key}]")
        print(f"type={type(value)}, dtype={value.dtype}, shape={value.shape}")
        print(value)
        print("-" * 60)


if __name__ == "__main__":
    main()
