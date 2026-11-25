"""Protocol 9, Note 9-30 (post hoc): reliability of agentic verdicts across teams (RQ1).

Units (Notes 9-29, 9-34): attempted ICML 2026 papers (protocol 8 snapshot of 2026-10-17, author's namespace excluded,
candidates labelled `no` excluded) with at least two distinct teams; a team's verdict = its latest logbook.
R1a paper-level discordance and Krippendorff's alpha (nominal) for decided; R1b claim-level alpha on anchored claims;
R1c crossed random-effects logistic model (paper, team) variance shares; R1d attempts needed (Spearman-Brown and
majority-of-k agreement on papers with at least six teams). By group with bootstrap over papers within group.

Usage: python posthoc_p9_reliability.py   -> results/p9_reliability.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p8_common as P8  # noqa: E402
from posthoc_p9_adversarial import icml_units  # noqa: E402
from posthoc_p9_areas import LIFE  # noqa: E402

SEED, B = 20261124, 2000
OUT = HERE / "results" / "p9_reliability.json"
ANCHORED = Path(r"C:\Projects\data\datasets\literature\icml2026-challenge-snapshots\2026-10-27\raw\live\claims_anchored.json")
CLAIM_CATS = ("verified", "falsified", "toy", "inconclusive")
TARGET = 0.80


def alpha_nominal(units: list[list]) -> float | None:
    """Krippendorff's alpha, nominal, for units with variable numbers of values (units with < 2 values ignored)."""
    coinc = Counter()
    for vals in units:
        m = len(vals)
        if m < 2:
            continue
        cnt = Counter(vals)
        for a in cnt:
            for b in cnt:
                coinc[(a, b)] += cnt[a] * (cnt[b] - (a == b)) / (m - 1)
    n = sum(coinc.values())
    if n == 0:
        return None
    cats = sorted({a for a, _ in coinc})
    marg = {c: sum(v for (a, _), v in coinc.items() if a == c) for c in cats}
    do = sum(v for (a, b), v in coinc.items() if a != b) / n
    de = sum(marg[a] * marg[b] for a in cats for b in cats if a != b) / (n * (n - 1))
    return None if de == 0 else 1 - do / de


def load():
    lab = icml_units()
    cv = P8.claim_verdicts()
    anchored_raw = json.loads(ANCHORED.read_text(encoding="utf-8-sig"))
    anchored = {o: {P8.A.norm(c["text"]) for c in v} for o, v in anchored_raw.items()}
    papers, unmatched, matched = [], 0, 0
    for o in sorted(cv):
        if o not in lab:
            continue
        by_team = defaultdict(list)
        for c in cv[o]:
            by_team[P8.A.namespace(c["space"])].append(c)
        # teams with a logbook but no claims are absent from cv rows; they count as not decided
        teams = sorted(by_team)
        dec = {t: int(any(c["verdict"] in P8.DECISIVE for c in by_team[t])) for t in teams}
        claims = defaultdict(list)
        anc = anchored.get(o, set())
        for t in teams:
            for c in by_team[t]:
                if c["verdict"] not in CLAIM_CATS:
                    continue
                if c["text"] in anc:
                    claims[c["text"]].append(c["verdict"])
                    matched += 1
                else:
                    unmatched += 1
        papers.append(dict(orid=o, med=lab[o] in LIFE, dec=dec, claims=dict(claims)))
    return papers, dict(claim_rows_matched=matched, claim_rows_unmatched_excluded=unmatched)


def paper_alpha(ps):
    return alpha_nominal([list(p["dec"].values()) for p in ps])


def claim_alpha(ps):
    return alpha_nominal([v for p in ps for v in p["claims"].values()])


def boot(ps, stat, rng):
    groups = [sorted((p for p in ps if p["med"] == m), key=lambda p: p["orid"]) for m in (True, False)]
    vals = []
    for _ in range(B):
        s = [g[i] for g in groups for i in rng.integers(0, len(g), len(g))]
        v = stat(s)
        if v is not None:
            vals.append(v)
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def boot_diff(ps, stat, rng):
    med = sorted((p for p in ps if p["med"]), key=lambda p: p["orid"])
    oth = sorted((p for p in ps if not p["med"]), key=lambda p: p["orid"])
    vals = []
    for _ in range(B):
        a = stat([med[i] for i in rng.integers(0, len(med), len(med))])
        b = stat([oth[i] for i in rng.integers(0, len(oth), len(oth))])
        if a is not None and b is not None:
            vals.append(a - b)
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def k_needed(r1):
    if r1 is None or r1 <= 0:
        return None
    return TARGET * (1 - r1) / (r1 * (1 - TARGET))


def majority(vals, rng):
    s = sum(vals)
    if 2 * s == len(vals):
        return int(rng.integers(0, 2))
    return int(2 * s > len(vals))


def majority_k(ps, rng):
    out = {}
    six = [p for p in ps if len(p["dec"]) >= 6]
    for k in range(1, 6):
        agree = []
        for p in six:
            vals = list(p["dec"].values())
            for _ in range(200):
                idx = rng.permutation(len(vals))
                a = majority([vals[i] for i in idx[:k]], rng)
                b = majority([vals[i] for i in idx[k:]], rng)
                agree.append(a == b)
        out[k] = float(np.mean(agree)) if agree else None
    return dict(papers=len(six), agreement_by_k=out)


def mixed_model(ps):
    import pandas as pd
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

    rows = sorted((dict(y=d, paper=p["orid"], team=t) for p in ps for t, d in p["dec"].items()),
                  key=lambda r: (r["paper"], r["team"]))
    df = pd.DataFrame(rows)
    model = BinomialBayesMixedGLM.from_formula("y ~ 1", {"paper": "0 + C(paper)", "team": "0 + C(team)"}, df)
    fit = model.fit_vb()
    sd = np.exp(fit.vcp_mean)  # posterior means of log SDs -> SDs (order: paper, team)
    v_paper, v_team = float(sd[0] ** 2), float(sd[1] ** 2)
    resid = np.pi ** 2 / 3
    tot = v_paper + v_team + resid
    r6 = lambda x: round(float(x), 6)  # variational fit differs in the 8th decimal across processes
    return dict(rows=len(df), var_paper=r6(v_paper), var_team=r6(v_team), var_residual_latent=r6(resid),
                share_paper=r6(v_paper / tot), share_team=r6(v_team / tot),
                method="statsmodels BinomialBayesMixedGLM fit_vb; values rounded to 6 decimals")


def summary(ps, rng):
    pa, ca = paper_alpha(ps), claim_alpha(ps)
    return dict(papers=len(ps),
                discordant_share=float(np.mean([len(set(p["dec"].values())) > 1 for p in ps])),
                paper_alpha=pa, claim_alpha=ca,
                claim_units=sum(1 for p in ps for v in p["claims"].values() if len(v) >= 2),
                k_for_reliability_080=k_needed(pa))


def main() -> dict:
    papers, claim_counts = load()
    multi = [p for p in papers if len(p["dec"]) >= 2]
    rng = np.random.default_rng(SEED)
    res = dict(note="9-30", post_hoc=True, attempted_papers=len(papers), units_two_or_more_teams=len(multi),
               teams_per_paper=dict(sorted(Counter(min(len(p["dec"]), 6) for p in papers).items())),
               claims=claim_counts)
    res["all"] = summary(multi, rng)
    res["all"]["paper_alpha_ci"] = boot(multi, paper_alpha, rng)
    res["all"]["claim_alpha_ci"] = boot(multi, claim_alpha, rng)
    for g, m in (("medical", True), ("other", False)):
        sel = [p for p in multi if p["med"] == m]
        res[g] = summary(sel, rng)
    res["diff_paper_alpha_medical_minus_other"] = dict(
        estimate=res["medical"]["paper_alpha"] - res["other"]["paper_alpha"], ci=boot_diff(multi, paper_alpha, rng))
    res["diff_claim_alpha_medical_minus_other"] = dict(
        estimate=res["medical"]["claim_alpha"] - res["other"]["claim_alpha"], ci=boot_diff(multi, claim_alpha, rng))
    res["R1c_mixed"] = mixed_model(multi)
    res["R1d_majority_of_k"] = majority_k(multi, rng)
    res["reading"] = dict(
        one_verdict_not_enough=res["all"]["paper_alpha_ci"][1] < 0.667,
        medical_differs=not (res["diff_paper_alpha_medical_minus_other"]["ci"][0] <= 0
                             <= res["diff_paper_alpha_medical_minus_other"]["ci"][1]))
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: r[k] for k in ("units_two_or_more_teams", "all", "medical", "other",
                                        "diff_paper_alpha_medical_minus_other", "R1c_mixed", "R1d_majority_of_k",
                                        "reading")}, indent=1))
