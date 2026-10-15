---
name: on-page-seo
description: Optimize one page against its target query — title tag, meta description, H1/H2 structure, keyword and entity coverage, search-intent match, internal links in and out, image alt text, content gaps versus the pages that rank, thin or duplicated sections. Use for "on-page SEO", "optimize this page", "why doesn't this page rank for X", or title and meta rewrites.
argument-hint: <url> --query "<target query>" [--compare <url> <url>]
---

# On-page SEO

Take one page and one target query, show exactly where the page falls short of what the
query needs and of what currently ranks for it, and hand back the rewritten title, meta
description, H1, H2s, an internal-link plan and a short list of content gaps.

## When to use

- "Optimize this page for <query>", "on-page SEO review", "why is this page stuck on page
  two", "rewrite the title and meta description".
- After `technical-seo-audit` shows the page is crawlable and indexable but not performing.
- Before updating an older page that should rank for a defined query.

Not for: crawl, index, redirect or speed problems (`technical-seo-audit`); writing or
rewriting the body copy (`answer-engine-content`); planning a new article from scratch
(`content-brief`); structured data (`schema-markup`); how AI engines see the page
(`geo-audit`).

## Inputs

- **URL** (or the pasted draft for an unpublished page).
- **Target query** — the primary query the page should rank for, plus up to five
  secondary queries or questions if the user has them. If none is given, derive the
  primary query from the H1 and title and say that you did. One page, one primary intent.
- **Market** — country and language; they change what ranks.
- **Reference pages** (optional) — two or three URLs that rank for the query. If the user
  gives none and a search tool is available, search the query and take the first three
  organic results that are not the user's own domain; record the query, date and
  locale used. Results vary by location and personalisation, so call this a sample.
- **Site pages** (optional) — the sitemap or a list of related pages, for the link plan.
  Without it, work from the pages the fetched page links to and from the sitemap.

## Steps

1. **Fetch the page.** Record: status and final URL, `<title>`, meta description,
   canonical, robots meta, the full H1–H3 outline, visible word count of the main content,
   every image with its `alt`, every internal and external link with its anchor text,
   JSON-LD types, and any visible dates. If the main content is not in the raw HTML,
   stop and report it: the page cannot be assessed on-page until it is, and
   `technical-seo-audit` should look at rendering.
2. **Establish intent.** Classify the query: informational, commercial investigation,
   transactional, navigational or local. Look at what the reference pages are (guides,
   comparisons, product pages, tools, forum threads) and at their format. Decide whether
   the user's page is the right *type* for the query. If it is a product page for a "how
   to" query, say so plainly: the fix is a different page, not a rewrite. Intent
   patterns are in `references/elements.md`.
3. **Fetch the reference pages** (if available). For each, extract title, H1, the H2/H3
   outline, approximate word count, formats used (tables, lists, video, calculator),
   visible date, and the entities and sub-topics it covers. Use them as evidence of what
   the query needs; do not copy their wording.
4. **Build the coverage matrix.** Rows are sub-topics and entities; columns are the
   user's page and each reference page. A topic present on two or three of the references
   and absent from the page is a gap. A topic on only one reference is optional. A topic
   the page covers that no reference does is a possible differentiator; keep it only if it
   serves the query.
5. **Review each element** against `references/elements.md`, recording current value,
   issue and proposal:
   - title tag — length, primary term early, intent match, uniqueness
   - meta description — concrete promise, length, uniqueness
   - H1 — one, matches the title's promise, names the topic
   - H2/H3 — answer sub-questions, no skipped levels, no label-only headings
   - first 100 words — answer or definition present, primary term used naturally
   - URL — short, readable, stable (only recommend a change if the current one is
     misleading, and then only with a redirect plan)
   - images — missing, generic or stuffed alt text; file names; dimensions
6. **Check for thin and duplicated sections.** Mark sections that restate their heading,
   repeat other sections, or say nothing the references do not say better. Check whether
   another page on the user's site targets the same query (compare titles and H1s from the
   sitemap; with a search tool, look at which of the user's URLs appear for the query).
   If two pages compete, recommend merging or differentiating, not optimising both.
7. **Plan internal links.** *In:* find three to eight pages on the site that are
   topically related and already visible (hub pages, related articles, the product page
   this page supports) and propose a link from each: source URL, anchor text, where in
   the source it fits, and why. *Out:* propose two to five contextual links from this
   page to the pages a reader needs next. Check the page's existing links: broken,
   redirecting, `nofollow`, generic anchors, and whether the page is linked from
   anywhere except the sitemap.
8. **Assess snippet-worthiness.** Is there a self-contained answer of about 40 to 60
   words under a question heading? Do lists and tables appear where the references use
   them? List the blocks to add, with the heading each belongs under.
9. **Write the proposals.** Titles and descriptions in two or three variants with
   character counts; one H1; the revised H2 outline with new, moved and removed headings
   marked. Keep claims to what the page and the user's business can support.
10. **Write the gap list** and hand it off. For each gap: the topic, which reference
    pages cover it, where it belongs in the outline, and the action (add, deepen,
    restructure, delete). The rewrite itself belongs to `answer-engine-content`; for a
    full rewrite or a new page, `content-brief` produces the brief.

## Output

```
On-page SEO — {url}
Target query: "{query}" ({given by user / derived from H1}) · Market: {country, language}
Intent: {type} · Page type fits: yes / partly / no · Reference pages: {n} ({source})
Top issues: 1. {…} 2. {…} 3. {…}
```

Then:

1. **Element table**

   | Element | Current | Issue | Proposed |
   | --- | --- | --- | --- |
   | Title | "Prorations \| Kestrel" (20) | A label; no intent signal, primary term missing | "How to Prorate a Subscription Upgrade: 3 Methods and Examples" (61) |
   | Meta description | none | Engine will choose a fragment | "Three ways to prorate a subscription upgrade, with a worked example for each…" (145) |
   | H1 | "Prorations" | Same as title; no topic words | "How to prorate a subscription upgrade" |
   | Images | 4 images, 3 with `alt=""` or `alt="image"` | Content images undescribed | Alt text per image, in the rewrite section |

2. **Rewrites** — title, meta description and H1 (variants with counts, the recommended
   one marked), then the revised H2/H3 outline as a list with `new`, `moved`, `renamed`
   or `remove` beside each line.
3. **Coverage matrix** — sub-topic · this page · reference A · B · C · verdict (gap /
   optional / differentiator).
4. **Internal-link plan**

   | Direction | From | To | Anchor | Where | Reason |
   | --- | --- | --- | --- | --- | --- |
   | In | /blog/usage-billing-models | this page | proration methods | para on mid-cycle changes | Same topic; passes weight from a page that is already visited |
   | Out | this page | /pricing | plan limits | after the plan example | Next step for a buyer |

5. **Content gaps** — a short list, each line: topic · covered by · where it goes · action.
   End with the hand-off line: "Rewrite with `answer-engine-content`; use these gaps and
   the rewritten outline as the brief."
6. **How to tell it worked** — the metric and the window: in Search Console, the page's
   impressions, average position and click-through rate for the target query, compared
   over four to six weeks before and after the change. Title changes can be rewritten by
   the search engine; check the displayed title before judging.

## Guardrails

- Fetch only the page the user gave, reference pages the user gave or the search returned,
  and same-site pages for the link plan. No logins, no forms.
- Reference pages are evidence of what the query needs, never text to reuse. Do not
  reproduce their sentences, headings word for word, or numbers without a source.
- Do not promise rankings. Say what the change addresses and how the user will see it
  worked.
- A sample of three results is not the whole results page. State the sample, the date and
  the locale, and treat gaps found in only one reference as optional.
- Do not recommend keyword counts, density targets or word-count targets as goals.
- Keep titles, descriptions and headings truthful to the page. Do not propose wording the
  page cannot back up (prices, awards, "best", "free").
- Do not recommend changing a live URL, canonical or noindex setting without a redirect
  and a rollback plan, and route that to `technical-seo-audit`.

## Era tools used

None. This skill works on public pages only and needs no Era account.

## Hand-offs

- `answer-engine-content` — rewrite the page body from the gap list and the new outline.
- `content-brief` — a full brief when the right answer is a new page or a rebuild.
- `technical-seo-audit` — when the page is not indexable, not rendered in raw HTML, or
  competes with a duplicate URL.
- `schema-markup` — markup for the FAQ, breadcrumb and article once the content is final.
- `geo-audit` — to check the same page for AI-engine readiness (citability, crawler
  access).
