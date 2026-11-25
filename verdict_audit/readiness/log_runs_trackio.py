"""Protocol 9, Note 9-36: log analyses and coding tasks as runs in the local Trackio project `p9-journal-runs`.

One run per task: config = note, script, git commit, model ids, prompt file and SHA-256, seeds, unit counts;
metrics = headline results and, where measured, tokens and API-equivalent cost (results/p9_costs.json).
Earlier coding tasks are logged retrospectively. Runs outside any logbook workspace; the project stays local.

Usage: python log_runs_trackio.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
PROMPTS = HERE / "codes" / "p9"
PROJECT = "p9-journal-runs"


def sha(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def commit() -> str:
    return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=HERE, capture_output=True, text=True).stdout.strip()


def load(name: str) -> dict:
    return json.loads((RES / name).read_text(encoding="utf-8"))


PROMPT_OF = {"p9_coder1": "CODER_PROMPT.md", "p9_coder2": "CODER_PROMPT.md", "p9_coder2full": "CODER_PROMPT.md",
             "p9_ext": "CODER_PROMPT.md", "p9_adjudication": "ADJ_PROMPT.md", "p9_ext_adj": "ADJ_PROMPT.md",
             "p9_ref": "REF_PROMPT.md", "p9_claims": "CLAIM_PROMPT.md"}


def runs() -> list[tuple[str, dict, dict]]:
    c = commit()
    out = []
    costs = load("p9_costs.json")
    for task, v in costs["tasks"].items():
        p = PROMPTS / PROMPT_OF[task]
        tok = {f"{m}/{k}": n for m, d in v["models"].items() for k, n in d.items()}
        out.append((f"{task}-retrospective",
                    dict(note=v["note"], kind="coding", retrospective=True, git_commit=c, models=sorted(v["models"]),
                         prompt_file=str(p.relative_to(HERE)), prompt_sha256=sha(p), units=v["units"], unit=v["unit"],
                         subagents=v["subagents"], dates=v["dates"], prices_source=costs["prices_source"]),
                    dict(cost_usd_low=v["cost_usd"][0], cost_usd_high=v["cost_usd"][1],
                         **({"cost_per_unit_usd_low": v["cost_per_unit_usd"][0],
                             "cost_per_unit_usd_high": v["cost_per_unit_usd"][1]} if v["cost_per_unit_usd"] else {}),
                         **tok)))
    a = load("p9_adj_types.json")
    out.append(("note-9-28-adjudication-types",
                dict(note="9-28", kind="analysis", script="posthoc_p9_adjudication_types.py", git_commit=c, models=[]),
                dict(variance_n=a["fields"]["variance"]["n"], variance_silence=a["fields"]["variance"]["silence_pairs"],
                     compute_n=a["fields"]["compute"]["n"], compute_silence=a["fields"]["compute"]["silence_pairs"],
                     reference_standard_n=sum(a["reference_standard"][k] for k in ("code_used", "data_obtained",
                                                                                     "weights_used")))))
    r = load("p9_reliability.json")
    out.append(("note-9-30-reliability",
                dict(note="9-30/9-35", kind="analysis", script="posthoc_p9_reliability.py", git_commit=c,
                     models=["zai-org/GLM-5.2 (challenge judge, from the data)"], seed=20261124, bootstrap=2000,
                     units=r["units_two_or_more_teams"]),
                dict(discordant_share=r["all"]["discordant_share"], paper_alpha=r["all"]["paper_alpha"],
                     paper_alpha_ci_low=r["all"]["paper_alpha_ci"][0], paper_alpha_ci_high=r["all"]["paper_alpha_ci"][1],
                     claim_alpha=r["all"]["claim_alpha"], teams_for_080=r["all"]["k_for_reliability_080"],
                     share_team=r["R1c_mixed"]["share_team"], share_paper=r["R1c_mixed"]["share_paper"],
                     medical_alpha=r["medical"]["paper_alpha"], other_alpha=r["other"]["paper_alpha"],
                     medical_papers=r["medical"]["papers"])))
    bp = PROMPTS / "barriers" / "BARRIER_PROMPT.md"
    out.append(("note-9-33-barriers-plan",
                dict(note="9-33", kind="planned coding", status="deferred by Kate 2026-11-25",
                     models=["claude-sonnet-5-5 (coders)", "claude-opus-5-5 (adjudicator)"],
                     prompt_file=str(bp.relative_to(HERE)), prompt_sha256=sha(bp), units=14980, unit="verdict",
                     git_commit=c), dict(units_planned=14980)))
    return out


def main() -> None:
    import trackio

    for name, config, metrics in runs():
        trackio.init(project=PROJECT, name=name, config=config)
        trackio.log(metrics)
        trackio.finish()
        print(f"logged {name}", file=sys.stderr)


if __name__ == "__main__":
    main()
