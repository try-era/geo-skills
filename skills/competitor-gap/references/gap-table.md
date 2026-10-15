# Gap table and winnability

Use the column names verbatim so tables compare from one run to the next. One row is one
prompt on one engine. Sort by the winnability score, highest first.

## Table template

```markdown
| # | Prompt | Engine | Named brands (in order) | Our position | Competitor position | What was cited | Win |
| ---: | --- | --- | --- | ---: | --- | --- | ---: |
| 1 | best CRM for agencies | Perplexity | Competitor A, Competitor B, Competitor C | — | A: 1 · B: 2 | g2.com/categories/crm · competitor-a.com/agencies | 54 |
| 2 | CRM with WhatsApp | ChatGPT | Competitor A, **Us** | 2 | A: 1 | none shown | 12 |
```

Column rules:

- **Prompt** — the monitored prompt text, unedited. Add the `list_prompts` id in the
  appendix, not in the table.
- **Engine** — ChatGPT, Perplexity, Gemini, Google AI, Claude or Grok.
- **Named brands (in order)** — every brand named in the opened `response_text`, in order
  of first mention. Bold the brand being analysed. Untracked names go in italics.
- **Our position** — the `position` from `list_answers` (1 = first). `—` when absent.
- **Competitor position** — `Name: n` for each tracked competitor named, counting the order
  of mention you read in the opened answer.
- **What was cited** — up to three domains or paths from the answer's `citations`, in the
  order shown. Write `none shown` when the answer carries no citation. Mark the owner:
  plain text for third-party, `(own)` for the brand, `(comp)` for a competitor.
- **Win** — the winnability score below.

Add one line under the table: the number of rows hidden because their score is below 9,
and where to find them (the appendix).

## Winnability heuristic

A ranking aid for choosing where to work first. It is not a forecast of results.

Gate: a row enters the table only when (1) at least one tracked competitor is named in the
opened answer, and (2) the brand is absent, or named later than that competitor.

Score = **R × C × A × S**. Each factor is 1, 2 or 3. The range is 1 to 81.

| Factor | Question | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| **R** run weight | How often is this prompt asked? | Bottom third of the brand's prompts by answers in the window | Middle third | Top third |
| **C** competitor named | How consistently do rivals win it? | A rival is named on one engine only | On two engines | On three or more, or the same rival on every engine that ran it |
| **A** absence | How complete is our absence? | Named, but behind | Absent from some answers of this prompt | Absent from every answer of this prompt in the window |
| **S** source | Is there a third-party source we could also appear on? | Only competitor-owned pages cited, or nothing cited | Third-party sources cited, but generic (news roundups, listicles outside the category) | A third-party page cited that lists or compares products in this category and does not name us |

How to measure the inputs:

- **R** — count the `list_answers` rows for the prompt in the window, rank all prompts by
  that count, and cut the ranking into thirds. State the cut points in Method.
- **C** — count engines (among those that ran the prompt) whose opened answer names a
  tracked competitor.
- **A** — count the answers for the prompt where `mentioned` is false against all answers
  for it.
- **S** — read the `citations` of the opened answers. A page counts as "does not name us"
  only after you have fetched it or the answer text shows the omission; otherwise score 2
  and write "not verified" in the cause line.

Bands (heuristic thresholds; adjust them once and keep them stable between runs):

| Score | Label | What it means |
| ---: | --- | --- |
| 27 and above | Fight now | Asked often, rivals win consistently, and there is a specific page to appear on or answer |
| 9 to 26 | Worth a page | A good page or one placement could move it |
| below 9 | Monitor | Rare prompt, thin evidence or nothing to place against; revisit next window |

Why a product: a 1 on any factor should pull a row down. A rare prompt (R = 1) is a poor
bet even when the gap is total, and a gap with no third-party source (S = 1) can only be
closed with your own page, which is slower and less certain.

## Worked example

Numbers are invented for illustration.

Prompt "best CRM for agencies", Perplexity. It sits in the top third of prompts by answers
(R = 3). Competitors A and B are named on Perplexity, ChatGPT and Gemini (C = 3). The brand
is absent from all 12 answers in the window (A = 3). The answer cites a g2.com category
page and competitor-a.com; the g2 page lists seven tools and does not list the brand
(S = 3). Score 3 × 3 × 3 × 3 = 81, label "Fight now".

Prompt "CRM with WhatsApp", ChatGPT. Bottom third (R = 1), one competitor on one engine
(C = 1), the brand is named second (A = 1), nothing cited (S = 1). Score 1, "Monitor".

## Why-they-win block

One per top gap, at most ten:

```markdown
### P3 · best CRM for agencies · Perplexity · {date}
**Cause:** (b) a third-party list names them, not us
**Said:** "{verbatim fragment, one or two sentences}"
**Cited:** {url} — {what the page is: category page, review, forum thread}
**Sub-queries the engine ran:** {from get_answer search_queries}
**Evidence strength:** {3 absent answers of 3 · page fetched, brand not listed}
**Action:** {one line} → {sibling skill}
**Check in four weeks:** re-read {prompt} on {engine}; a win is {brand named / URL cited}.
```

Cause codes: (a) competitor's own page cited · (b) third-party list or review names them
and not us · (c) sub-queries test criteria our pages do not address · (d) no source cited,
answer came from the model · (e) the engine frames the category in words we do not use ·
"unclear" when the evidence does not decide.

## Cause to action

| Cause | Action | Hand off to |
| --- | --- | --- |
| (a) competitor page cited | Publish a page that answers the same question better: a direct answer first, a comparison table, sourced numbers | `answer-engine-content`; `content-brief` if it belongs in the content plan |
| (b) third-party list cited | Get listed or reviewed on that page; offer data or a product trial | `citation-sources` (outreach brief) |
| (c) criteria not addressed | Measure the demand behind the sub-queries, then cover each criterion on a page | `ai-keyword-research`, then `answer-engine-content` |
| (d) no source cited | Low winnability. Improve the brand's footprint: consistent naming, organisation schema, third-party mentions; re-check in a month | `schema-markup`, `on-page-seo` |
| (e) different framing | Align the page titles and headings with the category words the engine uses | `on-page-seo`, `answer-engine-content` |

## Appendix (practitioner version)

A second table with every gap row below the cut, the prompt ids from `list_prompts`, and
the `answer_id` of each opened answer, so any quote can be re-read with `get_answer`.
