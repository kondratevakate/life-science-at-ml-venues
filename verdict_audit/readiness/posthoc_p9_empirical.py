"""Protocol 9, Note 9-22 (post hoc): empirical-only documentation, release fields with unclear as no, verdict mix.

E-a MH difference over venue-years among papers with a stated data scale; E-b release fields with `unclear` counted
as not released; E-c claim-level and paper-level verdict mix of attempted ICML 2026 papers by group.

Usage: python posthoc_p9_empirical.py   -> results/p9_empirical.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p8_common as P8  # noqa: E402
from analyze_p8 import wilson  # noqa: E402
from analyze_p9 import INDICATOR, boot_ci, final_codes, mh_rd  # noqa: E402
from build_p9_sheets import KEYS  # noqa: E402
from posthoc_p9_areas import LIFE, boot_papers  # noqa: E402

PRIMARY = ("code", "main_data_access", "weights_release", "variance")
RELEASE = ("main_data_access", "weights_release", "synthetic_or_sample_release", "outputs_release")
VERDICTS = ("verified", "falsified", "toy", "inconclusive", "other")


def papers() -> list[dict]:
    keys = json.loads(KEYS.read_text(encoding="utf-8"))
    final = final_codes()
    return [dict(stratum=keys[i]["stratum"], ls=keys[i]["group"] == "life_science", **final[i]) for i in sorted(final)]


def contrast(sel: list[dict], field: str, unclear_as_no: bool = False) -> dict:
    pos = INDICATOR[field]
    use = sel if unclear_as_no else [p for p in sel if p[field] != "unclear"]
    rows = [(p["stratum"], p["ls"], int(p[field] == pos)) for p in use]
    share = {g: sum(r[2] for r in rows if r[1] == ls) / max(1, sum(r[1] == ls for r in rows))
             for g, ls in (("medical", True), ("other", False))}
    return dict(n=len(rows), n_medical=sum(r[1] for r in rows), share=share, rd=mh_rd(rows), ci=boot_ci(rows, mh_rd))


def verdict_mix() -> dict:
    units = [u for u in json.loads((P8.DATA / "papers.json").read_text(encoding="utf-8")) if u["stratum"] == "icml-2026"]
    labels = {}
    import csv
    with (HERE / "codes" / "labels.csv").open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["kind"] == "cand" and r["unit"].startswith("icml-2026:"):
                labels[r["unit"].split(":", 1)[1]] = r["label"]
    cv = P8.claim_verdicts()
    att = []
    for u in units:
        o = u["forum_id"]
        if u["candidate"] and labels.get(o) not in LIFE:
            continue
        if o in cv:
            att.append(dict(orid=o, med=labels.get(o) in LIFE, verdicts=[c["verdict"] for c in cv[o]]))
    out = {}
    for g, med in (("medical", True), ("other", False)):
        sel = [p for p in att if p["med"] == med]
        c = Counter(v for p in sel for v in p["verdicts"])
        n = sum(c.values())
        out[g] = dict(papers=len(sel), claim_rows=n,
                      claim_share={v: c[v] / n for v in VERDICTS},
                      claim_wilson={v: wilson(c[v], n) for v in VERDICTS},
                      any_toy=sum("toy" in p["verdicts"] for p in sel) / len(sel))

    def toy_claim_diff(s):
        share = []
        for med in (True, False):
            v = [x for p in s if p["med"] == med for x in p["verdicts"]]
            if not v:
                return None
            share.append(sum(x == "toy" for x in v) / len(v))
        return share[0] - share[1]

    def any_toy_diff(s):
        a = [("toy" in p["verdicts"]) for p in s if p["med"]]
        b = [("toy" in p["verdicts"]) for p in s if not p["med"]]
        return sum(a) / len(a) - sum(b) / len(b) if a and b else None

    out["toy_claim_diff"] = dict(rd=toy_claim_diff(att), ci=boot_papers(att, toy_claim_diff))
    out["any_toy_diff"] = dict(rd=any_toy_diff(att), ci=boot_papers(att, any_toy_diff))
    return out


def main() -> dict:
    ps = papers()
    emp = [p for p in ps if p["data_scale"] != "not_stated"]
    res = dict(
        E_a=dict(units=dict(medical=sum(p["ls"] for p in emp), other=sum(not p["ls"] for p in emp)),
                 fields={f: contrast(emp, f) for f in PRIMARY}),
        E_b={f: contrast(ps, f, unclear_as_no=True) for f in RELEASE},
        E_c=verdict_mix())
    res["E_a"]["holds"] = {f: bool(v["ci"] and v["ci"][0] > 0) for f, v in res["E_a"]["fields"].items()}
    (HERE / "results" / "p9_empirical.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    print(json.dumps(main(), indent=1)[:3000])
