"""Eval harness: reproduces discussion #5668 and measures the fix.

For every (query, browsing_version) pair, ranks the corpus with the naive
relevance-only ranker and with the version-aware ranker, then reports how often
the top result belongs to the version the reader is actually browsing.

Metrics:
  top1_version_hit   % of pairs where the #1 result is in the browsed version
  wrong_version_top1 count of pairs where #1 is a DIFFERENT version (the reported bug)
  top3_version_share mean share of the top-3 results in the browsed version

Exit code is nonzero if the version-aware ranker does not beat naive — a sanity
gate so the "fix" can't be claimed without evidence.
"""

import copy
import sys

from corpus import PAGES, eval_pairs
from rankers import TfidfIndex, naive_rank, version_aware_rank, DEFAULT_CONFIG


def evaluate(rank_fn):
    pairs = list(eval_pairs())
    top1_hits = 0
    wrong_version = 0
    top3_share_sum = 0.0
    rows = []
    for q, version, _relevant in pairs:
        results = rank_fn(q, version)
        top3 = results[:3]
        top1 = top3[0]
        hit = top1["version"] == version
        top1_hits += hit
        if not hit:
            wrong_version += 1
        share = sum(1 for p in top3 if p["version"] == version) / len(top3)
        top3_share_sum += share
        rows.append((q, version, top1["version"], top1["url"], hit))
    n = len(pairs)
    return {
        "pairs": n,
        "top1_version_hit": top1_hits / n,
        "wrong_version_top1": wrong_version,
        "top3_version_share": top3_share_sum / n,
        "rows": rows,
    }


def main():
    index = TfidfIndex(PAGES)
    boost_cfg = copy.deepcopy(DEFAULT_CONFIG)
    scope_cfg = copy.deepcopy(DEFAULT_CONFIG)
    scope_cfg["search"]["version_aware"]["mode"] = "scope"

    naive = evaluate(lambda q, v: naive_rank(index, q, PAGES))
    boosted = evaluate(lambda q, v: version_aware_rank(index, q, PAGES, v, boost_cfg))
    scoped = evaluate(lambda q, v: version_aware_rank(index, q, PAGES, v, scope_cfg))

    print(f"evaluated {naive['pairs']} (query, browsing-version) pairs\n")
    print(f"{'ranker':<28}{'top1_version_hit':>16}{'wrong_version_top1':>18}{'top3_version_share':>18}")
    for name, m in [("naive (relevance only)", naive),
                    ("version-aware boost x1.75", boosted),
                    ("version-aware scope", scoped)]:
        print(f"{name:<28}{m['top1_version_hit']:>16.3f}{m['wrong_version_top1']:>18d}"
              f"{m['top3_version_share']:>18.3f}")

    print("\nwhere naive puts the wrong version on top (the reported bug):")
    shown = 0
    for q, version, topv, url, hit in naive["rows"]:
        if not hit and shown < 8:
            brow = [u for u in boosted["rows"] if u[0] == q and u[1] == version][0]
            print(f"  q={q!r} browsing={version}: naive top1={topv} {url}")
            print(f"    -> version-aware top1={brow[2]} {brow[3]}")
            shown += 1

    ok = boosted["top1_version_hit"] > naive["top1_version_hit"]
    print(f"\nversion-aware boost beats naive on top1_version_hit: {ok}")
    if not ok:
        print("SANITY GATE FAILED: no improvement demonstrated", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
