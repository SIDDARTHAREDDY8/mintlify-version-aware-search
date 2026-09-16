"""Rankers: a naive relevance-only ranker (current behavior per discussion #5668)
and a version-aware ranker implementing the three options the discussion asks for:

  1. version-aware ranking  -> mode "boost": results from the browsed version get a
     multiplicative boost (configurable), others are demoted.
  2. project-level config   -> mode "scope": only the browsed version is searched.
     Shipped as a docs.json-shaped config dict so the surface matches the request.
  3. folder-prefix exclusion -> "exclude_prefixes": index-time exclusion independent
     of .mintignore, e.g. ["/4.0/", "/4.7.x/"].

Pure Python, no dependencies.
"""

import math
import re
from collections import Counter

_TOKEN = re.compile(r"[a-z0-9]+")

TITLE_WEIGHT = 3.0


def tokenize(text):
    return _TOKEN.findall(text.lower())


class TfidfIndex:
    def __init__(self, pages):
        self.pages = pages
        self.df = Counter()
        for p in pages:
            toks = set(tokenize(p["title"])) | set(tokenize(p["body"]))
            self.df.update(toks)
        self.n = len(pages)

    def idf(self, tok):
        return math.log((1 + self.n) / (1 + self.df.get(tok, 0))) + 1.0

    def score(self, query, page):
        qtoks = tokenize(query)
        if not qtoks:
            return 0.0
        title_toks = Counter(tokenize(page["title"]))
        body_toks = Counter(tokenize(page["body"]))
        s = 0.0
        for t in set(qtoks):
            tf = title_toks.get(t, 0) * TITLE_WEIGHT + body_toks.get(t, 0)
            if tf > 0:
                s += (1.0 + math.log(tf)) * self.idf(t) * qtoks.count(t)
        return s


def naive_rank(index, query, pages):
    """Relevance only — the behavior discussion #5668 reports: no version awareness."""
    scored = [(index.score(query, p), p) for p in pages]
    scored.sort(key=lambda x: (-x[0], x[1]["url"]))
    return [p for _, p in scored]


DEFAULT_CONFIG = {
    "search": {
        "version_aware": {
            "mode": "boost",        # "boost" | "scope" | "off"
            "boost": 1.75,          # multiplicative boost for the browsed version
            "exclude_prefixes": [],  # e.g. ["/4.0/"] — folder-prefix exclusion list
        }
    },
}


def _apply_exclusions(pages, exclude_prefixes):
    if not exclude_prefixes:
        return pages
    return [p for p in pages
            if not any(p["url"].startswith(px) for px in exclude_prefixes)]


def version_aware_rank(index, query, pages, active_version, config=None):
    """Version-aware ranking per the discussion's requested options."""
    cfg = (config or DEFAULT_CONFIG)["search"]["version_aware"]
    pages = _apply_exclusions(pages, cfg.get("exclude_prefixes", []))

    if cfg.get("mode") == "scope":
        pages = [p for p in pages if p["version"] == active_version]

    boost = float(cfg.get("boost", 1.75))
    scored = []
    for p in pages:
        s = index.score(query, p)
        if cfg.get("mode") != "off" and p["version"] == active_version:
            s *= boost
        scored.append((s, p))
    scored.sort(key=lambda x: (-x[0], x[1]["url"]))
    return [p for _, p in scored]
