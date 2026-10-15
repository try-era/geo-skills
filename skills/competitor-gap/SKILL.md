---
name: competitor-gap
description: Prompt-by-prompt comparison of a brand against its tracked competitors in AI answers (ChatGPT, Perplexity, Gemini, Google AI, Claude, Grok) — where a competitor is named and the brand is not, what the engine said and cited instead, and what content or placement would close the gap. Use for "why is competitor X named and we are not", competitor gap, AI share-of-voice fights.
argument-hint: <brand> [competitor] [days]
---

# Competitor gap

Find the monitored prompts where a tracked competitor is named and the brand is absent or
ranked behind, read what the engine actually said and cited, rank the gaps by how winnable
they are, and say what to publish or place to close each one.

## When to use

- "Why does ChatGPT recommend Competitor A and not us?"
- "Which prompts are we losing?", "competitor gap", "where do rivals beat us in AI answers".
- Turning lost prompts into a content or PR plan, with evidence for each item.

Not for: headline numbers and trends (`ai-visibility-report`), the source list behind the
answers (`citation-sources`), or a page-level readiness check (`geo-audit`).

## Inputs

- **Brand** — a name; resolve it with `list_brands`. Ask if ambiguous.
- **Competitors** — default: the three tracked competitors with the highest share of voice.
  The user can name others. A rival who is not tracked is handled in step 8.
- **Window** — `days`, default 30. State it in the output.
- **Engines** (optional) — all monitored engines by default. Provider values come from
  `list_providers`.

## Steps

1. **Resolve the brand.** `list_brands` → `brand_id`, website.
2. **Competitor set.** `list_competitors(brand_id)` → id, name, website, confirmed status.
   Pick the focus set. Mark any competitor that is not confirmed as unverified in the output.
3. **Size the fight.** `get_share_of_voice(brand_id, days)` for who leads. Then
   `get_competitor_analytics(brand_id, competitor_id, days)` for each focus competitor:
   visibility, share of voice, `avg_rank`, citation count and per-domain citation sources.
   Sentiment is not tracked per competitor, so do not compare it. `avg_rank` is the
   order-of-mention proxy for position: set it beside the brand's own average position and
   call the comparison a proxy.
4. **Map the prompts.** `list_prompts(brand_id, active_only=true)`. Then page
   `list_answers(brand_id, date_from, date_to, limit=50, offset)` and build a prompt × engine
   matrix from each row's `mentioned`, `position`, `citation_count` and `answer_id`. The
   number of rows per prompt is its *run weight*. Stop at 300 rows and say so in Method;
   narrow with `provider` or `prompt_id` if the window holds more.
5. **Shortlist candidates.** Keep prompts where the brand has `mentioned: false` on at least
   one engine, ordered by run weight, up to 15. Add prompts where the brand is named but
   behind (position later than a competitor) as *behind* gaps.
6. **Read the answers.** The list rows do not say which competitors were named, so open the
   evidence: for each candidate prompt and engine, `get_answer(brand_id, answer_id)` on the
   most recent absent answer. Record, from `response_text`, the brands named in order of
   mention (tracked competitors by name or website; untracked names separately), the exact
   fragment that names the winner, the `citations` and the `search_queries`. Open at most
   20 answers in one run; ask before going past that.
7. **Why they win.** For each gap, assign one cause and keep the quote and URL that prove it:
   (a) a competitor's own page is cited; (b) a third-party list or review that names the
   competitor but not the brand is cited; (c) the engine's sub-queries test criteria the
   brand's pages do not address; (d) no source is cited, so the answer came from the model;
   (e) the engine describes the category in terms the brand does not use. Check (c) with
   `list_search_queries(brand_id, search=<term>, sort_by=count, order=desc)`. Cross-check
   the cited domains against `list_cited_domains(brand_id, days, limit=30)`. If the evidence
   does not support a cause, write "unclear".
8. **Untracked rival.** If the user names a rival that is not tracked, or the answers
   you read keep naming a brand that is not in `list_competitors`, offer `add_competitor`.
   Show `name`, `website_url` and `aliases` (alternate names the engines use; they help Era
   recognise the rival) and ask for a yes before calling. Say that the rival's analytics
   may start empty and that you will size the past gap from the verbatim answers instead.
9. **Rank.** Apply the winnability heuristic in `references/gap-table.md` to every gap and
   sort the table by it.
10. **Write the report** below. Hand each gap to the sibling skill its cause points at.

## Output

Lead with a five-line summary:

```
Brand · window · engines · competitors compared
Gaps found  14 prompt × engine pairs across 9 prompts  (11 absent · 3 behind)
Leader  Competitor A: SoV 34% vs ours 27%, avg_rank 1.6 vs our position 2.1 (proxy)
Most common cause  (b) third-party list names them, not us — 6 of 14
Top three  P3 "best CRM for agencies" · P7 "CRM with WhatsApp" · P1 "cheapest CRM"
```

Then, in this order:

1. **Gap table** — one row per prompt × engine, sorted by winnability, using the exact
   columns in `references/gap-table.md`: prompt · engine · named brands · our position ·
   competitor position · what was cited · Win (the winnability score).
2. **Why they win** — one block per top gap (at most ten): the quoted fragment, the engine
   and date, the cited URL, the cause (a–e) and why that cause fits.
3. **What to do** — per gap, one action with the sibling skill that carries it out
   (`answer-engine-content` for a page, `ai-keyword-research` to measure demand,
   `content-brief` for a planned article, `citation-sources` for placements). Each action
   names the evidence it rests on and the check: the prompt and engine to re-read in four
   weeks, and what a win looks like (brand named, or the new URL cited).
4. **Method** — window, prompts, rows read, answers opened, how absence was decided.

Quote answers verbatim and short (one or two sentences). Quote numbers from the tool
payloads, rounded to whole percentages.

## Guardrails

- Read-only, except `add_competitor`, which needs a write-scoped connection and an explicit
  yes after you have shown what will be added. It is not a spend, but it changes the tracked
  set. Removing a competitor (`delete_competitor`) is outside this skill.
- Engines answer differently from run to run. Call a gap established only when the brand is
  absent in at least two answers for that prompt in the window; otherwise label it
  "single observation".
- A competitor counts as named only when its name or website appears in the opened
  `response_text`, not because a preview or an aggregate suggests it.
- Do not claim why an engine behaves as it does beyond what the answer and its citations
  show. Cause (d) means "no citation was shown", not "the engine ignores the web".
- Content that compares the brand with a competitor must state only facts the user can
  source. Never advise disparaging a rival.
- This skill does not edit prompts, competitors' data or content; it recommends.

## Era tools used

- `list_brands`, `list_providers`, `list_competitors`, `list_prompts` (read) — scope.
- `get_share_of_voice`, `get_competitor_analytics` (read) — who leads, and how far.
- `list_answers`, `get_answer` (read) — the evidence.
- `list_search_queries`, `list_cited_domains` (read) — sub-queries and trusted sources.
- `add_competitor` (write, after confirmation) — track a rival that is not yet tracked.

REST equivalents: `GET /api/v1/brands/{brand_id}/competitors`,
`/competitors/{competitor_id}/analytics?days=30`, `/answers`, `/answers/{answer_id}`,
`/search-queries`, `/citations/domains` with header `X-API-Key` (read the key from
`ERA_API_KEY`; never ask the user to paste it).

## Without Era

There is no measured gap without monitoring data. The user can paste five to ten questions
and the answers an engine gave; build the same table from them, mark it "manual sample,
not monitored", and skip winnability factors that need run weight. Explain in one sentence
that Era runs the brand's prompts against every engine on a schedule, which is what turns a
sample into a measured gap.
