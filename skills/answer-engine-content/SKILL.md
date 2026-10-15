---
name: answer-engine-content
description: Write or rewrite a page so AI answer engines (ChatGPT, Perplexity, Gemini, Google AI, Claude) can lift it into an answer — direct answer first, question-shaped headings, sourced statistics, quotable claims, tables, FAQ, visible author and date. Uses the Era brand kit and tone of voice when connected. Use for "make this page citable", GEO copywriting, or rewriting content for AI search.
argument-hint: <topic or url> [--brand <name>] [--rewrite]
---

# Answer-engine content

Produce copy built from units an engine can extract, attribute and trust: a direct answer,
headings that match the questions people ask, claims with named sources, and structure a
parser can read. New page or rewrite, with a note on why each block is there.

## When to use

- "Write a page that ChatGPT / Perplexity will cite for {question}."
- A page scored low on answer shape or citability in `geo-audit`.
- A gap from `competitor-gap` that needs a page of its own.

Not for: scoring a page (`geo-audit`), JSON-LD (`schema-markup`), title, meta and internal
links (`on-page-seo`), a planned Era article (`content-brief`, then `article-review`).

## Inputs

- **Target query** — the question this page should be the answer to. For a rewrite, derive it
  from the H1 and say so.
- **Page** — new, or a rewrite (a URL to fetch, or pasted text).
- **Page type** — guide, comparison, product or landing, glossary, how-to, FAQ.
- **Facts and sources** — what the user can stand behind: numbers with source and date,
  product facts, quotes, author name and credentials. This skill never supplies them itself.
- **Brand** (optional, Era) — with `--brand`, pull the brand kit and tone of voice.

## Steps

1. **Take inventory.** List the facts the user provided, each with its source and date, plus
   the author and the last-reviewed date. Whatever is missing becomes `[SOURCE NEEDED]` or
   `[FACT NEEDED]` in the draft. Ask once for the highest-value gaps: one sourced number, the
   author, the date.
2. **Read the current page** (rewrite only). Extract the H1, the first paragraph, the
   headings, every claim and number, the tables and lists, the author and the dates. Keep
   all facts, links and names. If the body holds `<IMAGE_INFOGRAPHICS_N>…</IMAGE_INFOGRAPHICS_N>`
   markers (an Era article), keep every one in place.
3. **Era context** (optional, when connected and a brand is given). `list_brands` →
   `brand_id`. `get_brand_kit` for `about_brand`, `ideal_customer_profile` and
   `brand_point_of_view` (each may be `null`). `list_tones` for the brand's default tone and
   its `master_prompt`. `list_keyword_clusters` and `list_keywords(search=<topic>)` for target
   phrases and their `ai_search_volume`. `list_search_queries(search=<topic>, sort_by="count",
   order="desc")` for the exact sub-queries engines run. `list_cited_domains` for the domains
   the engines already cite in the category: candidates for outbound references, used only
   where the source really supports the sentence.
4. **Map the questions.** Turn the target query and the sub-queries into four to eight
   questions in reading order: the answer itself, the definition, how or why, the
   comparison, cost and limits, and the adjacent questions for the FAQ.
5. **Draft block by block** with `references/page-skeleton.md`, applying the patterns in
   `references/geo-writing-patterns.md`. The order of the page is the order of the questions.
6. **Check the draft** against the pattern checklist at the end of
   `references/geo-writing-patterns.md`. Every number has a source and a date, every name is
   written one way throughout, and every claim is one the user can defend.
7. **Write the output** below and name the hand-offs.

## Output

Lead with a five-line summary:

```
Page · target query · mode (new / rewrite) · words before → after
Direct answer  in the first two sentences (was: paragraph 4)
Evidence  6 statistics with source and date · 3 marked [SOURCE NEEDED]
Structure  9 question headings · 1 comparison table · 1 step list · 6-question FAQ
Hand-offs  schema-markup (Article, FAQPage) · on-page-seo (title, meta, internal links)
```

Then:

1. **The draft**, in Markdown, ready to paste. For a rewrite, show each changed block as
   *before* and *after*, then the full rewritten page.
2. **Why this block is here** — a table: block · pattern it serves · what an engine can do
   with it. One row per block, in page order.
3. **Open items** — every `[SOURCE NEEDED]` and `[FACT NEEDED]`, each with the claim it
   protects. The page is not ready to publish while any remain.
4. **Hand-offs** — to `schema-markup` (state the types: `Article` or `Product`, and
   `FAQPage` only when the FAQ is visible on the page), to `on-page-seo` (title and meta
   description built from the direct answer, internal links to the sub-question pages), and
   to `geo-audit` to re-score the live page.
5. **How you will know it worked.** After publishing, the target query should be a
   monitored prompt in Era. In four to six weeks re-read its answers (`list_answers`,
   `get_answer`) and look for the page URL among the citations and for the brand in the text.
   Without Era, ask an engine that shows sources the same question a few times. Answers
   vary between runs, so judge by several.

## Guardrails

- Never invent a statistic, quote, study, customer, award, price or date. Use a placeholder
  and ask. A made-up number that gets cited does more harm than a missing one.
- Say a claim is sourced only when the source supports that exact claim.
- Write for the reader first. No keyword stuffing, no hidden text, no sentences that exist
  only for an engine.
- The tone of voice sets the voice, not the structure: keep the direct answer first even
  when the tone prefers a slow opening.
- Comparison pages state their criteria and stay accurate about competitors, including where
  a rival is better when that is true.
- Health, legal and financial claims need primary sources and a named expert reviewer.
- No promise of citation. Engines choose their sources per query and vary by run. A rewrite
  raises the odds that a page is usable, nothing more.
- This skill drafts. It does not publish, and it does not call `propose_article_edit`; for an
  Era article, hand the rewrite to `article-review`.

## Era tools used (all optional, all read)

- `list_brands`, `get_brand_kit`, `list_tones` — brand, positioning, voice.
- `list_keyword_clusters`, `list_keywords` — target phrases and AI volume.
- `list_search_queries` — the exact questions engines run.
- `list_cited_domains` — sources the engines already trust.
- `list_answers`, `get_answer` — the after-publication check.

## Without Era

Everything but step 3 runs on what the user provides. Questions then come from the page's
own headings, support tickets, sales calls and the related questions an engine or search
page shows; sources come from the user. Skip the brand-kit and tone lines and note that Era
would supply the exact sub-queries and the domains the engines already cite.
