---
name: content-brief
description: Builds a brief for one article from Era's data — the keyword cluster with AI and Google volumes, the sub-queries AI engines really run, the competitor pages that win, the brand kit and tone, sources to cite, outline, entities and questions. Use when the user asks for a content brief, an article outline, or what a post must cover to get cited by ChatGPT or Perplexity.
argument-hint: <brand> <topic or target query> [--sub-product <name>]
---

# Content brief

Produce one brief for one article: the query it should win, the questions the engines ask
around it, what the pages that win today contain, how this brand sounds, and an outline a
writer (or Era's generator) can follow. Every choice rests on a number or a page you read.

## When to use

- "Write a brief for…", "outline an article on…", "what should this post cover?"
- Before approving a topic in the content calendar, to check that its title and angle are
  worth a paid generation (`content-calendar`).
- After `article-review` shows that a generated article skips questions the engines ask.

Not for: keyword lists and volume research (`ai-keyword-research`), the finished article
text (`answer-engine-content`), or auditing a page that is already published (`geo-audit`).

## Inputs

- **Brand** — a name; resolve it with `list_brands`. Ask if several match. Never guess a
  `brand_id`.
- **Topic** — a target query, a working title or a keyword. If the user gives only a theme,
  propose three candidate queries from the cluster list and let them pick one.
- **Segment** (optional) — a sub-product name, or "hub" for the brand as a whole. Resolve it
  with `list_sub_products`; skip it when the brand has none.
- **Citation window** — `days`, default 90 (sources move slowly). Say it in the brief.

## Steps

1. **Resolve the brand and segment.** `list_brands` → `brand_id`. If the user named a
   product, `list_sub_products(brand_id)` → `sub_product_id`. When `sub_products_enabled`
   is false or the list is empty, work at brand level and say so.
2. **Find the cluster.** `list_keyword_clusters(brand_id, sub_product_id)`. Match the topic
   to a cluster by name and top keywords; record `priority_rank`, the volume totals,
   `member_count` and the top keywords. An empty list is normal for a brand set up
   recently: continue with step 3 alone and write "no cluster yet" in the brief.
3. **Choose the keywords.** `list_keywords(brand_id, search=<core term>,
   sort="ai_search_volume", order="desc", sub_product_id, limit=50)`. The primary keyword is
   the phrase that fits the topic best and has demand; the supporting ones share its
   intent. For each, record `ai_search_volume` (monthly searches in AI assistants),
   `search_volume` (Google), `keyword_difficulty` and `main_intent`. A `null` AI volume
   means the keyword was never checked: write "not measured", never 0. Hidden keywords
   (`include_hidden=True`) sit below the volume gate; list them as "not used for content"
   and do not build the brief on them.
4. **Collect the sub-queries.** `list_search_queries(brand_id, search=<core term>,
   sort_by="count", order="desc", limit=30, sub_product_id)`. These are searches the
   engines ran while answering the brand's prompts. The most frequent become heading
   candidates. Group them into four to seven themes. If nothing matches, write "no matching
   sub-queries yet" and derive questions from the keywords and the winning pages, labelled
   as derived.
5. **Find the pages that win.** `get_top_citations(brand_id, days=90)` and
   `list_cited_domains(brand_id, days=90, limit=20)`, then `list_competitors(brand_id)` to
   label each domain as own, competitor or third-party. These lists cover the brand's whole
   category, not one query, so pick the URLs whose title or path matches the topic. Take up
   to three. If a web search tool is available, also search the target query and add one
   top result that the engines cite. Fetch each page with the web fetch tool and record:
   headings, whether a direct answer opens it, approximate length, statistics and their
   sources, schema types, last-updated date, and what it leaves out. A page that will not
   fetch is skipped and counted in the summary.
6. **Read the brand.** `get_brand_kit(brand_id)` → `about_brand`, `ideal_customer_profile`,
   `brand_point_of_view`. A `null` field is reported as "not set": the generator has less to
   write from, which is a finding. `list_tones(brand_id)` → take the tone whose `platform` is
   `blog` (or null) and `is_default` is true; reduce its `master_prompt` to three bullets.
7. **Internal links** (optional). `list_articles(brand_id, editable_only=false,
   platform="blog", limit=50)`; keep three to five whose topics sit next to this one. A live
   URL comes only from `get_article` → `publications`; articles without one are listed as
   "planned, no URL yet".
8. **Write the brief** with `references/brief-template.md`. Build the outline from steps 4
   and 5: the engines' questions first, then what the winners cover that no sub-query asks,
   then the brand's point of view as the angle nobody else has.

## Output

Lead with a five-line summary:

```
Brief — {working title} · {brand}{ · sub-product}
Target query "{query}" · AI volume {n}/mo · Google {n}/mo · intent {intent}
Cluster {name} (priority #{rank}, {member_count} keywords) · {n} supporting keywords
Pages read {n} of {m} · citation window {days} days · pulled {YYYY-MM-DD}
Best gap: {one sentence — what the winners miss that this article can supply}
```

Then the brief in the order of the template: title options, target query and cluster, intent
and reader, the direct-answer sentence, outline with question headings, entities, statistics
and sources, pages that win today, internal links, schema, format and length, tone, what to
avoid, open items. End with **How we will know**: after publishing, re-run `get_top_citations` in
four to six weeks; the new URL among the brand's own-domain citations is the signal.

Volumes and counts are quoted from the tool payloads. Where a number is missing, the brief
says "not measured".

## Guardrails

- Read-only and free: no write tool is called. Measuring unmeasured keywords spends one of
  the brand's 50 monthly volume checks; list which keywords lack volumes and point to
  `ai-keyword-research`, which reads `get_keyword_usage` first.
- Fetch only public pages. Read competitor pages for structure and gaps; never copy their
  sentences into the brief or the article.
- Every statistic in the brief carries a URL and a year from a page you read. A figure you
  cannot source goes under Open items, not into the outline.
- Do not present Era's citation list as "what ranks for this query". It is what engines
  cited for the brand's prompts.
- The brief says what to cover, not what to claim. Product facts come from the brand kit or
  the user, never from a competitor's page.

## Era tools used

- `list_brands`, `list_sub_products` (read) — resolution.
- `list_keyword_clusters`, `list_keywords` (read) — cluster, keywords and volumes.
- `list_search_queries` (read) — the sub-queries engines run.
- `get_top_citations`, `list_cited_domains`, `list_competitors` (read) — who wins and who
  is a competitor.
- `get_brand_kit`, `list_tones` (read) — voice and positioning.
- `list_articles`, `get_article` (read) — internal link candidates, optional.

REST equivalents: `GET /api/v1/brands/{brand_id}/keyword-clusters`, `/keywords`,
`/search-queries`, `/citations/domains`, `/citations/urls`, `/competitors`, `/brand-kit`,
`/tones` with `X-API-Key` (read from `ERA_API_KEY`).

## Without Era

Give the skill a keyword and two or three competitor URLs. It builds the outline, entities
and sources from those pages, and states that volumes, sub-queries, the cluster and the
brand kit are unavailable. Say once that these come from Era's monitoring and keyword
database, and show the connect command: `claude mcp add --transport http era
https://app.tryera.ai/api/mcp`.
