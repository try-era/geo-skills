---
name: geo-audit
description: Audit a page or site for AI-search readiness (GEO / AEO) — can AI crawlers reach it, is there an llms.txt, is the content answer-shaped and citable, are entities and structured data clear, are authorship and freshness visible. Scores 0–100 with prioritised fixes. Use when the user asks how ChatGPT, Perplexity, Gemini or Claude see a URL, or wants a GEO, AEO or AI-visibility audit of a site.
argument-hint: <url> [--site] [--brand <name>]
---

# GEO audit

Answer one question with evidence: *when an AI answer engine looks for an answer in this
page's topic, can it find, read, trust and quote this page?* Score it, show the evidence,
and list the fixes in the order that moves the score most.

## When to use

- "How does ChatGPT / Perplexity see this page?", "GEO audit", "AEO audit", "AI readiness".
- Before publishing or redesigning a page that should get cited.
- As the diagnostic step when `ai-visibility-report` shows a page never gets cited.

Not for: Google crawl and speed problems (`technical-seo-audit`), writing the content
(`answer-engine-content`), or generating the `llms.txt` itself (`llms-txt`).

## Inputs

- **URL** — one page. With `--site`, also audit the home page, the `robots.txt`,
  `llms.txt`, the sitemap, and up to five pages the user names or the sitemap ranks first.
- **Target query** (optional) — the question this page should be the answer to. If absent,
  derive it from the H1 and say so.
- **Brand** (optional, Era) — with `--brand`, pull the brand's citation data so the audit
  knows whether the engines already cite this domain and which sources they prefer.

## Steps

1. **Fetch what the engines fetch.** Get `robots.txt`, `llms.txt`, `llms-full.txt`, the
   sitemap, and the page itself. Run `scripts/check_ai_access.sh <url>` when a shell is
   available — it prints the AI-crawler rules, the status of the three files, and the
   page's response headers. Otherwise fetch them with the web tool and read the same
   things by hand. Note the HTTP status, canonical, `noindex`, `nosnippet`,
   `max-snippet`, and whether the main content is present in the initial HTML or only
   rendered by JavaScript.
2. **AI crawler access.** Compare `robots.txt` against the agents in
   `references/ai-crawlers.md`. For each engine family, state: *allowed / blocked /
   unlisted*. Flag the common mistake of blocking the training crawler and the
   search/answer fetcher together (GPTBot vs OAI-SearchBot, ClaudeBot vs Claude-User,
   Google-Extended vs Googlebot).
3. **Answer shape.** Read the page as an engine would: does the first screen answer the
   target query directly, in one to three sentences, before context? Are the H2/H3s
   questions or claims the engine can map to sub-queries? Are definitions, numbers, steps
   and comparisons in extractable units (short paragraphs, lists, tables) rather than
   buried in prose? Count: direct-answer paragraphs, question headings, tables, lists.
4. **Citability.** What would an engine quote? Count concrete statistics with a stated
   source and date, named entities (products, people, standards, places), quotable
   one-sentence claims, and original data (benchmarks, surveys, first-hand tests). Note
   vague claims ("industry-leading", "fast") that no engine can cite.
5. **Entities and structured data.** Check for JSON-LD (`Organization`, `Article`,
   `Product`, `FAQPage`, `HowTo`, `BreadcrumbList`), `sameAs` links, a consistent brand and
   product name across title, H1 and schema, and `dateModified`. Validate what exists;
   list what is missing for this page type.
6. **Trust signals.** Author with a bio and credentials, organisation identity, contact
   page, last-updated date visible on the page, outbound citations to primary sources,
   consistency between what the page claims and what third-party sources say.
7. **Era context** (when `--brand` is given and Era is connected). `list_brands` → brand;
   `list_cited_domains(brand_id, days=90)` and `get_top_citations` to see whether this
   domain is cited at all and which third-party domains the engines prefer in the
   category; `list_search_queries(brand_id)` to check whether the target query is one the
   engines actually run. Fold this into the score as the *Authority* category evidence.
8. **Score and write.** Apply `references/scoring.md` (six categories, 100 points). Each
   deduction is a line with the evidence. Then produce the report below.

## Output

```
GEO audit — {url}
Score 58/100  · Access 16/20 · Answer shape 9/20 · Citability 8/20 · Entities & schema 10/15 · Authority 9/15 · Freshness 6/10
Target query: "{query}"  (derived from H1 / given by user)
Verdict: {one sentence — e.g. "Readable by every engine, but nothing on the page is quotable: no numbers, no sources, no direct answer."}
```

Then:

- **Access** — table: engine family · crawler · rule · effect. Plus the three files
  (`robots.txt`, `llms.txt`, sitemap): present / missing / malformed.
- **Answer shape** — what the first screen says, the question headings found, the
  extractable units counted.
- **Citability** — the quotable sentences found (quote them), the statistics with and
  without sources, the vague claims to replace.
- **Entities & schema** — the schema present (validated), missing types for this page
  type, naming inconsistencies.
- **Authority & freshness** — author, organisation, dates, outbound citations, and (with
  Era) whether the engines already cite the domain.
- **Fixes, ranked** — a numbered list; each item says the expected score gain, the effort
  (minutes / hours / days), and which sibling skill does it (`llms-txt`, `schema-markup`,
  `answer-engine-content`, `on-page-seo`, `technical-seo-audit`).

With `--site`, add a per-page table (url · score · top fix) and a site-level section for
`robots.txt`, `llms.txt` and the sitemap. When the `geo-page-auditor` subagent is available
(it ships with this plugin), run one instance per page in parallel and merge their blocks;
otherwise audit the pages in sequence with the same rubric.

## Guardrails

- Only fetch public URLs the user gave or that the sitemap lists. Never submit forms or
  follow login flows.
- Report what the fetch returned, not what the CMS claims. If the page needs JavaScript to
  show its content, say that the engines' fetchers may see an empty page, and score
  accordingly.
- Robots rules are read literally; do not assume an engine honours or ignores them beyond
  what the rules say.
- A score is a diagnosis, not a ranking prediction. Say so once in the Method line.

## Era tools used (optional)

- `list_brands` (read) — resolution.
- `list_cited_domains`, `get_top_citations` (read) — is this domain cited, and which
  sources win.
- `list_search_queries` (read) — is the target query one the engines run.

## Without Era

Everything except step 7 runs on the public page alone. Skip the Era line in *Authority*
and note that citation data would show whether the engines already trust the domain.
