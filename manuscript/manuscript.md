# Well documented, rarely picked: a systematic meta-research study of reproducibility practice in medical and life-science papers at top machine-learning venues and their agentic reproduction

Ekaterina Kondrateva^1,2^, Florian Kofler^1,3,4,5^, Attila Simkó^6^

^1^ Hertie AI Institute for Brain Health, University of Tübingen, Tübingen, Germany
^2^ Maastricht University, Maastricht, the Netherlands
^3^ University of Zurich, Zurich, Switzerland
^4^ Technical University of Munich, Munich, Germany
^5^ Helmholtz Munich, Munich, Germany
^6^ Umeå University, Umeå, Sweden

Corresponding author: Ekaterina Kondrateva, [EMAIL]. ORCID 0000-0003-3623-6106.

## Abstract

**Background.** Medical and life-science machine-learning (ML) papers are often assumed to be hard to reproduce because their data are restricted and their code is not shared. Agentic reproduction, in which AI agents attempt to rerun published work, now makes it possible to test this at conference scale.

**Methods.** We drew all 2,170 papers labelled clinical or life science by blind language-model coders (Cohen's kappa 0.96) from nine venue-years of CVPR, ICCV, ECCV, ICLR, ICML and NeurIPS (2025 to 2026), and an equal random sample of other papers. Two blind language-model coders read the full texts of the 3,278 papers we could retrieve and coded twelve reproducibility practices under a protocol frozen before data collection. Differences were pooled across venue-years with Mantel-Haenszel risk differences and paper bootstrap intervals. Outcomes of reproduction came from the public verdicts of the ICML 2026 agent reproduction challenge.

**Results.** Life-science papers were the better-documented group: code released 59% versus 46% (pooled difference +13 points, 95% CI +10 to +17), main data openly available where access was stated (+15, +11 to +19), weights released (+29, +22 to +35) and variance reported 66% versus 42% (+24, +21 to +28). These held for each coder, without any one venue-year, and on untruncated texts. In the challenge, attempted medical papers received a verified or falsified verdict 19 points less often than 1,821 other attempted papers (CI −28 to −10; permutation p < 0.001), mainly clinical papers. Within the same team, claims were decided about equally often (−3.6, CI −7.8 to +0.8). Medical papers were first taken up by teams that settled fewer of their other papers (40% versus 60%), and adjusting for this removed the gap (−3.6, CI −12 to +5). Their claims needed retraining or large-scale runs more often (57% versus 39%, +18, CI +10 to +26). Stated practices predicted poorly what reproducers obtained (code: kappa 0.22).

**Conclusions.** Crowd reproduction does not fail medical papers for lack of stated materials. It sends them to fewer and less decisive teams and asks costlier questions. Reproduction efforts should report who attempted each paper and what its claims cost to check.

## Introduction

Concerns about the reproducibility of medical artificial intelligence are long-standing. When a high-profile study of AI for breast cancer screening was published without its code and with few methodological details, critics argued that this undermined its scientific value [1]. A survey of 511 papers found that ML for health compared poorly with other areas of ML on dataset and code accessibility [2], and an audit of 400 AI conference papers found that none documented all the variables a reproduction needs [3]. NeurIPS responded with a code submission policy and a reproducibility checklist [4], and failures such as data leakage have been traced across 17 fields that apply ML [5].

These studies measure what authors state. Whether stated materials let a third party settle a paper's claims is a different question, and until recently it could not be asked at scale, because each reproduction took weeks of expert work. AI agents now attempt reproductions of whole papers [6]. In 2026 the International Conference on Machine Learning (ICML) ran an open agent reproduction challenge in which more than 1,200 participants published 6,816 reproduction logbooks on 2,226 conference papers, and an automated judge rated 35,908 claims as verified, falsified, toy (evidence at reduced scale) or inconclusive [7]. This gives, for one venue, an outcome for reproduction that does not depend on what authors say about their own work.

We asked two questions. First, do medical and life-science papers at top ML venues state reproducibility practices (code, data access, weights, variance, compute) less often than other papers, as is commonly assumed? Second, in the ICML 2026 challenge, are medical papers settled (verified or falsified) as often as other papers, and if not, why? We expected life-science papers to be less well documented and prespecified this direction. The data showed the opposite on documentation, and a gap in the other direction on outcomes, which we then examined with prespecified post hoc analyses.

## Methods

### Protocol and reporting

The study followed a written protocol (Protocol 9) frozen in a public git repository before the paper frame was drawn, before any full text was retrieved and before any coding (commit 839281e, 19 October 2026, five minutes before the first full text was retrieved). The protocol builds on three earlier protocols in the same repository (Protocols 6 to 8, on the same challenge) and was designed after their results were known. Every later decision is recorded as a dated note in the protocol (Notes 9-1 to 9-21), written before the analysis it governs was computed. Analyses beyond those in the protocol are reported as post hoc. We report the study following the PRISMA 2020 statement [8] where its items apply to a meta-research study of published papers; the completed checklist is in Supplementary File S2. The protocol, all notes and their commit history are in Supplementary File S1 and the repository.

### Information sources and eligibility

The sources were the public virtual-site listings of nine venue-years: CVPR 2025, ICCV 2025, ECCV 2026, ICLR 2025, ICLR 2026, ICML 2025, ICML 2026, NeurIPS 2025 and NeurIPS 2026 (40,290 papers after removing duplicates and papers without an abstract). Abstracts missing from the 2026 listings were taken from the challenge's paper metadata (ICML 2026) or from each paper's page on the venue site (ICLR 2026, NeurIPS 2026, ECCV 2026).

A paper was a candidate for the medical and life-science group if its venue topic was a health, biology, neuroscience or chemistry topic, or its title or abstract matched a prespecified regular expression of clinical and biological terms (Supplementary File S1, Protocol 7). This gave 5,530 candidates. Each candidate was labelled `clinical`, `life_science` or `no` from title and abstract only by a blind language-model coder; a second blind coder labelled a random 25% of candidates (1,633 papers over the whole listing; agreement 97.7%, Cohen's kappa 0.96 [9]; gate 0.80) and disagreements were adjudicated with a written reason. Of the candidates, 1,013 were labelled clinical and 1,157 life science (2,170 together, the life-science group below) and 3,360 were excluded. To estimate how many medical papers the prefilter missed, both coders labelled a random 200 non-candidates; none was medical (0 of 200, 95% Wilson interval [10] 0 to 1.9%). The comparison group was a random sample of 2,170 non-candidates, allocated to venue-years in proportion to the life-science counts (seed 20261019).

### Full-text retrieval and excerpts

Full texts were retrieved in a fixed order: arXiv HTML, then arXiv PDF (arXiv identifier from a title search, accepted at a normalised title similarity of at least 0.95 and an arXiv year no earlier than the venue year minus one; ambiguous matches excluded), then the open proceedings (CVF, PMLR). Papers without a full text were counted and not imputed. From each full text an excerpt of at most 15,000 characters was built from the end of the introduction, sections whose heading concerned availability, reproducibility, ethics, data, setup, implementation, training, compute or limitations, the NeurIPS checklist items on reproducibility, and paragraphs on seeds and repeated runs, with a truncation flag per paper.

### Data items and coding

Each excerpt was coded on twelve fields (Table 1 lists the indicators): whether main claims were listed and linked to evidence; code (released, promised, no); main data access (open, credentialed or on request, private, synthetic only); an experiment on open data; release of synthetic or sample data, of weights and of outputs; variance (several seeds, error bars or intervals); environment (versions or container); compute (amount, hardware only, none); compute tier; and training-set scale. Every field allowed `unclear`. Coders used stated text only; a named dataset without stated access terms was `unclear`.

Coding was done by language-model subagents (claude-sonnet-5-5), 20 papers per batch, with venue, year and group hidden. Coder 1 coded all papers and coder 2 a random 25% (813 papers). The protocol set a gate of kappa 0.80 on each primary field (code, main data access, weights, variance, compute). Code (0.85), main data access (0.83) and weights (0.96) met the gate and use coder 1's codes. Variance (0.71) and compute (0.70) did not; as the protocol required, coder 2 then coded these two fields for all papers and every disagreement (1,404 items) was adjudicated by a blind adjudicator (claude-opus-5-5) who saw the two labels in random order and gave a reason.

### Reproduction outcomes

Outcomes came from the public verdict snapshot of the ICML 2026 agent reproduction challenge retrieved on 17 October 2026 [7]. A paper was attempted if it had at least one logbook and decided if at least one of its claims was rated verified or falsified. Logbooks were deduplicated, and the first author's own logbooks were excluded because the first author took part in the challenge. Of the 6,341 ICML 2026 papers, 622 candidates labelled `no` were excluded, leaving 328 medical and 5,391 other papers.

To test whether stated practices agree with what reproducers obtained (reference standard), two blind coders read the logbooks of the 222 attempted ICML 2026 papers in the frame and coded whether the authors' code was obtained and run, the main data obtained, and weights used; disagreements were adjudicated as above. A further random 300 attempted ICML 2026 papers outside the frame were added later under a prespecified extension (Note 9-17).

### Quantitative synthesis

For each indicator we computed the share of papers with the practice among papers with a known value (`unclear` excluded and counted), by group and venue-year, with Wilson intervals [10]. The difference between groups was pooled over the nine venue-years as a Mantel-Haenszel risk difference [11], with a 95% interval from 2,000 paper bootstrap resamples within strata (seed 20261017; results identical under two hash seeds). Three directional labels were prespecified: life-science papers report open main data, release weights and report variance less often; a label was to be assigned only if the pooled interval excluded zero in that direction.

For reproduction outcomes the primary analysis compared the decided share of attempted papers by group, unadjusted and adjusted for compute tier and data scale. Post hoc analyses (Notes 9-9 to 9-15), each with its reading rule frozen before computing, examined how many teams attempted each paper, the strength of the first team (the share of its other attempted papers on which its own latest logbook was decided, the paper itself left out), within-team claim-level differences, and the cost of checking each claim. For the last, two blind coders labelled every distinct claim text of the 110 attempted medical papers and of 110 randomly drawn attempted other papers as needing inference only, retraining, large-scale runs, or analysis only. An adjustment was read as accounting for a gap if the adjusted estimate was less than half the unadjusted one and its interval included zero. Adversarial checks (Note 9-12) stated in advance what would refute each main claim.

### Ethics

The study used published papers and public challenge records. It involved no human participants and no personal or patient data, and no ethics approval was required.

## Results

### Study selection

Figure 1 shows the flow of papers. Of the 4,340 papers in the frame, full texts were retrieved for 3,278 (1,568 life-science and 1,710 other papers); 1,057 could not be matched to a full text, 4 failed to download and 1 had no usable text. Retrieval was complete or nearly complete for ICML, CVPR and ICCV, which have open proceedings, and lowest for NeurIPS 2026 (165 of 431 life-science and 212 of 431 other papers) and the other venue-years that relied on arXiv alone (Supplementary Table S1). Of the excerpts, 2,793 reached the 15,000-character cap.

### Documentation practices

Table 1 gives every indicator. Life-science papers stated nine of the ten practices more often than other papers. They released code in 59.4% of papers with a known value against 46.2% (pooled difference +13.1 points, 95% CI +9.6 to +16.6), reported open main data in 83.7% against 67.3% (+15.0, +10.7 to +19.3), released weights in 48.6% against 19.4% (+28.6, +21.6 to +35.0) and reported variance in 66.4% against 42.1% (+24.4, +20.7 to +27.9). None of the three prespecified labels was assigned: all three differences ran in the direction opposite to the one we had expected. The exception was claims listed and each tied to a table, figure or theorem, which was rare in both groups (2.7% against 6.1%, −3.3 points, −4.7 to −1.9). Compute was rarely stated by either group (21.7% and 17.1% gave an amount), and most papers did not state their compute tier (1,349 of 1,568 life-science papers).

The four main differences survived every prespecified check (Note 9-12, F1): leaving out each venue-year in turn, using coder 1's or coder 2's codes alone, restricting to papers whose excerpt was not truncated, and stratifying by venue-year and excerpt length. They held for clinical and life-science papers separately and for vision venues (CVPR, ICCV, ECCV) and learning venues (ICLR, ICML, NeurIPS) separately, except open main data at vision venues (+7.5, −1.9 to +16.9).

### Reproduction outcomes in the ICML 2026 challenge

Medical papers were attempted about as often as other papers (110 of 328, 33.5%, against 1,821 of 5,391, 33.8%) but by fewer teams (mean 1.5 against 3.3 teams per attempted paper). Among attempted papers, 46.4% of medical papers were decided against 65.5% of other papers, a difference of −19.1 points (95% CI −28.4 to −9.6; permutation p = 0.0005). The gap was larger for clinical papers (−23.6, −36.2 to −10.9) than for life-science papers (−13.4, −27.5 to +0.9), and it remained when every logbook of the team with the most medical attempts was dropped (−19.1, −29.7 to −8.7). The same direction held for full verification (some logbook verified every claim it rated: −19.3, −22.1 to −15.7) and for any falsified claim (−10.8, −16.9 to −4.1). In the prespecified analysis on the 222 attempted frame papers, the gap was −17.0 points (−29.7 to −4.4); adjusting for stated compute tier and data scale left it at −14.7 (−28.8 to −0.5), so scale did not account for it.

Table 2 shows the post hoc decomposition. The judge did not treat medical claims differently: within the same team, claims of medical papers were decided 3.6 points less often than claims of other papers (−7.8 to +0.8), against 29.1 points less often without this adjustment. The first team to take up a medical paper had settled 40.0% of its other attempted papers, against 60.3% for teams first on other papers (−20.3, −26.0 to −14.3). Adjusting for this first-team strength reduced the decided gap from −19.1 to −3.6 points (−11.9 to +5.1), which meets the reading rule. Claims of medical papers were also costlier to check: of 1,083 coded claims, 56.7% of medical against 39.1% of other claims needed retraining or large-scale runs (+17.6, +9.7 to +25.8), and fewer could be settled by analysis alone (19.3% against 45.3%). For full verification, adjusting for first-team strength reduced the gap from −19.1 to −13.0 points (−20.7 to −5.1) on the claim-coded sample, and adjusting for both strength and claim cost reduced it to −5.6 (−11.9 to +1.4).

### Stated practices against what reproducers obtained

On the 222 attempted frame papers, a stated code release agreed poorly with reproducers having run the authors' code (sensitivity 0.74, specificity 0.56, kappa 0.22; n = 162 with a known value on both sides), and stated open data agreed poorly with reproducers having obtained the data (kappa 0.13, n = 89). Weights agreed better (kappa 0.55, n = 43). Pooled with the 300 extension papers, the kappas were 0.28 (n = 347), 0.16 (n = 163) and 0.60 (n = 118). In NeurIPS papers, the checklist answer on open code agreed with the coded code release at kappa 0.22 (n = 152) (Table 3).

## Discussion

### Principal findings

Across nine venue-years of six top ML venues, medical and life-science papers stated more of the practices that reproduction needs than other papers did: code, open data, weights and variance. This contradicts the assumption we set out to test. Yet in the one venue where outcomes could be observed, medical papers were settled less often by agentic reproducers. The gap was not in how the judge treated their claims. It went with which teams took the papers up and with what their claims cost to check: medical papers were taken up by fewer teams, first by teams that settled fewer papers of any kind, and their claims more often required retraining or large runs. With both factors taken into account, the gap in full verification fell from −19 to −6 points and its interval included zero.

### Comparison with earlier work

An earlier survey found weaker sharing in ML for health than in other ML areas [2]. Our frame differs: it covers only papers accepted at general ML venues, several of which have introduced code policies and checklists [4], and it compares life-science papers with other papers at the same venues and in the same years. Within this setting the life-science papers documented more. Earlier audits measured documentation alone [3]; here it could be compared with what reproducers obtained, and a stated code link agreed with a reproducer actually running the authors' code at a kappa of only 0.22. PaperBench evaluated agents on a fixed set of 20 ICML 2024 Spotlight and Oral papers [6]; in an open challenge, by contrast, participants choose what to attempt, and the challenge data show that the domain of a paper changes who attempts it and what is asked.

### Implications

For venues and challenge organisers, the main implication is that the share of papers verified depends on who attempts them and on what their claims cost to check, not only on what authors provide. A verified rate reported without these two factors would mislead readers about medical papers. We suggest that crowd reproduction efforts report, per paper, the number and track record of the teams that attempted it and the share of its claims that need retraining or large-scale runs. For medical ML authors, our results suggest that more documentation alone will not raise the share of their papers that are settled, because the documentation is already above the venue average.

### Strengths and limitations

The frame is a census of life-science papers at nine venue-years with a matched comparison group, the protocol and coding rules were fixed before data collection, every coding decision is public, and the main differences survived prespecified attempts to refute them. The study has several limitations. All coders, adjudicators and the challenge judge are language models; agreement between coders was high, but they may share systematic errors. Full texts were missing for a quarter of the frame, mostly at NeurIPS 2026 and ICLR, where we relied on arXiv. Many excerpts were truncated, so release fields are often `unclear` and their shares are lower bounds. Coded practices are what authors state, not working artifacts. The reproduction outcomes come from one venue, one challenge and one judge model, and the challenge's participants chose what to attempt. Protocol 9 was designed after the results of earlier protocols on the same challenge were known, and the explanations of the outcome gap (team strength and claim cost) are post hoc, although each reading rule was frozen before computing. The analyses are observational.

### Conclusions

Medical and life-science papers at top ML venues are better documented than other papers at the same venues, yet in agentic crowd reproduction they are settled less often. The gap follows the teams that take them up and the cost of their claims, not a lack of stated materials. Reports of crowd reproduction should state who attempted each paper and what its claims cost to check.

## Declarations

**Data availability.** The paper-level table (4,340 papers with identifiers, titles, group, full-text status and all codes), the claim codes, the frozen protocol and all aggregate results are available at https://github.com/kondratevakate/life-science-at-ml-venues [DOI to be added on release] (code MIT licence; data and text CC BY 4.0). Abstracts and full texts were retrieved from public conference websites, arXiv and open proceedings and are not redistributed for copyright reasons; the repository contains the retrieval scripts and SHA-256 manifests of the retrieved files. Challenge verdicts come from the public snapshot of the ICML 2026 agent reproduction challenge retrieved on 17 October 2026. No patient or participant data were used.

**Code availability.** All analysis code is in the repository above; `python setup_data.py` links the retrieved inputs and each analysis script reproduces its result file. Rerunning all Protocol 9 analyses from the committed codes gave byte-identical results.

**Ethics approval and consent.** Not applicable: no human participants or personal data.

**Competing interests.** EK took part in the ICML 2026 agent reproduction challenge as a reproducer; her own logbooks were excluded from all analyses. [Other competing interests of all authors to be added.]

**Funding.** [To be added.]

**Author contributions.** [To be added in CRediT terms.]

**Use of AI tools.** Paper labels, full-text codes, reference-standard codes, claim codes and adjudications were produced by language-model subagents (claude-sonnet-5-5 and claude-opus-5-5) under the frozen protocol and prompts, which are public in the repository. Analysis code and drafts of this manuscript were written with the assistance of Claude (Anthropic). The authors checked every number against the result files and take responsibility for the content.

## References

1. Haibe-Kains B, Adam GA, Hosny A, Khodakarami F, Massive Analysis Quality Control (MAQC) Society Board of Directors, Waldron L, et al. Transparency and reproducibility in artificial intelligence. Nature. 2020;586(7829):E14–6. doi:10.1038/s41586-020-2766-y
2. McDermott MBA, Wang S, Marinsek N, Ranganath R, Foschini L, Ghassemi M. Reproducibility in machine learning for health research: still a ways to go. Sci Transl Med. 2021;13(586):eabb1655. doi:10.1126/scitranslmed.abb1655
3. Gundersen OE, Kjensmo S. State of the art: reproducibility in artificial intelligence. Proc AAAI Conf Artif Intell. 2018;32(1). doi:10.1609/aaai.v32i1.11503
4. Pineau J, Vincent-Lamarre P, Sinha K, Larivière V, Beygelzimer A, d'Alché-Buc F, et al. Improving reproducibility in machine learning research (a report from the NeurIPS 2019 reproducibility program). J Mach Learn Res. 2021;22(164):1–20.
5. Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. Patterns. 2023;4(9):100804. doi:10.1016/j.patter.2023.100804
6. Starace G, Jaffe O, Sherburn D, Aung J, Chan JS, Maksin L, et al. PaperBench: evaluating AI's ability to replicate AI research. In: Proceedings of the 42nd International Conference on Machine Learning. PMLR; 2025. p. 56843–73.
7. Abid A. What we learned by reproducing 2,200 papers from ICML [Internet]. Hugging Face; 2026 Aug 13. Available from: https://huggingface.co/blog/icml-2026-open-reproductions
8. Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71. doi:10.1136/bmj.n71
9. Cohen J. A coefficient of agreement for nominal scales. Educ Psychol Meas. 1960;20(1):37–46. doi:10.1177/001316446002000104
10. Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc. 1927;22(158):209–12. doi:10.1080/01621459.1927.10502953
11. Mantel N, Haenszel W. Statistical aspects of the analysis of data from retrospective studies of disease. J Natl Cancer Inst. 1959;22(4):719–48. doi:10.1093/jnci/22.4.719

## Tables

TABLE1

TABLE2

TABLE3

## Figure legends

**Figure 1.** Flow of papers through the study. Counts per venue-year are in Supplementary Table S1.

**Figure 2.** Life-science minus other papers, Mantel-Haenszel risk difference over nine venue-years with 95% bootstrap intervals, for each reproducibility practice stated in the full text.

**Figure 3.** Decided share among attempted ICML 2026 papers, medical minus other, unadjusted and after each adjustment, with 95% bootstrap intervals.
