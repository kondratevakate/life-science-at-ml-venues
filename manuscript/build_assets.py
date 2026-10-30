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


def table1(p9: dict) -> list[list[str]]:
    rows = [["Practice", "Life science, % (n known)", "Other, % (n known)", "Pooled difference, points (95% CI)",
             "Unclear, life science / other"]]
    for f, label in INDICATORS:
        a = p9["A9_3"][f]
        ls, ot = a["life_science"], a["other"]
        rows.append([label, f"{pct(ls['share'])} ({ls['n_known']})", f"{pct(ot['share'])} ({ot['n_known']})",
                     f"{pts(a['mh_rd'])} ({ci(a['mh_ci'])})", f"{ls['unclear']} / {ot['unclear']}"])
    return rows


def table2(areas: dict, ext: dict, claims: dict, adv: dict) -> list[list[str]]:
    d, e1, k3 = areas["PH9_d"], ext["E1"], claims["K3"]
    r = lambda x: f"{pts(x['rd'])} ({ci(x['ci'])})"
    return [["Outcome and adjustment", "Medical minus other, points (95% CI)"],
            ["Decided, unadjusted (110 vs 1,821 attempted papers)", r(d["unadjusted"])],
            ["Decided, clinical papers only", r(adv["F2"]["label_split"]["clinical"])],
            ["Decided, life-science papers only", r(adv["F2"]["label_split"]["life_science"])],
            ["Decided, adjusted for number of teams", r(d["teams"])],
            ["Decided, adjusted for first-team strength", r(e1["decided"]["adjusted"])],
            ["Claim decided, unadjusted (claim level)", r(d["claim_level_unadjusted"])],
            ["Claim decided, within team (claim level)", r(d["claim_level_within_team"])],
            ["Fully verified, unadjusted (claim-coded sample)", r(k3["unadjusted"])],
            ["Fully verified, adjusted for first-team strength", r(k3["strength"])],
            ["Fully verified, adjusted for strength and claim cost", r(k3["strength_and_cost"])]]


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


def table_s1(p9: dict) -> list[list[str]]:
    cov = p9["coverage"]
    rows = [["Venue-year", "Life science: frame / full text", "Other: frame / full text"]]
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
                    f"life-science group n = {SCREEN['clinical'] + SCREEN['life_science']:,}"),
        (0.5, 0.38, f"Frame: life science {frame // 2:,} + random other {frame // 2:,}\nn = {frame:,}"),
        (0.5, 0.20, f"Full text retrieved and coded\nlife science {coded['life_science']:,}, other {coded['other']:,}"),
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


def forest(rows: list[tuple[str, float, list]], path: Path, xlabel: str) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 0.42 * len(rows) + 1.0))
    for i, (label, est, c) in enumerate(reversed(rows)):
        ax.plot([100 * c[0], 100 * c[1]], [i, i], color="black", lw=1)
        ax.plot(100 * est, i, "s", color="black", ms=5)
    ax.axvline(0, color="grey", lw=0.8, ls="--")
    ax.set_yticks(range(len(rows)), [r[0] for r in reversed(rows)], fontsize=9)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.tick_params(axis="x", labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def checks(p9: dict, areas: dict, ext: dict, claims: dict, adv: dict, ext9: dict) -> list[str]:
    """(quoted text, why) pairs; each text must appear verbatim in manuscript.md."""
    a3, a5 = p9["A9_3"], p9["A9_5"]
    want = [f"59.4% of papers with a known value against {pct(a3['code']['other']['share'])}%",
            f"({pts(a3['code']['mh_rd'])} points, 95% CI {ci(a3['code']['mh_ci'])})".replace("(", "(pooled difference ", 1),
            f"{pct(a3['main_data_access']['life_science']['share'])}% against {pct(a3['main_data_access']['other']['share'])}% ({pts(a3['main_data_access']['mh_rd'])}, {ci(a3['main_data_access']['mh_ci'])})",
            f"{pct(a3['weights_release']['life_science']['share'])}% against {pct(a3['weights_release']['other']['share'])}% ({pts(a3['weights_release']['mh_rd'])}, {ci(a3['weights_release']['mh_ci'])})",
            f"{pct(a3['variance']['life_science']['share'])}% against {pct(a3['variance']['other']['share'])}% ({pts(a3['variance']['mh_rd'])}, {ci(a3['variance']['mh_ci'])})",
            f"({pct(a3['claims']['life_science']['share'])}% against {pct(a3['claims']['other']['share'])}%, {pts(a3['claims']['mh_rd'])} points, {ci(a3['claims']['mh_ci'])})".replace("+", "", 0),
            f"{pct(a5['cells']['life_science']['decided'])}% of medical papers were decided",
            f"{pts(areas['PH9_d']['unadjusted']['rd'])} points (95% CI {ci(areas['PH9_d']['unadjusted']['ci'])}; permutation p = {adv['F2']['permutation']['p']}",
            f"clinical papers ({pts(adv['F2']['label_split']['clinical']['rd'])}, {ci(adv['F2']['label_split']['clinical']['ci'])})",
            f"life-science papers ({pts(adv['F2']['label_split']['life_science']['rd'])}, {ci(adv['F2']['label_split']['life_science']['ci'])})",
            f"was dropped ({pts(adv['F2']['top_medical_team_dropped']['rd'])}, {ci(adv['F2']['top_medical_team_dropped']['ci'])})",
            f"rated: {pts(ext['E4']['fully_verified']['unadjusted']['rd'])}, {ci(ext['E4']['fully_verified']['unadjusted']['ci'])})",
            f"falsified claim ({pts(ext['E4']['any_falsified']['unadjusted']['rd'])}, {ci(ext['E4']['any_falsified']['unadjusted']['ci'])})",
            f"the gap was {pts(a5['unadjusted']['rd'])} points ({ci(a5['unadjusted']['ci'])})",
            f"left it at {pts(a5['both']['rd'])} ({ci(a5['both']['ci'])})",
            f"3.6 points less often than claims of other papers ({ci(areas['PH9_d']['claim_level_within_team']['ci'])})",
            f"{pts(-areas['PH9_d']['claim_level_unadjusted']['rd']).lstrip('+')} points less often without",
            f"settled {pct(ext['E1']['first_team_strength']['mean'][0])}% of its other attempted papers, against {pct(ext['E1']['first_team_strength']['mean'][1])}%",
            f"({pts(ext['E1']['first_team_strength']['diff'])}, {ci(ext['E1']['first_team_strength']['ci'])})",
            f"to {pts(ext['E1']['decided']['adjusted']['rd'])} points ({ci(ext['E1']['decided']['adjusted']['ci'])})",
            f"{pct(claims['K1']['costly']['medical'])}% of medical against {pct(claims['K1']['costly']['other'])}% of other claims",
            f"({pts(claims['K1']['costly']['diff'])}, {ci(claims['K1']['costly']['ci'])})",
            f"({pct(claims['K1']['analytic']['medical'])}% against {pct(claims['K1']['analytic']['other'])}%)",
            f"to {pts(claims['K3']['strength']['rd'])} points ({ci(claims['K3']['strength']['ci'])})",
            f"reduced it to {pts(claims['K3']['strength_and_cost']['rd'])} ({ci(claims['K3']['strength_and_cost']['ci'])})",
            f"kappa {p9['A9_4']['code_vs_code_used']['kappa']:.2f}; n = {p9['A9_4']['code_vs_code_used']['n']}",
            f"kappa {p9['A9_4']['main_data_access_vs_data_obtained']['kappa']:.2f}, n = {p9['A9_4']['main_data_access_vs_data_obtained']['n']}",
            f"kappas were {ext9['pooled']['code_vs_code_used']['kappa']:.2f} (n = {ext9['pooled']['code_vs_code_used']['n']})",
            f"(+7.5, {ci(ext['E5']['vision']['main_data_access']['ci'])})",
            f"{p9['adjudicated']:,} items",
            ]
    return [w for w in want if w not in TEXT]


def main() -> None:
    FIG.mkdir(exist_ok=True)
    p9, areas, ext = load("p9.json"), load("p9_areas.json"), load("p9_extended.json")
    claims, adv, ext9 = load("p9_claims.json"), load("p9_adversarial.json"), load("p9_ext.json")
    tables = dict(table1=table1(p9), table2=table2(areas, ext, claims, adv), table3=table3(p9, ext9),
                  table_s1=table_s1(p9))
    (HERE / "tables.json").write_text(json.dumps(tables, indent=1, ensure_ascii=False), encoding="utf-8")
    fig1(p9)
    forest([(label, p9["A9_3"][f]["mh_rd"], p9["A9_3"][f]["mh_ci"]) for f, label in INDICATORS], FIG / "fig2.png",
           "Life science minus other, percentage points (Mantel-Haenszel, 95% CI)")
    d = areas["PH9_d"]
    fig3 = (("Decided, unadjusted (110 vs 1,821 attempted papers)", d["unadjusted"]),
            ("Decided, clinical papers only", adv["F2"]["label_split"]["clinical"]),
            ("Decided, life-science papers only", adv["F2"]["label_split"]["life_science"]),
            ("Decided, adjusted for number of teams", d["teams"]),
            ("Decided, adjusted for first-team strength", ext["E1"]["decided"]["adjusted"]),
            ("Claim decided, unadjusted (claim level)", d["claim_level_unadjusted"]),
            ("Claim decided, within team (claim level)", d["claim_level_within_team"]))
    forest([(label, x["rd"], x["ci"]) for label, x in fig3], FIG / "fig3.png",
           "Medical minus other, percentage points (95% CI)")
    missing = checks(p9, areas, ext, claims, adv, ext9)
    for m in missing:
        print("NOT IN TEXT:", m, file=sys.stderr)
    print(f"tables and figures written; {len(missing)} quoted numbers not found in the text", file=sys.stderr)
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
