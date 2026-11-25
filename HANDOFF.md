# HANDOFF

State on 2026-11-23, end of day. Repo `C:\Projects\02_academia\studies\life-science-at-ml-venues`, branch
`attila-comments-adjudication` (pushed, no PR yet; `main` untouched). Work by Claude in a side session of the PSE9
paper thread. Backlog and journal plan: `BACKLOG.md`.

## Done in this block

- Co-author comments in Overleaf (2 threads, 2026-11-09) answered in Overleaf on 2026-11-20; the three promised
  edits are in Overleaf `main.tex` and in `manuscript/manuscript.md` (commit a6fd3d5): 1,553 corrected to 1,521
  plus 32 reference-standard disagreements; disagreement breakdown in Methods (Note 9-28,
  `verdict_audit/readiness/posthoc_p9_adjudication_types.py`); group-composition paragraph in Results (Note 9-26).
  39 tests pass; number check finds 0 missing quotes.
- Venue decided by Kate on 2026-11-22: Nature presubmission enquiry first, then PNAS (precedents with DOIs in
  `BACKLOG.md`). The enquiry draft is not written yet (Kate: "not now").
- Simulated reviews: TMLR format and Nature Machine Intelligence format (both in chat only). Main asks: a
  human-coded validation subsample, a mediator-aware analysis of the first-team adjustment, comparison with
  external reproductions, the open-data reversal within data type in the main text.

## Literature (side session "Literature review: preregistration and evidence in ML")

About 55 sources over four themes (preregistration formats, agent and human reproduction, evidence grading,
LLM reviewers), plus full-text extraction of 12 key papers: questions, design, resources, results. Results are in
that session's chat; full texts are in a temporary folder that may be cleared. Key facts, all from full texts:

- No paper of the 12 states numbered research questions; only Brodeur et al. (PNAS 2026, OSF sz2g8) was
  preregistered. None compares reported practices with materials actually used: this paper's niche.
- Cost anchors: under USD 1 per AI review (AAAI-26 pilot); about USD 1.3 per static audit (ReproRepo); USD 12 per
  reproduction run and USD 66 per confirmed reproduction (RECLAIM); about USD 400 per paper (PaperBench).
- ReproRepo's 89.7% is on 280 ICLR 2026 papers only, not on all 1,149.
- Gaps left by the 12 papers that our existing data can fill: reported vs used material; agreement between teams
  instead of one run; self-selected attempts at scale; who checks (first-team effect); health vs other domains;
  release level vs verdict. Not possible without new work: judge reliability against humans (needs the
  human-coded subsample).
- To check in our data: whether the challenge snapshot holds the logbook authors' own verdicts, to compare with
  the judge (as RECLAIM compared 128 claimed with 73 confirmed reproductions).

All references still need a full `bib-verify` pass before they enter the manuscript.

## Proposed tests of the recommendations (not frozen, not run)

Each to be frozen as Note 9-29 onward with a success criterion before computing:
1. Explicit data-access statement vs `unclear`: decided-verdict rate among attempted papers.
2. Claim cost (analysis only vs retraining) predicts the verdict (extends Notes 9-13 and 9-14).
3. Material actually used (logbook codes, 522 papers) explains verdicts better than stated availability.
4. Cheap checker baseline: predict a decided verdict from the paper excerpt on a model ladder, cheapest first;
   compare with NeurIPS checklist answers; reference = 1,931 attempted papers.
5. Optional intervention pilot: give an agent data access through IDC (Imaging Data Commons) MCP for imaging
   papers that were inconclusive for lack of data; needs a cost estimate first; IDC MCP capabilities unchecked.
Kate's view (2026-11-22): recommendations without testing or implementation are weak.

## Datasets found (nothing downloaded)

- Already local: ICML 2026 challenge snapshots and logbooks (`C:\Projects\data`, registry ids
  `icml2026-challenge-snapshots`, `icml2026-repro-logbooks-2026-10-18`).
- Hugging Face: `Mithilss/reclaim` (100 NeurIPS 2025 papers, fixed claims, release tiers, GPU estimates, CC BY 4.0;
  run logs on GitHub `mithils3/reclaim`), most useful because NeurIPS 2025 is in our frame; overlap not yet
  checked (Kate: "not now"). Also `chuxuan/REPRO-Bench`, `siegelz/core-bench`, `josancamon/paperbench` (mirror;
  official in `openai/preparedness`), `Just-Curieous/EXP-Bench`, `ChristineYe8/ReplicationBench`.
- Not found on Hugging Face: ReproRepo data, the Brodeur replication-games data, an MLRC or ReScience summary.

### Dataset plan to strengthen the paper (agreed with Kate 2026-11-24, nothing run yet)

In order; freeze each as a protocol note with a success criterion before computing:
1. ICML 2026 data we already hold (free): agreement of verdicts between teams on the same paper; and, if the
   snapshot holds them, the logbook authors' own verdicts against the judge's (RECLAIM's analogue: 128 claimed vs
   73 confirmed).
2. RECLAIM (`Mithilss/reclaim`, 100 NeurIPS 2025 papers, CC BY 4.0): run our unchanged full-text coder prompt on
   the 100 papers and test whether coded practices (code, weights, data access, claims linked) predict RECLAIM's
   per-paper outcome and match its release tier. Works even without overlap with our frame; also count the overlap.
   Cost: one small download plus tokens for 100 papers (estimate: a few USD). Answers the review point on
   external reproductions with a fixed, preregistered set.
3. NeurIPS 2026 ML Intern Reproductions: after the hackathon (ends 13 Dec 2026 per web search), use its logbooks
   as a second venue and wave; NeurIPS 2026 full texts are now public, which also fills the 464 frame papers that
   had no full text.
4. REPRO-Bench (`chuxuan/REPRO-Bench`, 112 papers with human reproducibility scores): human reference for the
   cheap-checker baseline.
5. IDC through MCP: optional intervention pilot, only after a cost estimate.
PaperBench, EXP-Bench and CORE-Bench serve as context only (2024 or non-venue papers).

## New and ongoing (checked 2026-11-23)

- NeurIPS 2026 ML Intern Reproductions (Hugging Face org `Neurips-2026-MLIntern-Repro`): dataset `papers` with
  1,046 NeurIPS 2026 papers, one claim each; registration Space live. Per web search (not checked on the org
  page): hackathon 30 Nov to 13 Dec 2026, registration by 29 Nov. A second wave of agent-reproduction data,
  directly comparable with ICML 2026.
- MLRC 2026 is an official NeurIPS 2026 track (TMLR-first); 16 papers accepted; scope includes AI tools for
  replicating papers.
- arXiv 2610.22465 (2026-10-15): "Author-in-the-loop Agentic Reproducibility Auditing for a Machine Learning
  Conference", agent audits with author declarations as explicit inputs. Closest to the claim-manifest standard.
- arXiv 2609.11117: NLPCC 2026 Shared Task 11, agent-based experiment reproduction (AgentActionBench).

## Journal-paper experiments (frozen 2026-11-24, Notes 9-29 to 9-34)

- Design frozen before computing: RQ1 reliability across teams (9-30), RQ2 triage (9-31), RQ3 expert validity
  (9-32), RQ4 barriers (9-33); 9-34 corrects the verdict snapshot to the pinned 2026-10-17 file.
- RQ1 computed (`posthoc_p9_reliability.py`, `results/p9_reliability.json`): 903 papers with two or more teams;
  56% discordant on decided; paper-level alpha 0.21 (0.18 to 0.25), claim-level 0.21; about 15 teams for
  reliability 0.80; team 48% vs paper 15% of variance (mixed model); medical vs other alpha difference not
  established. Identical under PYTHONHASHSEED 0 and 1 (mixed-model values
  rounded to 6 decimals because the variational fit differs in the 8th decimal).
- RQ4 is a plan only (Kate, 2026-11-25: "not coding for now"): code all 14,980 inconclusive or toy verdicts (582
  medical) with two blind coders and adjudication; prompt committed at `codes/p9/barriers/BARRIER_PROMPT.md`; the
  sheet builder `build_p9_barriers.py` is not written yet.
- RQ2 waits for Kate's approval to download RECLAIM; RQ3 waits for expert coders who agree.

## Open items

- Nature presubmission enquiry: framing decision (lead with reported vs used, not the verdict gap), referenced
  summary paragraph, co-author review before sending, confirm the author list.
- Step-1 quick fixes from `BACKLOG.md` (NeurIPS kappa 0.21 vs 0.22 and others) not done.
- Overleaf PDF not recompiled or checked by eye after the 2026-11-20 edits.
- Decide whether to join the NeurIPS 2026 reproduction hackathon or only use its data later.
- Open a PR for this branch when Kate wants it merged.
