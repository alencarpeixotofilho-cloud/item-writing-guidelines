# Item-Writing Guidelines & Review Checklist

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Docs](https://img.shields.io/badge/guide-6%20chapters-8250df?style=flat-square)
![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)

> A practical, evidence-based guide to writing and reviewing multiple-choice
> items — plus **`itemcheck`**, a linter that catches the mechanical flaws
> human reviewers often miss.

Poorly written items measure test-taking skill instead of knowledge. The
research literature is consistent: technical flaws such as negative lead-ins,
"all of the above" and length cues change item difficulty and penalize the
examinees we most want to identify. This repository brings the established
recommendations together in a short guide, a 16-criterion review checklist and
an automated checker.

## 📖 The guide

| Chapter | Topic |
|---|---|
| [1. Principles](guide/01-principles.md) | One important idea per item, application over recall, cover-the-options rule, construct-irrelevant variance |
| [2. The stem](guide/02-vignette.md) | Vignette structure, data vs interpretation, window dressing |
| [3. The lead-in](guide/03-lead-in.md) | Closed, positive questions; rewriting EXCEPT items |
| [4. The options](guide/04-options.md) | One best answer, plausible distractors, homogeneity |
| [5. Technical flaws](guide/05-technical-flaws.md) | Catalog of flaws that help test-wise examinees or hurt knowledgeable ones |
| [6. Review workflow](guide/06-review-process.md) | Self-check → content review → technical review → item analysis |

📋 **[Review checklist](checklist/review-checklist.md)** — 16 criteria grouped as
critical, stem, options and language, with a decision box.

## 🤖 `itemcheck` — automated flaw detection

Write items in a simple Markdown format:

```markdown
---
id: GOOD-001
domain: Internal Medicine
---
## Stem
A 58-year-old man comes to the emergency department 40 minutes after ...
## Lead-in
Occlusion of which of the following arteries is the most likely cause of these findings?
## Options
A. Left anterior descending artery
B. Left circumflex artery
...
## Key
D
```

Then run:

```bash
pip install -e .
python -m itemcheck examples/
```

```text
FLAWED-001  (examples/flawed_items.md)
  ⚠ NEGATIVE_LEAD_IN       negatively phrased lead-in (NOT/EXCEPT); rewrite as a positive question
  ⚠ ALL_NONE_OF_THE_ABOVE  option E uses 'all/none of the above'
  ⚠ ABSOLUTE_TERM          option D contains the absolute term 'always'
  ⚠ LONGEST_KEY            the key is clearly the longest option (length cue)
  ℹ HETEROGENEOUS_OPTIONS  options differ a lot in length; keep them homogeneous
  ℹ SHORT_STEM             stem has 8 words; application-level items usually need a vignette

FLAWED-002  (examples/flawed_items.md)
  ⚠ GRAMMATICAL_CUE        lead-in ends with 'a' but options C start with a vowel

GOOD-001  (examples/good_items.md)
  ✔ no issues found
```

### Rules

| Rule | Severity | What it catches |
|---|---|---|
| `STRUCTURE`, `KEY`, `DUPLICATE_OPTIONS`, `LEAD_IN_MISSING` | error | Broken items |
| `NEGATIVE_LEAD_IN` | warning | NOT / EXCEPT / FALSE / least likely |
| `ALL_NONE_OF_THE_ABOVE` | warning | "All/none of the above" options |
| `ABSOLUTE_TERM` | warning | always, never, only, all, none … |
| `LONGEST_KEY` | warning | Key ≥ 1.4× the mean distractor length |
| `GRAMMATICAL_CUE` | warning | a/an agreement between lead-in and options |
| `OPEN_LEAD_IN` | info | Lead-in that is not a direct question |
| `WORD_REPEAT` | info | Distinctive stem word appearing only in the key |
| `VAGUE_FREQUENCY` | info | often, usually, rarely … |
| `HETEROGENEOUS_OPTIONS` | info | Options differing > 4× in length |
| `NUMERIC_ORDER` | info | Numeric options not sorted |
| `SHORT_STEM` | info | Stem under 25 words (no vignette) |

Options: `--json` for machine-readable output (e.g. to feed a review
dashboard) and `--fail-on {error,warning,never}` to use it in CI so that
flawed items cannot be merged into an item bank.

> `itemcheck` checks **form**, not **content**. Clinical accuracy, relevance and
> the uniqueness of the best answer always require a content expert.

## 🗂️ Repository structure

```text
item-writing-guidelines/
├── guide/        # 6 chapters (Markdown)
├── checklist/    # printable review checklist
├── examples/     # fictitious good and flawed items
├── itemcheck/    # parser, rules, CLI
└── tests/
```

## 🔒 Data & privacy

All items in this repository are **fictitious and written for demonstration**.
No real exam content, item bank or reviewer data is included.

## 📚 References

* Haladyna, T. M., Downing, S. M., & Rodriguez, M. C. (2002). A review of multiple-choice item-writing guidelines for classroom assessment. *Applied Measurement in Education, 15*(3), 309–333.
* Downing, S. M. (2005). The effects of violating standard item writing principles on tests and students. *Advances in Health Sciences Education, 10*(2), 133–143.
* Tarrant, M., & Ware, J. (2008). Impact of item-writing flaws in multiple-choice questions on student achievement in high-stakes nursing assessments. *Medical Education, 42*(2), 198–206.
* Paniagua, M. A., & Swygert, K. A. (Eds.). (2016). *Constructing Written Test Questions for the Basic and Clinical Sciences* (4th ed.). National Board of Medical Examiners.

## 📄 License

Released under the MIT License. See [`LICENSE`](LICENSE).
