# Backlog

## Journal paper (added 2026-11-20)

Kate (2026-11-20, translated): "put the plan for the journal paper in the backlog; maybe strengthen it with the second poster, the one about the AI scientist".

**Target (revised 2026-11-22, Kate's choice).** Nature presubmission enquiry first, then PNAS. 2026 precedents:
Nature Articles on AI-scientist systems (Lu et al. 10.1038/s41586-026-10265-5; Gottweis et al.
10.1038/s41586-026-10644-y; Ghareeb et al. 10.1038/s41586-026-10652-y; Miao et al., Paper2Agent,
10.1038/s41586-026-11044-y) and PNAS on AI vs human reproducibility assessment (Brodeur et al.
10.1073/pnas.2524747123). Fallbacks in the same genre: Royal Society Open Science (10.1098/rsos.251997), Research
Integrity and Peer Review (10.1186/s41073-026-00266-3), Nature Machine Intelligence Analysis (only a 2021
precedent). For Nature or PNAS the cheap AI checker (below) likely belongs in this paper, not a second one.

**Plan.**
1. Quick fixes without new computation: one NeurIPS checklist kappa (0.21 vs 0.22); pooled code kappa 0.28 as the
   main reported value; "medical" to "health and life-science"; open-data claim restated with the within-data-type
   reversal (-6.1); drop the outputs sign-change sentence from the abstract.
2. Framing: RQ1 to RQ3 (reporting, reported vs used, verdict gap), new title (the PSE9 phrase "rarely picked" does
   not match the attempt rates, 33.5% vs 33.8%), 150-word abstract.
3. Six display items: summary; reported practices; reported vs used (Table 3 as a figure); verdict gap unadjusted
   and adjusted; open-data stratification; flow or design table. Topics, t-SNE and Table A1 to the supplement.
4. Science gaps from the simulated review and Attila's comments: human-coded validation subsample (needs
   co-author hours); first-team adjustment discussed as a possible mediator, with team-stratified estimates;
   comparison with external reproductions (RECLAIM, MLRC/TMLR; references through bib-verify); optional manual
   audit of judge verdicts.
5. Submission: NMI presubmission enquiry first; co-author review before any submission; confirm the author list with
   all co-authors.

**Idea: strengthen it with the second PSE9 poster (AI scientist / voters).** Abstract 1 ("From scarcity to
abundance: when AI agents reproduce every paper, who decides who is right?", `icml-repro-working/verdict_audit/voters/`)
studies how verdicts of many agent reproductions are aggregated. It could answer the weakest point of this paper,
the reliability of the judge and of single-logbook verdicts. Parked because: not yet decided whether it joins this
paper or stays separate. Reopen when: the NMI framing (step 2) is decided.

## Framing option: where the bottleneck moves (added 2026-11-24)

Kate (translated): "there are dedicated grants for reproduction; how will they change now that agents exist, and
what will the bottleneck be in the end?" She also preferred option B: lessons from earlier reproduction challenges.

**Frame.** Funding reproduction in the age of agents. Compare waves: human challenges (MLRC since 2019, Replication
Games) vs agent challenges (ICML 2026, NeurIPS 2026). Agents make a run cheap (about USD 66 per confirmed
reproduction in RECLAIM; under USD 1 per AI review in the AAAI-26 pilot; vs 7 hours of a three-person team in
Brodeur et al.), so the bottleneck moves to:
1. data access (agents cannot sign data use agreements; our health papers: access often unstated, 49% vs 25%
   inconclusive claims);
2. human checking of verdicts (AI-led teams 37% in Brodeur; REPRO-Bench agents below chance; verdicts of different
   teams on the same paper disagree in our data);
3. selection of papers (volunteer choice; fewer teams per health paper; RECLAIM uses a fixed, preregistered set);
4. compute mostly not (RECLAIM uses about 6% of its GPU budget), except claims that need retraining.

**Recommendations to test or argue.** Funders pay for access infrastructure (IDC-like, credentialed sandboxes,
synthetic releases), for human adjudication of verdicts, and for representative paper selection, not for runs.

**Grant landscape (checked 2026-11-24 by web search).** Open Science NL (NWO) Replication Studies (pilot 2016,
EUR 3 million; 2025 round awarded; instrument in the 2026-2027 work programme, lower total budget); Horizon Europe
WIDERA reproducibility topics in 2022 and 2024 (e.g. REWIRE), none found for 2026 or 2027; Coefficient Giving
funded agent benchmarks for reproducibility (COS ReplicatorBench, KDD 2026; its USD 25 million RFP is closed).
Open Science NL might also fit Kate's own grant; eligibility not checked.

**Needed data.** MLRC outcomes are not aggregated anywhere found so far; coding human challenge reports is the
costly part. Reopen when the framing is chosen (BACKLOG step 2).

## Framing option: "verified is not valid" (added 2026-11-24, concrete RQs)

Nothing is frozen or run; each RQ becomes a protocol note with its criterion before any computing or coding.
Counts below are a crude first look (all logbooks, the first author's own not yet excluded, no deduplication).

**RQ1 reliability.** 2,118 judged papers; 973 attempted by two or more teams (313 by six or more); in 547 of the 973
the teams disagree on whether any claim was decided. Measure: between-team agreement on paper and claim verdicts,
variance split into paper, team and judge parts, and the number of independent attempts needed for a stable verdict.

**RQ2 cost and triage.** Does the cheap static coding of the paper text predict the outcome of runs (ICML 2026
verdicts; RECLAIM per-paper outcomes)? Report the share of runs a pre-screen would save.

**RQ3 scientific validity, by people.**
- Units: ICML 2026 frame papers with at least one verified claim: 51 health and life-science and 67 other (crude).
  Sample: all health papers plus a seeded random 50 other papers, about 100 papers.
- Instrument (fixed before coding): five validity threats, each coded present / absent / unclear with a quote:
  (a) leakage (patient-level split, preprocessing or tuning on test data, test reuse); (b) shortcut or confounding
  in the data (site, scanner, demographics, label proxies); (c) weak baselines (untuned, outdated, missing obvious
  comparator); (d) evaluation scope (no external data, no variance); (e) conclusion broader than the evidence
  (population, task, clinical claim). Items mapped to REFORMS and to the Kapoor and Narayanan leakage taxonomy.
- Procedure: two independent expert coders per paper, blind to group labels as far as possible and to the judge's
  evidence text; disagreements adjudicated by a third expert; agreement reported per item.
- Outcomes: share of verified papers with at least one major threat, by group; whether the logbook or the judge
  mentioned the threat (did the agent catch it); agreement of our LLM coder with the experts on the same checklist.
- People: expert coders in dataset validity, evaluation and clinical imaging; names only after they agree.
  Effort: about 100 papers x 2 coders; minutes per paper not yet estimated.

**RQ4 where agents stall in life science.**
- Units: all inconclusive and toy claim verdicts of attempted ICML 2026 papers.
- Measure: classify the judge's evidence text for each such claim into one barrier: data not accessible; compute or
  scale; code missing or broken; environment; claim not checkable as stated; attempt incomplete. LLM coding with a
  human-checked subsample.
- Analysis: barrier shares by group; link to coded main data access (open, credentialed, private, unclear);
  upper bound of claims that would become decidable if one barrier were removed.
- Policy output: barriers ranked by claims unlocked per unit cost, using published cost anchors (RECLAIM, AAAI-26,
  ReproRepo, PaperBench); maps to what funders should pay for (access infrastructure, compute, author release).
- Optional test: IDC data access for imaging papers whose claims were inconclusive for lack of data.
