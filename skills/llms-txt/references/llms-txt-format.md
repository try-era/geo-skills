# llms.txt format, worked example and validation checks

The format comes from the proposal at <https://llmstxt.org>. It is a proposal, not a
standard: no standards body maintains it, and the site is the reference. Re-read it before
telling a user that a detail is "required".

## What the file is for

A plain Markdown file at the site root that gives a language model a short, curated map of
the site: what it is, and which pages to read first. It is written for an agent that has a
limited context window and fetches pages on demand (a coding assistant reading product
docs, a research agent, an answer engine with a fetch tool). It is not a sitemap, not a
robots file and not an access-control mechanism: listing a URL grants nothing, omitting one
blocks nothing.

## Structure

The proposal defines this order. Only the H1 is required.

1. `# Name` — one H1: the site or project name. Required.
2. `> Summary` — a blockquote, one to three sentences: what this is and who it is for, with
   the facts a reader needs to interpret everything below.
3. Free Markdown — zero or more paragraphs or lists, with **no headings**: caveats and
   interpretation notes ("Docs are versioned; v3 is current", "Prices are in USD").
4. `## Section` — zero or more H2 sections. Each holds a Markdown list of links.
5. `## Optional` — an H2 with a reserved meaning: links that can be skipped when the
   reader needs a shorter context.

A list item is `- [Name](url)` with an optional `: notes` after it.

```
- [Quickstart](https://example.com/docs/quickstart): create a key and send the first request in five minutes
```

## Rules this skill applies

These are the proposal's rules plus the conventions that make a file useful. The first
group is structure; the rest is judgement.

| Rule | Why |
| --- | --- |
| Exactly one H1, first line | The only required element; parsers key on it |
| Blockquote directly after the H1 | The summary is what a truncated read still sees |
| No headings inside the free text before the first H2 | The proposal reserves headings for the link sections |
| Every link is absolute, `https`, on the canonical host | Relative links break when the file is fetched out of context |
| Link text is the page's name, not "click here" or the URL | The name is the label the agent sees |
| The note is one line, written from the page, no marketing words | It is what the agent uses to choose without opening the page |
| Same URL once | A duplicate wastes the reader's budget and signals a generated dump |
| The linked URL returns 200 and is indexable, in one hop | An agent that hits a redirect chain or a 404 loses trust in the file |
| Content type `text/plain` or `text/markdown`, UTF-8 | A `text/html` 200 usually means a single-page-app fallback, not a file |
| Sections ordered by importance; `## Optional` last | Readers truncate from the end |
| 10–60 links for most sites | A map, not an index. Large docs sites link section hubs and rely on `llms-full.txt` for depth |

## Markdown versions of pages

The proposal also suggests that pages useful to a model are available as clean Markdown at
the page's own URL with `.md` appended (and `index.html.md` for URLs that end in a
directory). If the site does this, link the `.md` URLs: they carry the content without
navigation, scripts and cookie banners. If it does not, link the HTML pages. Never invent a
`.md` URL; request it and keep it only if it returns 200 with Markdown.

## llms-full.txt

A second file, by convention, not part of the minimum proposal. It holds the **text of the
linked pages**, concatenated as Markdown, so an agent can load the whole documentation in
one request. Practical shape:

- Same order as `llms.txt`, one block per page.
- Each block starts with the page title as a heading and the source URL on the next line.
- Body is the main content only: no navigation, footer, cookie text, related-links lists.
- Headings inside a page are demoted one or two levels so the page title stays the top
  heading of its block.
- Code blocks, tables and lists survive the conversion; images become their alt text, or
  nothing if decorative.
- Size: report characters and an estimate of tokens (characters divided by four). Above
  roughly 200,000 tokens most context windows cannot hold it; split by section
  (`/docs/llms-full.txt`) and say so in `llms.txt`.

Do not put gated, personalised or internal content in either file. Both are public.

## Worked example

A fictional company, Kestrel Billing, `https://www.kestrelbilling.example`. Its site has
product pages, documentation, an API reference, a blog and legal pages. Below is the
`llms.txt` a careful pass over its sitemap would produce.

```markdown
# Kestrel Billing

> Kestrel Billing is a usage-based billing API for B2B software companies. It meters usage events, prices them against plans, issues invoices and syncs revenue to accounting systems. This file lists the pages that explain the product, its API and its pricing.

Documentation is versioned; the pages below describe v3, the current version. Prices are in US dollars per month, billed annually. The API base URL is https://api.kestrelbilling.example/v3.

## Product

- [Usage metering](https://www.kestrelbilling.example/product/metering): how events are ingested, deduplicated and aggregated into billable quantities
- [Pricing models](https://www.kestrelbilling.example/product/pricing-models): flat, tiered, volume, package and prepaid-credit pricing, with the limits of each
- [Invoicing and revenue sync](https://www.kestrelbilling.example/product/invoicing): invoice generation, proration rules, and the QuickBooks and Xero connectors
- [Pricing](https://www.kestrelbilling.example/pricing): three plans with event allowances and overage rates

## Documentation

- [Quickstart](https://www.kestrelbilling.example/docs/quickstart): create an API key, define a plan and send a first usage event
- [Concepts](https://www.kestrelbilling.example/docs/concepts): customers, meters, plans, subscriptions and invoices, and how they relate
- [Event ingestion](https://www.kestrelbilling.example/docs/events): event schema, idempotency keys, batch limits and late-event handling
- [Webhooks](https://www.kestrelbilling.example/docs/webhooks): event types, signature verification and retry schedule
- [Migrating from v2](https://www.kestrelbilling.example/docs/migrate-v2): breaking changes between v2 and v3 and a field-by-field mapping

## API reference

- [Authentication](https://www.kestrelbilling.example/api/authentication): API key scopes, rotation and rate limits
- [Customers](https://www.kestrelbilling.example/api/customers): create, update and list customers
- [Usage events](https://www.kestrelbilling.example/api/usage-events): the endpoint that records usage, with request and response examples
- [Invoices](https://www.kestrelbilling.example/api/invoices): retrieve, finalise and void invoices
- [Errors](https://www.kestrelbilling.example/api/errors): error codes, their causes and whether a retry is safe

## Guides

- [Billing for AI API usage](https://www.kestrelbilling.example/guides/ai-usage-billing): a worked setup for token-based pricing with per-model rates
- [Prorations explained](https://www.kestrelbilling.example/guides/prorations): the three proration modes with a numeric example for each
- [Revenue recognition export](https://www.kestrelbilling.example/guides/revenue-recognition): which fields to export and how they map to a ledger

## Company

- [About Kestrel Billing](https://www.kestrelbilling.example/about): who runs the company, where it is based and how it is funded
- [Security](https://www.kestrelbilling.example/security): hosting regions, encryption, SOC 2 report availability and data retention

## Optional

- [Blog](https://www.kestrelbilling.example/blog): product announcements and engineering write-ups; read only for history or a specific topic
- [Changelog](https://www.kestrelbilling.example/changelog): dated list of API and dashboard changes
- [Privacy policy](https://www.kestrelbilling.example/legal/privacy): how customer and end-customer data is processed
- [Terms of service](https://www.kestrelbilling.example/legal/terms): contract terms for the service
```

What this example does on purpose:

- The blockquote states the product, the buyer and the contents in plain terms.
- The free paragraph holds the three facts an agent would otherwise get wrong: current
  version, currency, and the API base URL.
- Sections follow the reader's likely order: what it is, how to use it, the reference,
  worked guides, the company, then the skippable material.
- Each note says what the page contains (limits, numbers, formats), not that it is "a
  comprehensive guide".
- The blog is one hub link in `## Optional`, not forty posts. The sitemap's tag pages,
  author pages, paginated archives and the checkout path are absent.

### The matching llms-full.txt, first block only

```markdown
# Kestrel Billing - full documentation text

Source: https://www.kestrelbilling.example/llms.txt
Generated: 2026-10-15. Pages are listed in the same order as llms.txt.

---

# Quickstart

Source: https://www.kestrelbilling.example/docs/quickstart

## Before you start

You need a Kestrel Billing account and a test-mode API key ...

## Send your first usage event

Post an event to `/v3/usage-events` ...

---

# Concepts

Source: https://www.kestrelbilling.example/docs/concepts
...
```

## Validation checks

Run every check against an existing file, and against a freshly generated one before
handing it over. Severity: **error** = the file is broken or misleading; **warning** =
works but degrades; **info** = worth knowing.

| ID | Check | How | Severity |
| --- | --- | --- | --- |
| V1 | File exists at `/llms.txt` on the canonical host, status 200, no redirect | `curl -sSIL -o /dev/null -w '%{http_code} %{num_redirects} %{content_type}\n' https://host/llms.txt` | error |
| V2 | Content type is `text/plain` or `text/markdown`, not `text/html`; UTF-8 | same command; if HTML, read the body: a page shell means the server returns its app for unknown paths | error |
| V3 | First non-empty line is a single `# H1`; there is exactly one H1 | read the file | error |
| V4 | A blockquote follows the H1 | read the file | warning |
| V5 | No headings between the blockquote and the first H2 other than H2 sections; no H3 inside the link sections | read the file | warning |
| V6 | Every list item under an H2 is `- [text](url)` or `- [text](url): note`; no bare URLs, no empty text | regex over the file | warning |
| V7 | Every URL is absolute, `https`, on the site's canonical host (no `www` mix, no staging host, no `localhost`, no tracking parameters) | list the hosts; compare with the canonical host | error |
| V8 | Every URL returns 200 in at most one redirect | request each; count 301/302/404/410/5xx | error for 4xx/5xx, warning for a redirect |
| V9 | No URL appears twice, including differing only by trailing slash, fragment or case | normalise and count | warning |
| V10 | Every linked page's canonical equals the listed URL; none is `noindex` | read `rel=canonical` and the robots meta of each page | warning |
| V11 | Every listed URL is in the sitemap, and the pages that matter most (pricing, docs hub, about) are in the file | compare against the sitemap | info |
| V12 | Length: the file is a map (about 10 to 60 links); no section has more than about 15 entries | count | info |
| V13 | Notes: present on most items, one line, no marketing adjectives, not a copy of the title | read | info |
| V14 | `## Optional`, if present, is the last section | read | warning |
| V15 | File is not blocked by `robots.txt` and not served with `noindex` in `X-Robots-Tag` unless the owner intends it | read `robots.txt` and the response headers | warning |
| V16 | `llms-full.txt`, if present: same checks V1-V2; blocks match the pages in `llms.txt`; size and token estimate reported | fetch and count | warning |

A file with any error is "broken". With only warnings it is "valid with warnings". Report
the check ID next to every finding so the user can re-run it.
