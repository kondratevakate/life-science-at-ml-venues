"""Protocol 9, Note 9-28 (post hoc, descriptive): what the adjudicated full-text disagreements were about.

For every adjudicated variance and compute disagreement, the two coder labels are paired. A pair of the field's
"not reported" label (variance `no`, compute `none`) with `unclear` is a disagreement about a paper that does not
state the practice ("silence"); every other pair concerns content. Reports the label pairs, the share of silence
pairs, how the adjudicator resolved them by group, and the reference-standard disagreements by field.

Usage: python posthoc_p9_adjudication_types.py   -> results/p9_adj_types.json
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODES = HERE / "codes" / "p9"
OUT = HERE / "results" / "p9_adj_types.json"
SILENT = {"variance": "no", "compute": "none"}


def load(pattern: str) -> dict:
    rows = {}
    for path in sorted(CODES.glob(pattern)):
        with path.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                rows[r["item_id"]] = r
    return rows


def main() -> None:
    coder1 = load("p9_coder1_batch_*.csv")
    coder2 = load("p9_coder2_batch_*.csv")
    coder2.update(load("p9_coder2full_batch_*.csv"))
    with (HERE / "results" / "p9_papers.csv").open(encoding="utf-8") as fh:
        group = {r["item"]: r["group"] for r in csv.DictReader(fh)}
    with (CODES / "adjudication.csv").open(encoding="utf-8") as fh:
        adjudicated = list(csv.DictReader(fh))

    out = {"note": "9-28", "post_hoc": True, "fields": {}}
    for field, silent in SILENT.items():
        rows = [r for r in adjudicated if r["field"] == field]
        pairs, resolved, silence_n = Counter(), Counter(), Counter()
        for r in rows:
            a, b = coder1[r["item_id"]][field], coder2[r["item_id"]][field]
            pairs[" vs ".join(sorted((a, b)))] += 1
            if {a, b} == {silent, "unclear"}:
                g = group[r["item_id"]]
                silence_n[g] += 1
                resolved[g] += r["label"] == silent
        n_silence = sum(silence_n.values())
        out["fields"][field] = {
            "n": len(rows),
            "label_pairs": dict(pairs.most_common()),
            "silence_pairs": n_silence,
            "content_pairs": len(rows) - n_silence,
            "silence_resolved_not_reported": {
                "all": [sum(resolved.values()), n_silence],
                **{g: [resolved[g], silence_n[g]] for g in sorted(silence_n)},
            },
        }
    out["reference_standard"] = dict(Counter(r["field"] for r in adjudicated if r["field"] not in SILENT))
    out["total_adjudicated"] = len(adjudicated)
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
