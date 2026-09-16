# Version-aware search for multi-version docs

A working prototype + eval harness for [mintlify discussion #5668](https://github.com/orgs/mintlify/discussions/5668):
on docs sites that ship multiple versions side by side, in-site search ranks purely by
relevance with no awareness of the version the reader is browsing — so old-version pages
outrank current-version equivalents and readers bail.

## What I built

- `corpus.py` — a synthetic multi-version docs corpus (versions `4.0`, `4.7.x`, `5.1`, `5.7`;
  30 pages across webhooks, auth, rate limits, quickstart, migration, SSO, CLI, errors,
  pagination) plus 10 queries with per-version ground truth.
- `rankers.py` — a TF-IDF baseline ranker (relevance only = reported current behavior) and a
  version-aware ranker implementing the discussion's three asks:
  1. **boost mode**: results from the browsed version get a multiplicative boost (default x1.75);
  2. **scope mode**: `docs.json`-shaped config scopes search to the browsed version only;
  3. **exclude_prefixes**: folder-prefix exclusion list, independent of `.mintignore`.
- `run_eval.py` — eval harness: 28 (query, browsing-version) pairs, reports top-1 version-hit
  rate, wrong-version top-1 count, and top-3 version share. Exits nonzero if the
  version-aware ranker doesn't beat naive (sanity gate).

Run it: `python3 run_eval.py` (pure Python, no dependencies).

## Verified results

```
ranker                      top1_version_hit  wrong_version_top1  top3_version_share
naive (relevance only)                0.357                18               0.310
version-aware boost x1.75            0.821                 5               0.345
version-aware scope                  1.000                 0               1.000
```

- The naive ranker **reproduces the exact repro from the discussion**: query `webhook`
  while browsing `5.1` returns `/4.7.x/setup-guides/plugins-setup-guide/reporting-setup`
  on top, ahead of the 5.1 webhook pages. 18 of 28 pairs put the wrong version first.
- Boost x1.75 fixes 13 of those 18 (top-1 version-hit 0.357 → 0.821).
- Scope mode (the discussion's option 2, project-level config) fixes all 28.

**Honest limits found by the eval** (not tuned away):

- All 5 remaining boost failures happen when the browsed version's page uses renamed
  vocabulary with weak exact-term overlap (e.g. 5.7's "Rate limiting" vs query
  "rate limits"). Raising the boost to x5.0 only reaches 0.893 — a multiplicative boost
  has a ceiling when the relevance gap is large.
- Two cases can *never* be fixed by boosting: `webhook` browsing 5.7 and `authentication`
  browsing 5.7 score **0.00** on the in-version page (plural "webhooks" with no stemming;
  the 5.7 auth page is OAuth-only with no "authentication" token). Boosting zero still
  gives zero — those need stemming/synonym expansion at index time, not ranking tweaks.
- Scope mode is exact but blunt: readers on old versions lose nothing, readers on the
  current version never see old pages — matching the tradeoff the discussion already notes
  for `noindex`.

## Disclosures

- The corpus is **synthetic**, constructed to reproduce the failure mode in #5668
  (old-version pages win on raw term frequency because they repeat legacy phrasing).
  It is not Mintlify's index, not scraped from any real docs site.
- This is a standalone prototype. It claims **no integration** with Mintlify's search
  stack and no knowledge of their internals — just a demonstration that version-aware
  ranking fixes the reported behavior, with measured before/after numbers and the
  boundary where boosting stops working.
