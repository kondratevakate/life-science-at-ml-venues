"""Protocol 9, Note 9-36: API-equivalent token cost of the coding subagents, from Claude Code session logs.

Assigns each subagent log to a coding task by the sheet path in its first user message and sums token usage per
model (one count per message id). Prices: Claude API list prices read on 2026-11-25. Cache writes as a range
(5-minute rate lower, 1-hour rate upper). Prints aggregates only, never message content.

Usage: python cost_accounting.py   -> results/p9_costs.json
"""
from __future__ import annotations

import glob
import json
import os
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "p9_costs.json"
LOGS = os.path.expanduser("~/.claude/projects")
# USD per million tokens: input, cache write 5m, cache write 1h, cache read, output
PRICES = {
    "claude-sonnet-5-5": (2.0, 2.5, 4.0, 0.10, 10.0),
    "claude-opus-5-5": (4.0, 5.0, 8.0, 0.20, 20.0),
    "claude-opus-5": (5.0, 6.25, 10.0, 0.50, 25.0),
}
PRICES_SOURCE = "platform.claude.com/docs/en/about-claude/pricing, read 2026-11-25"
TASKS = [  # (task, pattern in the first user message, note, coded units, unit)
    ("p9_coder1", r"p9_coder1_batch_", "9-5", 3278, "paper"),
    ("p9_coder2full", r"p9_coder2full_batch_", "9-6", None, "paper"),
    ("p9_coder2", r"p9_coder2_batch_", "9-5", 813, "paper"),
    ("p9_adjudication", r"p9_adj_batch_", "9-6/9-7", None, "disagreement"),
    ("p9_ref", r"p9_ref[12]_batch_", "9-7", 222, "logbook paper"),
    ("p9_claims", r"p9_claim[12]_batch_", "9-15", None, "claim"),
    ("p9_ext", r"p9_(ext[12]|refx[12])_batch_", "9-17", 300, "paper"),
    ("p9_ext_adj", r"ext_adj_sheets", "9-20", 302, "disagreement"),
]


def first_user_text(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh):
            if i > 30:
                break
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = r.get("message") or {}
            if r.get("type") == "user" or m.get("role") == "user":
                c = m.get("content")
                if isinstance(c, list):
                    c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
                return str(c or "")
    return ""


def scan() -> dict:
    tot = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    files, dates = defaultdict(int), defaultdict(set)
    for path in sorted(glob.glob(os.path.join(LOGS, "**", "*.jsonl"), recursive=True)):
        p = path.replace("\\", "/")
        if "/subagents/" not in p and not os.path.basename(p).startswith("agent-"):
            continue
        text = first_user_text(path)
        task = next((t for t, pat, *_ in TASKS if re.search(pat, text)), None)
        if not task:
            continue
        files[task] += 1
        seen = set()
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                m = r.get("message") or {}
                u = m.get("usage")
                if not u or m.get("role") != "assistant" or m.get("id") in seen:
                    continue
                seen.add(m.get("id"))
                d = tot[task][m.get("model", "?")]
                for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"):
                    d[k] += int(u.get(k) or 0)
                d["messages"] += 1
                if r.get("timestamp"):
                    dates[task].add(r["timestamp"][:10])
    return dict(tot=tot, files=files, dates=dates)


def cost(model: str, d: dict) -> tuple[float, float] | None:
    if model not in PRICES:
        return None
    pi, cw5, cw1, cr, po = PRICES[model]
    base = (d["input_tokens"] * pi + d["cache_read_input_tokens"] * cr + d["output_tokens"] * po) / 1e6
    return base + d["cache_creation_input_tokens"] * cw5 / 1e6, base + d["cache_creation_input_tokens"] * cw1 / 1e6


def main() -> dict:
    s = scan()
    res = dict(note="9-36", prices_source=PRICES_SOURCE, prices_usd_per_mtok=PRICES, basis="API-equivalent", tasks={})
    lo_all = hi_all = 0.0
    for task, _, note, units, unit in TASKS:
        models = {m: dict(v) for m, v in s["tot"].get(task, {}).items() if m in PRICES}
        lo = sum(cost(m, d)[0] for m, d in models.items())
        hi = sum(cost(m, d)[1] for m, d in models.items())
        lo_all, hi_all = lo_all + lo, hi_all + hi
        res["tasks"][task] = dict(note=note, subagents=s["files"].get(task, 0),
                                  dates=sorted(s["dates"][task])[::max(1, len(s["dates"][task]) - 1)] if s["dates"][task] else [],
                                  models=models, cost_usd=[round(lo, 2), round(hi, 2)], units=units, unit=unit,
                                  cost_per_unit_usd=[round(lo / units, 4), round(hi / units, 4)] if units else None)
    res["total_cost_usd"] = [round(lo_all, 2), round(hi_all, 2)]
    res["gaps"] = ("Not found in local logs: topic coding (9-24), axes coding (9-26), the 9-25 recovery coders and "
                   "adjudicators, the claim adjudication (9-15), and every orchestrating main thread.")
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = main()
    for t, v in r["tasks"].items():
        print(t, v["subagents"], v["cost_usd"], v["cost_per_unit_usd"])
    print("total", r["total_cost_usd"])
