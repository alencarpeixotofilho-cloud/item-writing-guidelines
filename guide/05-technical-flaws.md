# 5. Catalog of technical flaws

Flaws marked with 🤖 are detected automatically by `itemcheck`.

## 5.1 Flaws that help test-wise examinees

| Flaw | Description | Fix |
|---|---|---|
| 🤖 Longest key | The key is noticeably longer or more qualified than the distractors | Balance option length and detail |
| 🤖 Grammatical cue | Article or number in the lead-in agrees only with some options | Use a closed question |
| 🤖 Word repeat (clang) | A distinctive word from the stem appears only in the key | Rephrase the key or add the word to distractors |
| 🤖 Absolute terms | *always / never / only* in distractors | Remove absolutes |
| Convergence | The key shares the most elements with other options | Vary option components |
| Logical cue | A subset of options is mutually exclusive, so one must be right | Rewrite the set |

## 5.2 Flaws that hurt knowledgeable examinees

| Flaw | Description | Fix |
|---|---|---|
| 🤖 Negative lead-in | NOT / EXCEPT / FALSE | Phrase positively |
| 🤖 All / none of the above | Rewards partial knowledge | Replace with a plausible distractor |
| 🤖 Vague frequency terms | *often, usually, rarely* | Use precise data or remove |
| 🤖 Numeric options out of order | Increases reading load and errors | Sort ascending |
| 🤖 Heterogeneous options | Mixed length or category | Make options parallel |
| Tricky / ambiguous stem | Information missing or contradictory | Peer review, cover-the-options test |
| Unnecessary complexity | Long words, double negatives, window dressing | Simplify |

## 5.3 Structural errors

| Flaw | Detection |
|---|---|
| 🤖 Key not among the options | error |
| 🤖 Duplicate options | error |
| 🤖 Missing lead-in | error |
| 🤖 Fewer than three options | error |

## 5.4 Example of a heavily flawed item

```text
Deep vein thrombosis has several well-known risk factors.
All of the following are risk factors for deep vein thrombosis EXCEPT:
A. Recent major surgery
B. Active cancer
C. Combined oral contraceptive use
D. Regular moderate physical activity, which is always protective because it
   reduces venous stasis in the lower limbs                      <- key
E. All of the above
```

`itemcheck` reports: negative lead-in, *all of the above*, absolute term,
longest key, heterogeneous options and the lack of a clinical vignette.
