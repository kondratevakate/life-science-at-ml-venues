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
