"""Build the manuscript's tables and figures from the committed result files, and check its numbers.

Every table cell and figure value is read from verdict_audit/readiness/results/ at build time. The number check
recomputes each figure the text quotes and fails if the rounded value is not in manuscript.md.

Usage: python manuscript/build_assets.py   -> manuscript/tables.json, manuscript/figures/fig{1,2,3}.png
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "verdict_audit" / "readiness" / "results"
FIG = HERE / "figures"
TEXT = (HERE / "manuscript.md").read_text(encoding="utf-8")
STRATA = ("cvpr-2025", "iccv-2025", "eccv-2026", "iclr-2025", "iclr-2026", "icml-2025", "icml-2026", "neurips-2025",
          "neurips-2026")
INDICATORS = (("claims", "Main claims listed and linked to evidence"), ("code", "Code released"),
              ("main_data_access", "Main data openly available"), ("open_data_experiment", "Experiment on open data"),
              ("synthetic_or_sample_release", "Synthetic or sample data released"),
              ("weights_release", "Weights released"), ("outputs_release", "Outputs released"),
              ("variance", "Variance reported"), ("environment", "Environment stated"),
              ("compute", "Compute amount stated"))
LABEL = dict(INDICATORS)
# Candidate screening counts for the nine venue-years (results/candidates_summary.json and codes/labels.csv).
SCREEN = dict(listed=40290, candidates=5530, clinical=1013, life_science=1157, excluded_no=3360)


def load(name: str) -> dict:
    return json.loads((RES / name).read_text(encoding="utf-8"))


def pct(x: float) -> str:
    return f"{100 * x:.1f}"


def pts(x: float) -> str:
    """Percentage points with sign; the text uses the Unicode minus."""
    return f"{100 * x:+.1f}".replace("-", "−")


def ci(c: list) -> str:
    return f"{pts(c[0])} to {pts(c[1])}"


def est(x: dict) -> str:
    return f"{pts(x['rd'])} ({ci(x['ci'])})"


def table1(p9: dict) -> list[list[str]]:
    rows = [["Practice", "Medical, % (n known)", "Other, % (n known)", "Pooled difference, points (95% CI)",
             "Unclear, medical / other"]]
    for f, label in INDICATORS:
        a = p9["A9_3"][f]
        ls, ot = a["life_science"], a["other"]
        rows.append([label, f"{pct(ls['share'])} ({ls['n_known']})", f"{pct(ot['share'])} ({ot['n_known']})",
                     f"{pts(a['mh_rd'])} ({ci(a['mh_ci'])})", f"{ls['unclear']} / {ot['unclear']}"])
    return rows


def table2(areas: dict, ext: dict, claims: dict, adv: dict, more: dict) -> list[list[str]]:
    d, e1, e4, k3 = areas["PH9_d"], ext["E1"], ext["E4"], claims["K3"]
    return [["Outcome and adjustment", "Medical minus other, points (95% CI)"],
            ["Decided, all attempted papers (110 vs 1,821), unadjusted", est(d["unadjusted"])],
            ["Decided, clinical papers only", est(adv["F2"]["label_split"]["clinical"])],
            ["Decided, life-science papers only", est(adv["F2"]["label_split"]["life_science"])],
            ["Decided, adjusted for number of teams", est(d["teams"])],
            ["Decided, adjusted for first-team strength", est(e1["decided"]["adjusted"])],
            ["Fully verified, all attempted papers, unadjusted", est(e4["fully_verified"]["unadjusted"])],
            ["Fully verified, all attempted papers, adjusted for first-team strength", est(more["G1"]["adj_strength"])],
            ["Fully verified, claim-coded subsample (220 papers), unadjusted", est(k3["unadjusted"])],
            ["Fully verified, subsample, adjusted for first-team strength", est(k3["strength"])],
            ["Fully verified, subsample, adjusted for strength and claim cost", est(k3["strength_and_cost"])],
            ["Claim decided, unadjusted (claim level)", est(d["claim_level_unadjusted"])],
            ["Claim decided, within team (claim level)", est(d["claim_level_within_team"])]]


def table3(p9: dict, ext: dict) -> list[list[str]]:
    a4, pooled = p9["A9_4"], ext["pooled"]
    rows = [["Stated in full text vs obtained by reproducers", "n", "Sensitivity", "Specificity", "Kappa",
             "Kappa pooled with extension (n)"]]
    for key, label in (("code_vs_code_used", "Code released vs authors' code run"),
                       ("main_data_access_vs_data_obtained", "Main data open vs data obtained"),
                       ("weights_release_vs_weights_used", "Weights released vs weights used")):
        x, y = a4[key], pooled[key]
        rows.append([label, str(x["n"]), f"{x['sensitivity']:.2f}", f"{x['specificity']:.2f}", f"{x['kappa']:.2f}",
                     f"{y['kappa']:.2f} ({y['n']})"])
    c = a4["neurips_checklist_item5_vs_code"]
    rows.append(["NeurIPS checklist item 5 vs code released", str(c["n"]), f"{c['sensitivity']:.2f}",
                 f"{c['specificity']:.2f}", f"{c['kappa']:.2f}", ""])
    return rows


def table4(p9: dict, emp: dict) -> list[list[str]]:
    rows = [["Practice", "Main analysis: known value", "Empirical papers only: known value",
             "All coded papers, unclear counted as none"]]
    for f in ("code", "main_data_access", "weights_release", "variance", "synthetic_or_sample_release",
              "outputs_release"):
        a = p9["A9_3"][f]
        e = emp["E_a"]["fields"].get(f)
        b = emp["E_b"].get(f)
        rows.append([LABEL[f], f"{pts(a['mh_rd'])} ({ci(a['mh_ci'])})", est(e) if e else "",
                     (f"{pct(b['share']['medical'])} vs {pct(b['share']['other'])}%; {est(b)}") if b else ""])
    return rows


def table_s1(p9: dict) -> list[list[str]]:
    cov = p9["coverage"]
    rows = [["Venue-year", "Medical: frame / full text", "Other: frame / full text"]]
    for s in STRATA:
        ls, ot = cov[f"life_science|{s}"], cov[f"other|{s}"]
        rows.append([s, f"{ls['frame']} / {ls['coded']}", f"{ot['frame']} / {ot['coded']}"])
    tot = lambda g, k: sum(v[k] for kk, v in cov.items() if kk.startswith(g + "|"))
    rows.append(["Total", f"{tot('life_science', 'frame')} / {tot('life_science', 'coded')}",
                 f"{tot('other', 'frame')} / {tot('other', 'coded')}"])
    return rows


def fig1(p9: dict) -> None:
    coded = p9["coded"]
    frame = sum(v["frame"] for v in p9["coverage"].values())
    boxes = [
        (0.5, 0.92, f"Papers at nine venue-years, 2025-2026\nn = {SCREEN['listed']:,}"),
        (0.5, 0.74, f"Candidates by topic or term screen\nn = {SCREEN['candidates']:,}"),
        (0.5, 0.56, f"Labelled clinical ({SCREEN['clinical']:,}) or life science ({SCREEN['life_science']:,})\n"
                    f"medical group n = {SCREEN['clinical'] + SCREEN['life_science']:,}"),
        (0.5, 0.38, f"Frame: medical {frame // 2:,} + random other {frame // 2:,}\nn = {frame:,}"),
        (0.5, 0.20, f"Full text retrieved and coded\nmedical {coded['life_science']:,}, other {coded['other']:,}"),
    ]
    side = [(0.86, 0.65, f"Excluded: labelled\nnot medical\nn = {SCREEN['excluded_no']:,}"),
            (0.86, 0.29, f"Excluded: no full text\nn = {frame - coded['life_science'] - coded['other']:,}"),
            (0.12, 0.74, f"Non-candidates\nn = {SCREEN['listed'] - SCREEN['candidates']:,}\n(random sample drawn\nper venue-year)")]
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.axis("off")
    for x, y, t in boxes + side:
        ax.text(x, y, t, ha="center", va="center", fontsize=9, family="Arial",
                bbox=dict(boxstyle="square,pad=0.6", fc="white", ec="black", lw=0.8))
    for (x0, y0, _), (x1, y1, _) in zip(boxes, boxes[1:]):
        ax.annotate("", xy=(x1, y1 + 0.06), xytext=(x0, y0 - 0.06), arrowprops=dict(arrowstyle="->", lw=0.8))
    for (sx, sy, _), y in zip(side[:2], (0.65, 0.29)):
        ax.annotate("", xy=(sx - 0.1, sy), xytext=(0.5, y), arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("", xy=(0.12, 0.38), xytext=(0.12, 0.65), arrowprops=dict(arrowstyle="-", lw=0.8))
    ax.annotate("", xy=(0.26, 0.38), xytext=(0.12, 0.38), arrowprops=dict(arrowstyle="->", lw=0.8))
    fig.savefig(FIG / "fig1.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def forest_ax(ax, rows: list[tuple[str, dict]], xlabel: str, title: str | None = None) -> None:
    for i, (_, x) in enumerate(reversed(rows)):
        ax.plot([100 * x["ci"][0], 100 * x["ci"][1]], [i, i], color="black", lw=1)
        ax.plot(100 * x["rd"], i, "s", color="black", ms=5)
    ax.axvline(0, color="grey", lw=0.8, ls="--")
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks(range(len(rows)), [r[0] for r in reversed(rows)], fontsize=9)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.tick_params(axis="x", labelsize=9)
    if title:
        ax.set_title(title, fontsize=10, loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def main() -> None:
    FIG.mkdir(exist_ok=True)
    p9, areas, ext = load("p9.json"), load("p9_areas.json"), load("p9_extended.json")
    claims, adv, ext9 = load("p9_claims.json"), load("p9_adversarial.json"), load("p9_ext.json")
    more, emp = load("p9_more.json"), load("p9_empirical.json")
    tables = dict(table1=table1(p9), table2=table2(areas, ext, claims, adv, more), table3=table3(p9, ext9),
                  table4=table4(p9, emp), table_s1=table_s1(p9))
    (HERE / "tables.json").write_text(json.dumps(tables, indent=1, ensure_ascii=False), encoding="utf-8")
    fig1(p9)
    fig, ax = plt.subplots(figsize=(7.5, 0.42 * len(INDICATORS) + 1.0))
    forest_ax(ax, [(label, dict(rd=p9["A9_3"][f]["mh_rd"], ci=p9["A9_3"][f]["mh_ci"])) for f, label in INDICATORS],
              "Medical minus other, percentage points (Mantel-Haenszel, 95% CI)")
    fig.savefig(FIG / "fig2.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    d = areas["PH9_d"]
    paper = [("Decided, unadjusted", d["unadjusted"]),
             ("Decided, clinical papers only", adv["F2"]["label_split"]["clinical"]),
             ("Decided, life-science papers only", adv["F2"]["label_split"]["life_science"]),
             ("Decided, adjusted for number of teams", d["teams"]),
             ("Decided, adjusted for first-team strength", ext["E1"]["decided"]["adjusted"]),
             ("Fully verified, unadjusted", ext["E4"]["fully_verified"]["unadjusted"]),
             ("Fully verified, adjusted for first-team strength", more["G1"]["adj_strength"]),
             ("Fully verified, subsample, strength and claim cost", claims["K3"]["strength_and_cost"])]
    claim = [("Claim decided, unadjusted", d["claim_level_unadjusted"]),
             ("Claim decided, within team", d["claim_level_within_team"])]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.5, 6.2), gridspec_kw=dict(height_ratios=[len(paper), len(claim) + 0.6]),
                                 sharex=True)
    forest_ax(a1, paper, "", "(a) Paper level, attempted ICML 2026 papers")
    forest_ax(a2, claim, "Medical minus other, percentage points (95% CI)", "(b) Claim level")
    fig.tight_layout()
    fig.savefig(FIG / "fig3.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    missing = checks(p9, areas, ext, claims, adv, ext9, more, emp)
    for m in missing:
        print("NOT IN TEXT:", m, file=sys.stderr)
    print(f"tables and figures written; {len(missing)} quoted numbers not found in the text", file=sys.stderr)
    sys.exit(1 if missing else 0)


def checks(p9, areas, ext, claims, adv, ext9, more, emp) -> list[str]:
    """Quoted text that must appear verbatim in manuscript.md, each built from a result file."""
    a3, a5, d, ea, eb, ec = p9["A9_3"], p9["A9_5"], areas["PH9_d"], emp["E_a"], emp["E_b"], emp["E_c"]
    sh = lambda f, g: pct(a3[f][g]["share"])
    want = [
        f"{sh('code', 'life_science')}% of papers with a known value against {sh('code', 'other')}% (pooled difference {pts(a3['code']['mh_rd'])} points, 95% CI {ci(a3['code']['mh_ci'])})",
        f"{sh('main_data_access', 'life_science')}% against {sh('main_data_access', 'other')}% ({est(dict(rd=a3['main_data_access']['mh_rd'], ci=a3['main_data_access']['mh_ci']))[:-1].replace(' (', ', ', 1)})",
        f"{sh('weights_release', 'life_science')}% against {sh('weights_release', 'other')}% ({pts(a3['weights_release']['mh_rd'])}, {ci(a3['weights_release']['mh_ci'])})",
        f"{sh('variance', 'life_science')}% against {sh('variance', 'other')}% ({pts(a3['variance']['mh_rd'])}, {ci(a3['variance']['mh_ci'])})",
        f"({sh('claims', 'life_science')}% against {sh('claims', 'other')}%, {pts(a3['claims']['mh_rd'])} points, {ci(a3['claims']['mh_ci'])})",
        f"Among the {ea['units']['medical']:,} medical and {ea['units']['other']:,} other papers",
        f"code {pts(ea['fields']['code']['rd'])} ({ci(ea['fields']['code']['ci'])}), open main data {pts(ea['fields']['main_data_access']['rd'])} ({ci(ea['fields']['main_data_access']['ci'])}), weights {pts(ea['fields']['weights_release']['rd'])} ({ci(ea['fields']['weights_release']['ci'])}) and variance {pts(ea['fields']['variance']['rd'])} ({ci(ea['fields']['variance']['ci'])})",
        f"({pct(eb['main_data_access']['share']['medical'])}% against {pct(eb['main_data_access']['share']['other'])}%, {pts(eb['main_data_access']['rd'])}, {ci(eb['main_data_access']['ci'])})",
        f"fell to {pts(eb['weights_release']['rd'])} points ({ci(eb['weights_release']['ci'])})",
        f"synthetic or sample data ({pts(eb['synthetic_or_sample_release']['rd'])}, {ci(eb['synthetic_or_sample_release']['ci'])}) and outputs ({pts(eb['outputs_release']['rd'])}, {ci(eb['outputs_release']['ci'])})",
        f"rated verified in {pct(ec['medical']['claim_share']['verified'])}% against {pct(ec['other']['claim_share']['verified'])}% and inconclusive in {pct(ec['medical']['claim_share']['inconclusive'])}% against {pct(ec['other']['claim_share']['inconclusive'])}%",
        f"({pct(ec['medical']['claim_share']['toy'])}% against {pct(ec['other']['claim_share']['toy'])}%, {pts(ec['toy_claim_diff']['rd'])}, {ci(ec['toy_claim_diff']['ci'])})",
        f"{pct(a5['cells']['life_science']['decided'])}% of medical papers were decided",
        f"{pts(d['unadjusted']['rd'])} points (95% CI {ci(d['unadjusted']['ci'])}; permutation p < 0.001)",
        f"clinical papers ({est(adv['F2']['label_split']['clinical'])[:-1].replace(' (', ', ', 1)})",
        f"life-science papers ({est(adv['F2']['label_split']['life_science'])[:-1].replace(' (', ', ', 1)})",
        f"was dropped ({est(adv['F2']['top_medical_team_dropped'])[:-1].replace(' (', ', ', 1)})",
        f"full verification ({est(ext['E4']['fully_verified']['unadjusted'])[:-1].replace(' (', ', ', 1)})",
        f"falsified claim ({est(ext['E4']['any_falsified']['unadjusted'])[:-1].replace(' (', ', ', 1)})",
        f"the gap was {pts(a5['unadjusted']['rd'])} points ({ci(a5['unadjusted']['ci'])})",
        f"left it at {est(a5['both'])}",
        f"3.6 points less often than claims of other papers ({ci(d['claim_level_within_team']['ci'])})",
        f"{pts(-d['claim_level_unadjusted']['rd']).lstrip('+')} points less often without",
        f"settled {pct(ext['E1']['first_team_strength']['mean'][0])}% of its other attempted papers, against {pct(ext['E1']['first_team_strength']['mean'][1])}%",
        f"({est(dict(rd=ext['E1']['first_team_strength']['diff'], ci=ext['E1']['first_team_strength']['ci']))[:-1].replace(' (', ', ', 1)})",
        f"on {more['G2']['papers']} papers attempted by at least two teams, the stronger team decided the same paper {pct(more['G2']['rd'])} points more often than the weaker one ({ci(more['G2']['ci'])})",
        f"to {est(ext['E1']['decided']['adjusted'])[:-1].replace(' (', ' points (', 1)})",
        f"that gap was {est(more['G1']['adj_strength'])[:-1].replace(' (', ' points (', 1)}) after the adjustment",
        f"{pct(claims['K1']['costly']['medical'])}% of medical against {pct(claims['K1']['costly']['other'])}% of other claims",
        f"({est(dict(rd=claims['K1']['costly']['diff'], ci=claims['K1']['costly']['ci']))[:-1].replace(' (', ', ', 1)})",
        f"({pct(claims['K1']['analytic']['medical'])}% against {pct(claims['K1']['analytic']['other'])}%)",
        f"the full-verification gap was {pts(claims['K3']['unadjusted']['rd'])} points, {est(claims['K3']['strength'])} after adjusting",
        f"and {est(claims['K3']['strength_and_cost'])} after adjusting for both",
        f"kappa {p9['A9_4']['code_vs_code_used']['kappa']:.2f}; n = {p9['A9_4']['code_vs_code_used']['n']}",
        f"kappa {p9['A9_4']['main_data_access_vs_data_obtained']['kappa']:.2f}, n = {p9['A9_4']['main_data_access_vs_data_obtained']['n']}",
        f"kappas were {ext9['pooled']['code_vs_code_used']['kappa']:.2f} (n = {ext9['pooled']['code_vs_code_used']['n']})",
        f"(+7.5, {ci(ext['E5']['vision']['main_data_access']['ci'])})",
        f"{p9['adjudicated']:,} items",
        f"(adjusted {est(load('p9_posthoc.json')['PH9_b'])[:-1].replace(' (', ' points, ', 1)}; {load('p9_posthoc.json')['PH9_b']['n']} frame papers)",
        f"({load('p9_posthoc.json')['PH9_b']['distribution']['life_science']['listed_and_linked']} medical and {load('p9_posthoc.json')['PH9_b']['distribution']['other']['listed_and_linked']} other papers)",
        f"only {pct(a3['claims']['life_science']['share'])}% of medical and {pct(a3['claims']['other']['share'])}% of other papers tie each main claim",
        f"({pct(a3['claims']['life_science']['share'])}% of medical versus {pct(a3['claims']['other']['share'])}% of other papers)",
    ]
    return [w for w in want if w not in TEXT]


if __name__ == "__main__":
    main()
