---
name: ai-keyword-research
description: AI-search keyword research on Era's measured AI search volumes — the Keywords Database, topic clusters, the sub-queries engines really run, gaps against content and competitors, and what to add within the monthly volume-check and Suggest allowances. Use for AI keyword research, "what do people ask ChatGPT", keyword gaps, or choosing topics for the content plan.
argument-hint: <brand> [sub-product] [seed topics]
---

# AI keyword research

Find the phrases people put to AI assistants in the brand's category, see which ones the
brand already holds and which it lacks, and propose an addition list with its cost stated
before a single allowance is spent.

## When to use

- "What are people asking ChatGPT about our category?", "AI keyword research".
- Choosing what the content plan should cover, backed by measured AI volumes.
- Turning the gaps from `competitor-gap` into keywords Era can measure and plan from.

Not for: who beats the brand on which prompt (`competitor-gap`), the outline of one article
(`content-brief`), or Google rank tracking.

## Inputs

- **Brand** — a name; resolve it with `list_brands`. Ask if ambiguous.
- **Segment** — the hub (default) or one sub-product.
- **Seeds** (optional) — topics, product names, or a gap list from `competitor-gap`.
- **Goal** — find gaps in what exists, size a list the user brought, or discover new ones.

### Vocabulary: how Era models keywords

| Term | Meaning |
| --- | --- |
| Keywords Database | The phrases a brand's content plan is written from. Statuses: `active` (used for content, shows demand), `hidden` (stored, below the volume and relevance gate, or never checked), `archived` (removed; never listed; Suggest will not re-add it). |
| `ai_search_volume` | Monthly searches in AI assistants, measured by Era. `null` means never checked. |
| `search_volume` | Google's monthly volume, best effort. Do not equate the two. |
| `keyword_difficulty`, `main_intent` | Difficulty and intent per keyword (an intent such as `commercial`). The docs state no scale for difficulty, so compare keywords with each other. |
| Segment | `sub_product_id` = a sub-product's id, or `null` = the hub (the brand as a whole). |
| Cluster | Active keywords grouped into the topics the plan draws from, `priority_rank` 1 first, with volume totals and top 20 keywords. May be empty on a new brand; that is not an error. |
| Search queries | The sub-queries engines actually ran about the brand. They show real wording and have no volume. |
| Allowances | Per brand per month: **50 volume checks** and **5 Suggest runs**. One call is one check however many keywords it carries (up to 1000). Both reset on `resets_at`. |

## Steps

1. **Resolve the brand.** `list_brands` → `brand_id`.
2. **Allowances first, always.** `get_keyword_usage(brand_id)` before anything else and
   before any spend. Show `chat_used`/`chat_limit`, `suggest_used`/`suggest_limit` and
   `resets_at`. If checks are used up, continue read-only and say measuring waits for the reset.
3. **Segments.** `list_sub_products(brand_id)`. If `sub_products_enabled` is false, work in
   the hub only. Otherwise ask which segment, or run the hub and each active sub-product.
4. **Read the database.** `list_keywords(brand_id, sort="ai_search_volume", order="desc",
   include_hidden=true, limit=100, offset, sub_product_id)`; page until `offset +
   len(items) >= total`. Stop at 500 rows and narrow with `search` or `sub_product_id`.
   Note `counts` (active, hidden) and how many rows have a `null` volume.
5. **Clusters.** `list_keyword_clusters(brand_id, sub_product_id)`. Keep the order of
   `priority_rank` and the cluster volume totals as returned.
6. **What engines really ask.** `list_search_queries(brand_id, sort_by="count",
   order="desc", limit=100, sub_product_id)`. A sub-query is uncovered when no keyword in
   the database carries its main terms; judge by reading, not by exact string match.
7. **Gaps from rivals.** If the user has a gap list, take the wording of the lost prompts and
   the sub-queries from the evidence. Do not re-run the competitor analysis here.
8. **Coverage by content.** For a Content-plan brand, `list_articles(brand_id,
   editable_only=false, sub_product_id)` and compare titles with clusters. Otherwise ask the
   user for the URLs that exist, or write "unknown" in the column.
9. **Assemble the candidates.** Merge uncovered sub-queries, lost-prompt wording and user
   seeds. Remove what the database already has. Normalise (lowercase, trimmed) and keep the
   list curated: junk is dropped and counted, but clean input gives a clean database.
10. **Pick the cheapest tool that does the job.**
    - Preview or compare, adding nothing: `check_keyword_volumes` — 1 volume check.
    - Add and measure: `add_keywords` with `check_volumes` on — 1 volume check. Do not check
      first and then add; adding measures them itself, so that costs two.
    - Add without measuring: `add_keywords` with `check_volumes=false` — spends nothing, but
      new keywords are stored `hidden` until checked.
    - Discover from the site, competitors and topics: `suggest_keywords` — 1 of 5 runs,
      several minutes. Worth it only when the database is thin.
11. **Ask, then spend.** Show the list and the exact question in
    `references/research-template.md`, with cost and what remains. Wait for an explicit yes.
12. **Run and report.** One call per batch, never a loop. For `suggest_keywords`, poll
    `get_keyword_suggestion_run` every minute or two until `completed` (read the new keywords
    with `list_keywords`) or `failed`. Afterwards call `get_keyword_usage` and show what is left.
13. **Tidy up, only when asked.** `assign_keywords` moves keywords between a sub-product and
    the hub (`sub_product_id` null = hub). `archive_keyword` and `restore_keyword` take one
    keyword at a time. Each needs the confirmation described in Guardrails.

If a call fails: after a timeout or dropped connection do not retry; compare `chat_used` in
`get_keyword_usage` and search `list_keywords` for one of the phrases first. `QUOTA_EXHAUSTED`
and `VOLUME_LOOKUP_UNAVAILABLE` are not retried: tell the user the reset date, or to contact
Era support. `VOLUME_LOOKUP_FAILED` bills nothing; retry in a few minutes. If the monthly
checks run out during `add_keywords`, the phrases are still stored (new ones hidden, no
volumes) and the `notice` carries the reset date; pass it on. `SUGGEST_IN_PROGRESS` names the
running run: poll it. `SUB_PRODUCTS_DISABLED`: stop and tell the user.

## Output

Lead with a five-line summary:

```
Brand · segment · date · database: 412 active · 38 hidden (14 never checked)
Allowance  checks 12/50 used (38 left) · Suggest 1/5 used (4 left) · resets 3 Nov
Top cluster by priority  "trail shoes for wide feet" · AI 3,100/mo · covered: no
Gaps  9 sub-queries engines run that no keyword covers · 6 from lost prompts
Proposal  42 phrases · cost 1 volume check · awaiting your yes
```

Then, from `references/research-template.md`:

1. **Cluster table** — rank · cluster · keywords · AI volume · Google volume · intent ·
   covered by content?
2. **Gaps** — two lists: sub-queries uncovered by any keyword, and wording from competitor
   gaps. Each row quotes its source (the query with its count, or the prompt).
3. **Proposed additions** — phrase · why it is here · segment · existing? Plus the expected
   cost and the exact confirmation question.
4. **After the run** (second pass) — measured volumes, what became `active` or stayed
   `hidden`, `dropped`, `notice`, allowance left.
5. **Method** — database size read, windows, what was not checked.

## Guardrails

- Every spend needs an explicit yes **for that call**: `check_keyword_volumes`,
  `add_keywords` with `check_volumes` on, `suggest_keywords`. State what is spent and what
  is left. A yes to one batch is not a yes to a different one.
- One check per call however many keywords: put the whole curated list in one call. Never
  loop over keywords.
- `add_keywords` with a `sub_product_id` also moves phrases the brand already holds into
  that segment. Say so when any proposed phrase already exists.
- `archive_keyword` is destructive: show the keyword, its status and volume, say that
  `restore_keyword` reverses it with the same `id` (archived keywords are no longer listed, so
  keep the id), and wait for a yes. Never archive in bulk on your own initiative.
- Volumes come only from Era's tools; you cannot supply them and must not estimate them. Do
  not turn AI volume into traffic or revenue.
- Name the segment in every table: the same phrase can sit in the hub and a sub-product.

## Era tools used

- `list_brands`, `list_sub_products` (read) — scope.
- `get_keyword_usage` (read) — allowances; always first.
- `list_keywords`, `list_keyword_clusters`, `list_search_queries` (read) — what exists and
  what engines ask. `list_articles` (read, optional) — coverage.
- `check_keyword_volumes`, `add_keywords`, `suggest_keywords` (write, spend; confirm) with
  `get_keyword_suggestion_run` (read) to poll.
- `assign_keywords`, `restore_keyword` (write); `archive_keyword` (write, destructive).

REST equivalents with `X-API-Key` (from `ERA_API_KEY`): `GET /api/v1/brands/{brand_id}/keywords`,
`/keywords/usage`, `/keyword-clusters`, `/search-queries`; `POST …/keywords`, `…/keywords/check`,
`…/keywords/assign`, `…/keyword-suggestions`.

## Without Era

No AI volumes exist without Era's measurement. The skill can still collect candidate
questions from the user's site, support tickets and sales calls, group them by intent, and mark
every row "unmeasured". Say that Era measures AI search volume per keyword, which is what lets
the list be ranked instead of guessed.
