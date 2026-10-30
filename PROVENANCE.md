# Provenance

This repository started on 2026-10-30 as a byte-identical copy of the paths the study needs, taken with `git archive`
from [kondratevakate/icml-2026-repro](https://github.com/kondratevakate/icml-2026-repro) at commit `acc3b15`
(branch `codex/medical-reproducibility-map`). All 742 imported files have the same git blob ids as in the source
commit. History before that point, including every protocol freeze, stays in the source repository.

## Protocol freezes (in icml-2026-repro, branch master)

| Commit | Date (UTC+4) | What |
|---|---|---|
| `3b9e5ea` | 2026-10-18 18:45 | Freeze Protocol 7: medical label and readiness across venues |
| `2d92340`, `f70d29e` | 2026-10-18 18:49, 18:59 | Protocol 7 amendments (2026 abstracts; 12 strata) |
| `3217b19` | 2026-10-19 00:17 | Freeze Protocol 8 |
| `839281e` | 2026-10-19 10:26 | Freeze Protocol 9 (this study) |

The first Protocol 9 full text was retrieved at 2026-10-19 06:31 UTC (10:31 UTC+4), five minutes after the freeze
(`retrieved_at` in the full-text manifest). Later decisions are dated notes in `PROTOCOL.md`, each committed before
the analysis it governs.

To check:

```bash
git clone https://github.com/kondratevakate/icml-2026-repro && cd icml-2026-repro
git show --stat 839281e
git diff 839281e acc3b15 -- verdict_audit/readiness/PROTOCOL.md   # only appended notes after the freeze
```

## Data

The verdict snapshot the analyses pin (`p8_common.VERDICTS_SHA`) is the challenge's public verdict file downloaded on
2026-10-17T17:24:53Z. Listings were downloaded on 2026-10-18 (`results/sources_manifest.json`); full texts between
2026-10-19 and 2026-10-23 with a SHA-256 per file in the full-text manifest.
