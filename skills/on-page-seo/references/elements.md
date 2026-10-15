# On-page elements: rules of thumb

These are working rules, not search-engine laws. Search engines rewrite titles and snippets,
and no document sets a character quota. Where a number is given, it comes from how results
are displayed (truncation is by pixel width, which characters only approximate) or from
common practice, and the audit says "rule of thumb" when it uses one.

The examples are written for a fictional product, Kestrel Billing. Character counts are
shown in brackets.

## Title tag

- **Purpose:** the clickable headline in results and the strongest on-page statement of
  what the page is about.
- **Length:** about 50 to 60 characters (roughly 580 px on desktop). Longer titles are
  cut off, so put the information that earns the click first.
- **Placement:** primary term (or its closest natural phrasing) first; brand last,
  separated by `|` or `-`; drop the brand on long titles rather than the topic.
- **Match intent:** an informational query gets a title that promises an explanation; a
  commercial query a comparison or price; a transactional query the product and the action.
- **Avoid:** a list of keywords, the brand repeated, `Home` or `Untitled`, the same title
  on several pages, all capitals, promises the page does not keep ("ultimate", "complete",
  "everything").

| | Title | |
| --- | --- | --- |
| Weak | Home \| Kestrel Billing \| Billing Software \| Usage Billing \| SaaS Billing \| Invoicing Tool | [89] keyword list, no promise, cut off |
| Good | Usage-Based Billing for SaaS: Models and Pricing \| Kestrel | [58] topic first, says what the page offers |
| Weak | Prorations | [10] a label; says nothing a searcher can act on |
| Good | How to Prorate a Subscription Upgrade: 3 Methods and Examples | [61] matches a "how to" query, states the count |
| Weak | The Ultimate Complete Guide to Everything You Need to Know About Prorating Subscription Upgrades and Downgrades in 2026 | [119] truncated, padded |
| Good | Proration Methods for Subscription Upgrades, With Examples | [58] same topic in half the length |

## Meta description

- **Purpose:** the sentence under the title. It does not rank the page directly; it
  decides whether the result gets clicked. Search engines often replace it with text from
  the page when that text matches the query better.
- **Length:** about 120 to 160 characters. Mobile shows less than desktop, so the first
  100 characters carry the message.
- **Write:** what the reader will get, in concrete terms (a number, a format, a
  deliverable), with the primary term used naturally. One idea per description. Unique
  per page.
- **Avoid:** "Welcome to", the brand's own adjectives ("leading", "innovative"), a
  repeated title, quotation marks that may be cut, claims the page does not support, an
  empty tag (the engine will pick a random fragment).

| | Description | |
| --- | --- | --- |
| Weak | Welcome to Kestrel Billing, the leading provider of innovative billing solutions for modern businesses. Learn more about our products and services today. | [153] generic, could describe any company |
| Good | Three ways to prorate a subscription upgrade, with a worked example for each and the invoice line items the customer sees. Includes a calculator. | [145] concrete deliverables |
| Good | Compare Kestrel Billing's three plans by monthly event allowance, overage rate and included integrations. Test mode is free; paid plans start at $99. | [149] a commercial page that states the price |

## H1

- **Purpose:** names the page for the visitor who has just arrived. It should confirm
  that the click went to the right place.
- **Rules:** one clear H1 per page; it contains the primary topic in the words a visitor
  would use; it does not have to equal the title, but it must make the same promise; it
  is real text, not an image or the logo.
- **Avoid:** "Welcome", the brand name alone, a slogan, an H1 that contradicts the title,
  several H1s used for styling.

| | H1 | |
| --- | --- | --- |
| Weak | Welcome | [7] |
| Weak | Billing, reimagined | [19] a slogan; names no topic |
| Good | How to prorate a subscription upgrade | [37] matches the query and the title's promise |

## H2 and H3 structure

- **Purpose:** the outline a skimming reader, a search engine and an answer engine all
  use. Each H2 should name one sub-topic or answer one sub-question.
- **Rules:** descending levels with no skips (H2 then H3); phrase headings the way users
  ask ("What happens to the invoice when a customer upgrades mid-cycle?") or as a plain
  claim ("Daily proration is the most accurate method"); keep each section focused on its
  heading; as a rule of thumb a 1,500-word page has four to eight H2s.
- **Avoid:** headings used only for styling, labels such as "Overview", "Details",
  "More", clever headings that do not say what follows, repeating the primary keyword in
  every heading.

| | H2 | |
| --- | --- | --- |
| Weak | Overview | label |
| Weak | Why Kestrel is the best prorations solution for your business | claim with no support, brand-led |
| Good | Which proration method fits which billing cycle? | a question a reader asks |
| Good | Daily proration charges exactly for the days used | a claim the section then proves |

## First 100 words

- **Purpose:** where the page proves it answers the query. For informational queries,
  answer or define in the first one to three sentences, then add context. For commercial
  pages, state what the product is, who it is for and one proof point.
- **Rules:** the primary term appears naturally; no preamble ("In today's fast-paced
  world"); the opening paragraph can stand alone if lifted into a snippet.
- **Hand-off:** when the opening needs to be rewritten, give the gap and hand it to
  `answer-engine-content`.

## Keyword and entity coverage

- **Where the primary term belongs:** title, H1, the first 100 words, one or two H2s, the
  URL, and in image alt text where it describes the image. Use natural variants elsewhere.
- **No density target.** If a sentence reads as written for a robot, rewrite it.
- **Entities:** the products, standards, people, places, units and tools a knowledgeable
  author would name. Compare with the reference pages: an entity that appears on two of
  three top results and not on this page is a gap; one that appears on only one is
  optional.
- **Avoid:** adding terms that no section uses, hidden text, a keyword list in the footer.

## URL slug

- Short, lowercase, hyphen-separated, with the primary term and no filler words
  (`/guides/subscription-proration`, not `/guides/the-complete-guide-to-subscription-proration-2026`).
- No dates unless the page is date-bound; no parameters or IDs for content pages.
- Changing a live slug needs a 301 redirect from the old one and updated internal links.
  Do not change slugs for cosmetic reasons.

## Internal links

- **Into the page:** link from pages that are topically related and already get
  attention: the hub for the topic, related articles, the product page the article
  supports, and (for new pages) the navigation or a "related" block. As a rule of thumb a
  new page needs three to eight in-body links from relevant pages; the plan says which
  and why.
- **Out of the page:** two to five contextual links per 1,000 words to pages that help
  the reader's next step: a deeper guide, the pricing page, the sign-up page. Link at the
  first natural mention.
- **Anchor text:** two to five words that say what the target is. Vary it naturally; do
  not use the exact-match target query on every link.
- **Avoid:** "click here", "read more", the bare URL, the same anchor pointing at two
  different pages, links to redirecting or `noindex` URLs, links only in the footer.

| | Anchor | |
| --- | --- | --- |
| Weak | click here | no information |
| Weak | best usage based billing software (on every link to /pricing) | repeated exact-match |
| Good | how proration works on invoices | describes the destination |
| Good | Kestrel's plan limits | short, specific |

## External links

- Link to primary sources for facts, numbers and standards, with the source named in the
  anchor or beside it. Use `rel="sponsored"` for paid links and `rel="ugc"` for user
  content.
- Avoid linking to a competitor's marketing page as the source of a general fact when a
  neutral source exists.

## Image alt text and file names

- **Alt text:** describes what the image shows and why it is there, in a phrase, usually
  under about 125 characters. Decorative images get an empty `alt=""`.
- **Charts and screenshots with data:** state the key figure in the caption or the body
  text too, so it is readable without the image.
- **File names:** descriptive and hyphenated (`proration-daily-example.png`).
- **Technical:** set `width` and `height`; use a modern format at the displayed size; do
  not lazy-load the image that is first on screen.

| | Alt | |
| --- | --- | --- |
| Weak | image1 | no content |
| Weak | billing software best billing tool saas billing | keyword stuffing |
| Good | Invoice showing a daily-prorated upgrade charge of $12.40 | describes content and figure |
| Good | `alt=""` on a decorative divider | correct for decoration |

## Snippet-worthy blocks

- A direct answer of about 40 to 60 words, placed right under the question heading it
  answers, written so it makes sense on its own.
- Steps as an ordered list, comparisons as a table with a header row, definitions as one
  sentence with the term at the start.
- Match the shape that currently ranks: if the reference results show lists, give a list.
- **FAQ block:** three to six questions that real searchers ask, answers of about 40 to 80
  words, visible on the page. Markup for them belongs to `schema-markup`.

## Thin and duplicated sections

- **Thin:** a section that says nothing the reference pages do not say better, or that
  restates the heading. Merge it, deepen it with an example or data, or delete it.
- **Duplicated:** text repeated across pages of the same site. As a rule of thumb, if
  more than about a third of the main content of two pages is identical, merge them,
  differentiate them, or canonicalise one to the other.
- **Boilerplate:** repeated intros and legal text are fine in moderation; repeated body
  paragraphs are not.
- There is no ideal word count. Match the depth the query needs, as shown by the reference
  pages, and stop.

## Freshness

- Show a real "last updated" date on content that changes (prices, versions, statistics).
- Update the date only when the content changed. A date that moves without edits erodes
  trust and, in structured data, is a consistency error.

## Intent match

| Query looks like | Page type that fits | Check |
| --- | --- | --- |
| "how to ...", "what is ..." | Guide or explainer | Answers up front; steps or definition; not a product page |
| "best ...", "... vs ...", "alternatives" | Comparison or list | Criteria, a table, named options with trade-offs |
| "buy ...", "... pricing", "... near me" | Product, pricing or location page | Price or next step above the fold, trust details, clear action |
| Brand or product name | Home or product page | Correct page ranks; sitelinks make sense |
| A tool or template ("... calculator", "... template") | The tool itself | Usable without reading first |

If the target query's intent differs from the page's type, the answer is a different
page, not a rewrite of this one.
