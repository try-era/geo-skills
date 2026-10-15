---
name: schema-markup
description: Generate and validate JSON-LD structured data for a page — pick the schema.org type (Organization, WebSite, Article, Product, FAQPage, HowTo, BreadcrumbList, LocalBusiness, SoftwareApplication, Person, Event, VideoObject), build one linked @graph from what the page shows, and check required properties. Use for "add schema", "structured data", "JSON-LD" or rich results.
argument-hint: <url or page description> [--type <Type>]
---

# Schema markup

Produce JSON-LD that says, in a form machines read without guessing, what a page is, who
published it and which facts it states, and that matches what a visitor can see. For a
page that already has markup, audit it, fix it, and report what changed.

## When to use

- "Add schema / structured data / JSON-LD to this page", "why no rich results", "fix the
  schema errors in Search Console".
- A `geo-audit` or `technical-seo-audit` finding says structured data is missing, invalid
  or mismatched with the page.
- Building a CMS template that must emit correct markup on every page of a type.

Not for: crawl and index problems that stop markup from being read
(`technical-seo-audit`); titles, headings and content (`on-page-seo`); writing the
question-and-answer or step content that FAQ and HowTo markup describe
(`answer-engine-content`).

## Inputs

- **Page** — a URL, pasted HTML, or a description of the page. A URL is best: the markup
  must be built from the page's own content.
- **Site facts**, asked once if not on the page: organisation name and legal name, logo
  URL (a square image of at least 112 px), the official profiles for `sameAs`
  (LinkedIn, GitHub, Crunchbase, YouTube, Wikipedia or Wikidata when they exist).
- **Page type** (optional) — if the user knows it. Otherwise infer it and say so.
- **Delivery** — a single page, or a template (CMS, framework). A template needs
  placeholders and a rule for which fields feed which property.

## Steps

1. **Read the page.** Fetch it (web fetch, or `curl -sSL`). Record the final URL and
   canonical, title, H1, language, author and dates as displayed, price and rating if
   shown, FAQ or step blocks, breadcrumb trail, contact details, images, videos. These
   are the only legitimate sources of values.
2. **Inventory existing markup.** Run the extraction snippet in
   `references/validation.md` on the URL: it lists each JSON-LD block, its types, parse
   errors, unresolved references and duplicates. Also look for `itemscope` (microdata)
   and `typeof` (RDFa). Decide for each existing node: keep, fix, merge or drop. Two
   `Organization` nodes from a theme and a plugin are a finding.
3. **Choose the types.** Use the table below; read the matching section of
   `references/schema-types.md` for required and recommended properties.

   | Page | Primary node | Supporting nodes |
   | --- | --- | --- |
   | Home page | `WebSite`, `Organization` | `WebPage` |
   | Blog post, guide | `BlogPosting` or `Article` | `WebPage`, `BreadcrumbList`, `Person`, `Organization` |
   | News story | `NewsArticle` | same as above |
   | Documentation page | `TechArticle` | `WebPage`, `BreadcrumbList` |
   | Product or plan | `Product` + `Offer` | `ItemPage`, `BreadcrumbList`, `Organization` |
   | Software product | `SoftwareApplication` / `WebApplication` + `Offer` | `WebPage`, `Organization` |
   | Page with visible Q&A | `FAQPage` (as the page type or `mainEntity`) | beside the page's main type |
   | Procedure with steps | `HowTo` | beside `Article` |
   | Business location | `LocalBusiness` subtype | `WebPage`, `Organization` |
   | Author or team page | `ProfilePage` + `Person` | `Organization` |
   | Event | `Event` | `WebPage`, `Organization` |
   | Page built around a video | `VideoObject` | beside the page's main type |
   | About or contact page | `AboutPage` or `ContactPage` | `Organization` |

   One page, one primary entity: the thing the page is about. Do not stack `Product` on
   an article that merely mentions a product. Use the most specific accurate subtype
   (`Dentist`, not `LocalBusiness`; `BlogPosting`, not `Article`).
4. **Gather values and note gaps.** For each property, record where on the page its value
   comes from. A required value that the page does not show is a gap: leave the property
   out and list it. Never fill it from memory, a guess, or a competitor.
5. **Build one `@graph`.** A single `<script type="application/ld+json">` block with
   `"@context": "https://schema.org"` and an `@graph` array. Link the nodes:
   - Give each reusable entity a stable absolute `@id`: `https://host/#organization`,
     `https://host/#website`, `<page-url>#webpage`, `<page-url>#article`,
     `<page-url>#breadcrumb`, `<author-page>#person`.
   - `WebPage.isPartOf` -> `WebSite`; `WebPage.breadcrumb` -> `BreadcrumbList`;
     `Article.mainEntityOfPage` -> `WebPage`; `Article.author` -> `Person`;
     `Article.publisher` and `Product.brand` -> `Organization`; `Organization.logo` ->
     `ImageObject`.
   - Define the `Organization`, `WebSite` and `Person` nodes in full where the entity is
     introduced, and reference them by `{"@id": "..."}` elsewhere. The same `@id` on every
     page is what tells a consumer it is one entity.
   - `sameAs` on `Organization` and `Person` lists the official profiles and nothing else.
     It is how an engine ties the page's brand to the entity it already knows.
   - Absolute `https` URLs everywhere, using the canonical host. Dates in ISO 8601.
6. **Check consistency with the page** (check V12 in `references/validation.md`): every
   marked-up fact is visible to a visitor, and matches character for character where it
   is a name, price, date or contact detail. Remove markup the page does not support.
7. **Validate.** Run the structural self-checks V1–V14 yourself, then give the user the
   two external validators (schema.org validator, Google Rich Results Test) with the
   paste-ready block. State which checks you ran and that the Google test was not run.
8. **State the limits.** Google's rich results change and some are restricted. Say which
   of the page's types can produce a visible result today, using Google's current
   gallery, and which are for machine understanding only. FAQ and HowTo are the common
   cases: FAQ rich results are limited to well-known government and health sites, and
   HowTo rich results are no longer shown, so for most sites the markup does not change
   how the page looks in search. It remains valid, and it states the questions, answers
   and steps explicitly to any consumer that reads JSON-LD. Whether a given AI answer
   engine reads or weights structured data is not documented by most vendors; do not
   promise a citation gain. The test is observation: whether the Search Console report
   shows the items as valid, and whether citations of the page change over the following
   weeks.
9. **Placement.** Put the block in the server-rendered HTML (head or end of body), not
   injected by a script that crawlers may not run. One block per page where possible. For
   a template, give the template with variables and a table of field-to-property
   mappings, and test three pages per template after deploy.

## Output

```
Schema markup — {url}
Page type: {type} · Nodes: {list} · Existing markup: none / {n} blocks ({verdict})
Validation: structural {passed}/{total} checks passed · schema.org validator: not run · Rich Results Test: not run
Rich results possible today: {list or "none — markup is for machine understanding"}
```

Then:

1. **JSON-LD** — the complete block in a fenced `html` code block, including the
   `<script type="application/ld+json">` tags, ready to paste. One block, one `@graph`.
2. **Property table**:

   | Node | Property | Value source on the page | Required? |
   | --- | --- | --- | --- |
   | BlogPosting | headline | H1: "Prorations explained" | Recommended |
   | BlogPosting | datePublished | Byline: "Published 2 March 2026" | Recommended |
   | Product | offers.price | Price box: "$499 / month" | Required |

   Required means required for eligibility or for the markup to be useful (see
   `references/schema-types.md`). Every row has a source; a row with no source is not in
   the markup.
3. **Existing markup review** (when markup was found) — per block: kept, fixed, merged or
   removed, with the reason and the check ID.
4. **Validation notes** — the structural checks that passed, any warnings, the two links
   to run, what a clean result looks like, and the post-deploy steps (live fetch, Search
   Console Enhancements report in one to two weeks).
5. **Gaps** — properties the page does not support (for example, no visible date, no
   author) with the page change that would unlock each.

## Guardrails

- Mark up only what the page shows. No ratings, reviews, prices, dates, addresses, phone
  numbers, awards or `sameAs` links that are not on the page or supplied by the user.
- Never create a rating or review to make a rich result eligible. `AggregateRating`
  requires visible reviews from real users, and a business rating itself on its own page
  is not eligible.
- Never mark up content that is hidden from visitors or that the page does not contain
  (FAQ answers that appear only in the markup).
- Keep one source of truth. If a CMS plugin already emits correct markup, extend or
  disable it; do not add a second copy.
- Keep `dateModified` honest: change it only when the content changed.
- Misleading structured data can cost the site its rich results and can lead to a manual
  action. When a fact is uncertain, leave the property out.
- Fetch only the page the user gave and URLs it links to for checks (images, `sameAs`
  profiles). Never log in or submit forms.
- Do not claim a rich result will appear, or that AI engines will cite the page because
  of markup. Say what is eligible and how to check.

## Era tools used

None. This skill works on public pages only and needs no Era account.

## Hand-offs

- `geo-audit` — to see how the markup fits into the page's overall AI-readiness score.
- `technical-seo-audit` — if the markup is correct but not being picked up (noindex,
  blocked, JavaScript-injected, canonical conflict).
- `answer-engine-content` — to write the FAQ answers, steps or direct-answer blocks that
  the markup will describe, when the page lacks them.
- `on-page-seo` — for the title, headings and internal links around the marked-up page.
