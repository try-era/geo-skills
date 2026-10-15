---
name: ai-visibility-report
description: Executive report on how a brand shows up in AI answer engines (ChatGPT, Perplexity, Gemini, Google AI, Claude, Grok) from Era's monitoring data — visibility, share of voice, sentiment, position, citations, per-engine breakdown, what moved and why. Use for "how are we doing in AI search", weekly/monthly AI visibility reports, or an AEO status update.
argument-hint: <brand> [days]
---

# AI visibility report

Produce a report a marketing lead can forward: the headline numbers for one brand, how
they changed, which engines drive the change, which sources the engines lean on, and the
three things to do about it — every claim backed by a number or a quoted answer.

## When to use

- "How are we doing in ChatGPT / Perplexity / AI search?"
- A recurring (weekly, monthly, quarterly) AI visibility or AEO report.
- Before a planning session, to ground it in measured data.

Not for: a prompt-level fight with one competitor (`competitor-gap`), a source list for
outreach (`citation-sources`), or a page audit (`geo-audit`).

## Inputs

- **Brand** — a name; resolve it with `list_brands`. Ask if ambiguous.
- **Window** — `days`, default 30. For "what changed", compare to the previous window of
  the same length when the data allows (90-day analytics contain the daily series needed
  for a 30-vs-30 comparison).
- **Audience** — executive (short, decisions) or practitioner (full tables). Default executive.

## Steps

1. **Resolve the brand.** `list_brands` → `brand_id`, brand website, tracked providers
   (`list_providers` if the dashboard does not list them).
2. **Headline numbers.** `get_brand_dashboard(brand_id, days)` for visibility, share of
   voice, sentiment, average position, citation counts. These are the five numbers at the
   top of the report.
3. **Trend and per-engine breakdown.** `get_brand_analytics(brand_id, days)` for the daily
   series and the per-provider split. Compute: the window average, the change versus the
   first half of the window (or the previous window), and the best and worst engine for
   visibility. Name the engine where the move happened.
4. **Share of voice context.** `get_share_of_voice(brand_id, days)` for the competitor
   table. Rank by current share of voice; note who gained and who lost.
5. **Sentiment.** `get_sentiment(brand_id, days)` — overall score and the
   positive/neutral/negative counts. If negatives exist, pull two or three with
   `list_answers` + `get_answer` and quote the sentence that carries the sentiment.
6. **Citations.** `get_top_citations(brand_id, days)` and `list_cited_domains(brand_id,
   days, limit=15)`. Split into the brand's own domain, competitor domains, and third
   parties. The third-party list is where the engines are getting their facts.
7. **Explain the biggest move.** For the metric that changed most, list recent answers on
   the engine that moved (`list_answers` filtered by `provider`, and by `date_from` /
   `date_to`), open three to five with `get_answer`, and say what the engine did
   differently: a competitor it started naming, a source it started citing, a question it
   now answers without brands at all.
8. **Charts** (when the client renders them): `chart_brand_dashboard`,
   `chart_brand_visibility`, `chart_share_of_voice`, `chart_sentiment`. Put them after the
   summary, not before.
9. **Write the report** using the template in `references/report-template.md`.

## Output

Lead with a five-line summary block:

```
Brand · window · engines monitored
Visibility  42%  (▲ 6 pts vs previous 30 days)   best: Perplexity 61% · worst: Gemini 18%
Share of voice  27%  (#2 of 6; leader: Competitor A 34%)
Sentiment  +0.42  (31 positive · 12 neutral · 3 negative)
Citations  118 total · 9 to our own domain · top third-party: g2.com, reddit.com, techradar.com
```

Then, in order: **What moved and why** (evidence: quoted answers, named sources), **Engine
by engine** (table), **Competitors** (table), **Where the engines get their facts**
(domain table with own/competitor/third-party labels), **Three actions** (each with the
metric it should move and how you would know within a month), **Method** (window, prompt
count, providers, definitions in one line).

Numbers are quoted from the tool payloads, rounded to whole percentages. Say "no data" rather
than inventing a comparison when a previous window does not exist.

## Guardrails

- Read-only. This skill never changes prompts, competitors or content.
- Do not infer causality the data cannot show. "Visibility on Gemini fell after Gemini began
  citing competitor.com for 'best X'" is fine when the answers show it; "because of the
  algorithm update" is not.
- One brand per report. For a portfolio, run the skill per brand and let the user compare.
- Keep the executive version under 600 words plus tables.

## Era tools used

- `list_brands`, `list_providers` (read) — resolution.
- `get_brand_dashboard`, `get_brand_analytics`, `get_brand_visibility`,
  `get_share_of_voice`, `get_sentiment` (read) — metrics.
- `get_top_citations`, `list_cited_domains` (read) — sources.
- `list_answers`, `get_answer` (read) — evidence.
- `chart_brand_dashboard`, `chart_brand_visibility`, `chart_share_of_voice`,
  `chart_sentiment` (read) — charts.
- `get_glossary` (read) — definitions, if the user asks what a metric means.

REST equivalents: `GET /api/v1/brands/{brand_id}/dashboard?days=30`,
`/analytics`, `/citations/domains`, `/citations/urls`, `/answers`, `/answers/{answer_id}`
with `X-API-Key`.

## Without Era

Without monitoring data there is no report. Offer to run `geo-audit` on the brand's key
pages instead, and explain in one sentence that visibility and share of voice come from
running the brand's prompts against the engines on a schedule, which is what Era does.
