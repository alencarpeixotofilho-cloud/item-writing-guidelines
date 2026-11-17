"""Automated checks for common item-writing flaws.

Each rule returns zero or more :class:`Finding`. Severity:

* ``error``   — the item is structurally broken (e.g. key not among options)
* ``warning`` — a well-documented technical flaw (cueing, negative lead-in, ...)
* ``info``    — a style suggestion worth a human look

The checks are heuristics. They catch the *mechanical* flaws reviewers often
miss; they do not judge clinical accuracy or relevance, which always require
a content expert.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from statistics import mean

from .parser import Item


@dataclass
class Finding:
    rule: str
    severity: str
    message: str


ABSOLUTES = r"\b(always|never|only|all|none|every|completely|must)\b"
VAGUE = r"\b(frequently|usually|often|rarely|sometimes|commonly|occasionally|may)\b"
NEGATIVE = r"\b(not|except|false|incorrect|least likely|untrue)\b"
STOPWORDS = set("""a an the of and or to in on with for by at from is are was were be been
which what who whom this that these those most likely following patient his her their its
as it into over after before during than then there here has have had not no yes""".split())


def _words(s: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z\-]+", s.lower())


def rule_structure(item: Item):
    if len(item.options) < 3:
        yield Finding("STRUCTURE", "error", f"only {len(item.options)} options parsed")
    if item.key not in item.options:
        yield Finding("KEY", "error", f"key '{item.key}' is not one of the options")
    if not item.lead_in.strip():
        yield Finding("LEAD_IN_MISSING", "error", "lead-in is empty")
    texts = [t.strip().lower() for t in item.options.values()]
    if len(set(texts)) < len(texts):
        yield Finding("DUPLICATE_OPTIONS", "error", "two or more options are identical")


def rule_negative_lead_in(item: Item):
    if re.search(NEGATIVE, item.lead_in, flags=re.I):
        yield Finding("NEGATIVE_LEAD_IN", "warning",
                      "negatively phrased lead-in (NOT/EXCEPT); rewrite as a positive question")


def rule_closed_question(item: Item):
    if item.lead_in.strip() and not item.lead_in.strip().endswith("?"):
        yield Finding("OPEN_LEAD_IN", "info",
                      "lead-in is not a direct question; prefer a question answerable "
                      "with the options covered")


def rule_all_none(item: Item):
    for k, t in item.options.items():
        if re.search(r"\b(all|none|both) of the (above|options|alternatives)\b", t, re.I):
            yield Finding("ALL_NONE_OF_THE_ABOVE", "warning", f"option {k} uses 'all/none of the above'")


def rule_absolute_terms(item: Item):
    for k, t in item.options.items():
        m = re.search(ABSOLUTES, t, re.I)
        if m:
            yield Finding("ABSOLUTE_TERM", "warning",
                          f"option {k} contains the absolute term '{m.group(0)}' "
                          "(test-wise examinees eliminate it)")


def rule_vague_terms(item: Item):
    for k, t in item.options.items():
        m = re.search(VAGUE, t, re.I)
        if m:
            yield Finding("VAGUE_FREQUENCY", "info", f"option {k} uses the vague term '{m.group(0)}'")


def rule_longest_key(item: Item, ratio: float = 1.4):
    if item.key not in item.options or len(item.options) < 3:
        return
    lens = {k: len(v) for k, v in item.options.items()}
    others = [v for k, v in lens.items() if k != item.key]
    if lens[item.key] >= ratio * mean(others) and lens[item.key] == max(lens.values()):
        yield Finding("LONGEST_KEY", "warning",
                      "the key is clearly the longest option (length cue)")


def rule_word_repeat(item: Item):
    """Clang association: a distinctive word from the stem reappears only in the key."""
    if item.key not in item.options:
        return
    stem_words = {w for w in _words(item.stem + " " + item.lead_in) if w not in STOPWORDS and len(w) > 4}
    key_words = set(_words(item.options[item.key])) & stem_words
    other_words = set()
    for k, t in item.options.items():
        if k != item.key:
            other_words |= set(_words(t))
    cue = sorted(key_words - other_words)
    if cue:
        yield Finding("WORD_REPEAT", "info",
                      f"word(s) from the stem appear only in the key: {', '.join(cue[:3])}")


def rule_heterogeneous_length(item: Item):
    lens = [len(v) for v in item.options.values()]
    if len(lens) >= 3 and min(lens) > 0 and max(lens) / min(lens) > 4:
        yield Finding("HETEROGENEOUS_OPTIONS", "info",
                      "options differ a lot in length; keep them homogeneous")


def rule_numeric_order(item: Item):
    nums = []
    for t in item.options.values():
        m = re.match(r"^\s*([-+]?\d+(?:[.,]\d+)?)", t)
        if not m:
            return
        nums.append(float(m.group(1).replace(",", ".")))
    if nums != sorted(nums) and nums != sorted(nums, reverse=True):
        yield Finding("NUMERIC_ORDER", "info", "numeric options are not in logical order")


def rule_grammatical_cue(item: Item):
    lead = item.lead_in.strip().lower()
    if lead.endswith(" an"):
        bad = [k for k, t in item.options.items() if t[:1].lower() not in "aeiou"]
        if bad:
            yield Finding("GRAMMATICAL_CUE", "warning",
                          f"lead-in ends with 'an' but options {', '.join(bad)} start with a consonant")
    if lead.endswith(" a"):
        bad = [k for k, t in item.options.items() if t[:1].lower() in "aeiou"]
        if bad:
            yield Finding("GRAMMATICAL_CUE", "warning",
                          f"lead-in ends with 'a' but options {', '.join(bad)} start with a vowel")


def rule_short_stem(item: Item, min_words: int = 25):
    n = len(_words(item.stem))
    if n < min_words:
        yield Finding("SHORT_STEM", "info",
                      f"stem has {n} words; application-level items usually need a vignette")


ALL_RULES = [
    rule_structure, rule_negative_lead_in, rule_closed_question, rule_all_none,
    rule_absolute_terms, rule_vague_terms, rule_longest_key, rule_word_repeat,
    rule_heterogeneous_length, rule_numeric_order, rule_grammatical_cue, rule_short_stem,
]


def check(item: Item) -> list[Finding]:
    out: list[Finding] = []
    for rule in ALL_RULES:
        out.extend(rule(item))
    return out
