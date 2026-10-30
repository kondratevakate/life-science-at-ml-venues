"""Link the downloaded inputs into the paths the frozen scripts expect.

The analysis scripts were frozen in kondratevakate/icml-2026-repro and read their inputs from fixed relative paths.
Rather than edit them (their SHA-256 is recorded in the result manifests), this script links those paths to the
downloaded datasets under DATA_ROOT. Nothing is copied and nothing is downloaded.

  verdict_audit/readiness/data              -> DATA_ROOT/datasets/literature/ml-venue-listings/2024-2026-v1/raw
  data/verdicts_confirmation_2026-10-17     -> DATA_ROOT/datasets/literature/icml2026-challenge-snapshots/2026-10-27/raw/verdicts

The full texts (ml-venue-fulltext/2025-2026-v1) are read through DATA_ROOT directly by fetch_p9.py.

Usage: python setup_data.py [--data-root PATH]   (default: $DATA_ROOT, else C:\\Projects\\data)
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINKS = {
    HERE / "verdict_audit" / "readiness" / "data": Path("datasets/literature/ml-venue-listings/2024-2026-v1/raw"),
    HERE / "data" / "verdicts_confirmation_2026-10-17":
        Path("datasets/literature/icml2026-challenge-snapshots/2026-10-27/raw/verdicts"),
}
# The verdict snapshot every analysis pins (p8_common.VERDICTS_SHA).
CHECK = (Path("datasets/literature/icml2026-challenge-snapshots/2026-10-27/raw/verdicts/verdicts.json"),
         "652f1c162462d7ad142ff32e2bd13d5853e21c639681ef416971776fdd33c526")


def link(dst: Path, src: Path) -> None:
    if dst.exists() or dst.is_symlink():
        if dst.resolve() == src.resolve():
            print(f"ok      {dst.relative_to(HERE)}")
            return
        raise SystemExit(f"{dst} exists and points elsewhere; remove it first")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":  # a junction needs no admin rights, unlike a symlink
        subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(src)], check=True, capture_output=True)
    else:
        dst.symlink_to(src, target_is_directory=True)
    print(f"linked  {dst.relative_to(HERE)} -> {src}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=os.environ.get("DATA_ROOT", r"C:\Projects\data"))
    root = Path(ap.parse_args().data_root)
    missing = [str(root / s) for s in LINKS.values() if not (root / s).is_dir()]
    if missing:
        raise SystemExit("missing input folders (see README, Data):\n  " + "\n  ".join(missing))
    got = hashlib.sha256((root / CHECK[0]).read_bytes()).hexdigest()
    if got != CHECK[1]:
        raise SystemExit(f"verdict snapshot hash mismatch: {got}")
    for dst, src in LINKS.items():
        link(dst, root / src)


if __name__ == "__main__":
    sys.exit(main())
