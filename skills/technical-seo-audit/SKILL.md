---
name: technical-seo-audit
description: Audit a site's technical SEO from public fetches — crawlability, indexability, canonicals, redirects, sitemaps, robots.txt, HTTPS, mobile, Core Web Vitals, duplicate content, pagination, hreflang and JavaScript rendering — with findings ranked by impact and effort. Use for "technical SEO audit", "why isn't this page indexed", "site health check" or crawl and indexing problems.
argument-hint: <url> [--site] [--page <url>...]
---

# Technical SEO audit

Find what stops search engines from crawling, rendering, indexing and ranking a site's
pages, prove each finding with a fetched status code, header, tag or count, and rank the
fixes so the first ones are the ones that matter.

## When to use

- "Technical SEO audit", "site health check", "why is this page not indexed", "we lost
  traffic after the migration".
- Before a redesign or replatform, and after one, to confirm nothing was lost.
- When `geo-audit` reports a page the engines cannot fetch or render.

Not for: how AI crawlers are treated and whether the content is citable (`geo-audit`);
title, headings and content for one query (`on-page-seo`); writing structured data
(`schema-markup`); building the `llms.txt` file (`llms-txt`).

## Inputs

- **URL** — the home page or the page with the problem. With `--site`, audit the site;
  with `--page`, audit only the URLs given.
- **Symptom** (optional) — "page X is not indexed", "traffic fell on date Y", "slow on
  mobile". It decides which checks come first.
- **Data the user can paste** — Search Console coverage and crawl-stats summaries,
  PageSpeed Insights or CrUX results, a crawler export. Ask once; do not invent any of it.
- **Platform** (optional) — CMS, framework, CDN. It changes where fixes happen.

## Steps

Read `references/checklist.md` for the full list; this is the order of work. Use the web
fetch tool for pages and `curl` for headers and redirect chains when a shell is available.
Pause about a second between requests and keep a first pass to about 60 requests unless
the user asks for more.

1. **Choose the sample.** Technical problems live in templates, not single URLs. Take the
   home page, one listing or category, one detail page (product, article, doc), one deep
   page, one parameterised URL, and a made-up URL for the 404 test. Add the page named in
   the symptom. Say which URLs make up the sample.
2. **Transport and redirects.** Request the four host and protocol variants
   (`http`/`https` x apex/`www`) and record status, hops and final URL:

   ```
   for u in http://example.com/ http://www.example.com/ https://example.com/ https://www.example.com/; do
     curl -sSIL -o /dev/null -w "$u -> %{http_code} hops=%{num_redirects} %{url_effective} ttfb=%{time_starttransfer}s\n" "$u"
   done
   ```

   Then the made-up URL (`.../zz-audit-<timestamp>`): it should be a 404, not a 200 or a
   redirect to the home page. Record the kind of each redirect hop (301/308 or 302/307).
3. **robots.txt.** Fetch it. Read: status, `Disallow: /` for all agents, blocked asset
   paths, `Sitemap:` lines, size. Test the sample URLs against the rules by hand. A 5xx
   on `robots.txt` is treated by Google as a full disallow for a while, so rank it high.
4. **Indexability per sampled URL.** One fetch gives everything:

   ```
   curl -sSL -A 'Mozilla/5.0 (compatible; seo-audit/1.0)' -D /tmp/h.txt -o /tmp/p.html URL
   grep -i -e '^HTTP/' -e x-robots-tag -e '^link:' -e content-encoding -e cache-control /tmp/h.txt
   grep -i -o -e '<meta[^>]*name=.robots.[^>]*>' -e '<meta[^>]*name=.googlebot.[^>]*>' \
     -e '<link[^>]*rel=.canonical.[^>]*>' -e '<link[^>]*hreflang[^>]*>' \
     -e '<meta[^>]*name=.viewport.[^>]*>' /tmp/p.html
   ```

   Record: status, `noindex` in the tag or header, canonical (absolute? self? does its
   target return 200 and indexable?), the robots-and-noindex conflict, hreflang tags,
   viewport. Test a parameterised URL (`?utm_source=x&sort=price`) for its canonical.
5. **Sitemaps.** Fetch each sitemap from `robots.txt`. Check validity, URL count against
   the 50,000-URL and 50 MB limits, host and protocol, and sample 20 URLs: each should be
   200, indexable and self-canonical. Compare `lastmod` with the pages' real dates for a
   few.
6. **Duplicates, pagination, hreflang.** Compare titles and H1s across a template.
   For listings, check that page 2 has its own URL, a self-canonical and crawlable
   `<a href>` links. For multilingual sites, take one URL set and confirm return tags,
   self-reference, valid codes (`en-GB`, not `en-UK`) and that every alternate returns 200
   and is canonical.
7. **Mobile and JavaScript rendering.** Fetch the page with a desktop and a mobile
   user-agent and compare word counts, link counts and canonicals. Then ask the JS
   question: are the title, H1, main text, internal links, canonical and structured data
   in the raw HTML? An empty `<div id="root">` or `id="__next"` with little text means
   the content exists only after scripts run. Rendered HTML can be compared only with a
   browser tool, the Rich Results Test or Search Console URL Inspection; if none is
   available, say that rendering was not verified and report only the raw-HTML evidence.
8. **Performance and Core Web Vitals.** State the limits plainly.

   | Can be measured from a public fetch | Cannot be measured without a tool |
   | --- | --- |
   | TTFB (`curl -w '%{time_starttransfer}'`), HTML size, compression, caching headers | LCP, INP and CLS values |
   | Render-blocking scripts and styles in the head, count of third-party hosts | Interaction latency and long tasks (INP needs real interactions) |
   | Image formats, byte sizes, `width`/`height` attributes, `loading` and `fetchpriority` on the likely LCP image | Layout shifts from late-loaded ads, embeds and banners |
   | Font loading rules and preloads | Any pass or fail verdict on the Core Web Vitals assessment |

   The Core Web Vitals thresholds are LCP 2.5 s or less, INP 200 ms or less and CLS 0.1
   or less at the 75th percentile of real page loads, assessed separately for mobile and
   desktop. The source of truth is field data: the CrUX data shown in PageSpeed Insights
   ("real users" section), the CrUX API or dashboard, and the Search Console Core Web
   Vitals report. A lab run (Lighthouse) explains causes but does not replace the field
   verdict, and Lighthouse does not measure INP. If the user can run PageSpeed Insights on
   the URL, ask for the field numbers. Otherwise report the measurable proxies, label the
   verdict "not measured", and never state an LCP, INP or CLS number you did not receive.
9. **Hand off adjacent findings.** Missing or duplicate titles and descriptions go to
   `on-page-seo`; absent or invalid structured data to `schema-markup`; AI-crawler rules
   to `geo-audit`. Note them in one line each; do not audit them here.
10. **Rate each finding.** Assign impact (critical, high, medium, low) and effort (S, M, L)
    with `references/priority-matrix.md`. Mark each finding observed or inferred; an
    inferred finding is never critical. List every check that needed a tool the user did
    not provide under "Could not check", with the tool that answers it.
11. **Order the fixes** by the matrix: critical first, then quick wins, then scheduled
    work, respecting dependencies (access, rendering, indexation signals, discovery,
    performance, hygiene).

## Output

```
Technical SEO audit — {site}
Sample: {n} URLs across {m} templates · fetched {date} · tools: fetch, curl · not available: Search Console, CrUX
Findings: {c} critical · {h} high · {m} medium · {l} low
Verdict: {one sentence — e.g. "Staging noindex is live on /products/*, so 1,240 product pages cannot be indexed."}
```

Then:

1. **Findings table**, sorted by impact then effort:

   | # | Area | Finding | Evidence | Impact | Effort | Fix |
   | --- | --- | --- | --- | --- | --- | --- |
   | 1 | Indexability | `/products/*` carries `noindex` | `curl` of /products/blue-widget: `<meta name="robots" content="noindex,follow">` | Critical | S | Remove the tag from the product template; redeploy |

   Evidence is the command output, the header, the tag or the count, with the URL. "Looks
   slow" is not evidence.
2. **Fix order** — a numbered list; each line names the finding number, why it sits at
   that position (impact, effort, dependency), the owner type (content, developer, DevOps)
   and the check that verifies it (see the table in `references/priority-matrix.md`).
3. **Could not check** — each item with the tool that answers it: Search Console (coverage,
   crawl stats, URL Inspection), PageSpeed Insights or CrUX (Core Web Vitals), a crawler
   (orphan pages, full redirect graph), a browser (rendered DOM, interstitials).
4. **Hand-offs** — findings that belong to another skill, one line each.

For a single-page audit, keep the same structure with the sample reduced to that page and
the site-level checks (sitemap, robots, host variants) reported once.

## Guardrails

- Read-only. Use GET and HEAD against public URLs the user gave, the sitemap lists, or
  the pages link to on the same site. The only URLs you construct are the standard
  probes: `/robots.txt`, the sitemap locations it names, the host and protocol variants
  of the given URL, one made-up path for the 404 test, and a tracking-parameter variant
  of a given URL. Never log in, submit forms, or run load tests.
- Rate-limit requests. Use a plain user-agent that names the audit. Fetch with a
  search-engine user-agent string only to test for user-agent-based blocking, and say so
  in the finding.
- Separate what was observed from what is inferred, and say which is which. A canonical
  is a hint and a sitemap is a suggestion: write "the site asks for X", not "Google will
  index X".
- Do not predict ranking or traffic changes. State the mechanism and how to verify the
  fix.
- Never fabricate Core Web Vitals, index counts or crawl statistics. If a number did not
  come from a command or from the user, it does not appear.
- A site behind a CDN or WAF may answer an audit script differently from a real
  crawler. If a fetch returns 403 or a challenge page, report that and do not conclude
  the site blocks search engines.

## Era tools used

None. This skill works on public pages only and needs no Era account.

## Hand-offs

- `geo-audit` — AI-crawler access, citability and the AI-readiness score for the same
  pages.
- `on-page-seo` — titles, meta descriptions, headings and content for the pages this
  audit finds indexable but weak.
- `schema-markup` — structured data findings.
- `llms-txt` — if the site wants a curated `llms.txt` after the sitemap is clean.
