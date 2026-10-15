# Scoring rubric (100 points)

Start each category at full marks and deduct with a one-line reason. Round the total.
A category with no evidence either way scores half and says "not verifiable".

## Access — 20

| Deduct | For |
| ---: | --- |
| 20 | The page returns non-200 to fetchers, or the main content is absent from the initial HTML |
| 8 | A search/fetch agent of a major engine (OpenAI, Anthropic, Google, Perplexity, Microsoft) is disallowed |
| 6 | `noindex`, `nosnippet` or `max-snippet:0` on a page meant to be cited |
| 4 | No `robots.txt`, or one that is malformed |
| 3 | No XML sitemap, or the page is not in it |
| 2 | Canonical points elsewhere or is missing |
| 2 | A CDN/WAF returns 403/429 to one of the tested AI user-agents |

## Answer shape — 20

| Deduct | For |
| ---: | --- |
| 8 | No direct answer to the target query in the first screen |
| 4 | Headings are labels ("Overview", "Features") rather than questions or claims |
| 4 | Key facts live only in long paragraphs: no lists, tables or short definition blocks |
| 2 | Steps, comparisons or specs are images, not text |
| 2 | The page answers several unrelated queries at once (no single topic) |

## Citability — 20

| Deduct | For |
| ---: | --- |
| 6 | No statistics at all |
| 4 | Statistics without a named source and date |
| 4 | No named entities beyond the brand (no products, standards, people, places) |
| 3 | No original data or first-hand observation |
| 3 | Marketing adjectives stand in for claims ("best", "fastest", "leading") |

## Entities and schema — 15

| Deduct | For |
| ---: | --- |
| 6 | No JSON-LD at all |
| 4 | Schema present but the type does not match the page (e.g. `Article` on a product page) or fails validation |
| 3 | Brand/product named inconsistently across title, H1, schema and body |
| 2 | No `sameAs` / organisation identity links |

## Authority — 15

| Deduct | For |
| ---: | --- |
| 5 | No identifiable author or organisation |
| 4 | No outbound citations to primary sources |
| 3 | With Era data: the domain is never cited by the engines in the brand's category |
| 3 | Claims on the page contradict what the engines' preferred sources say |

## Freshness — 10

| Deduct | For |
| ---: | --- |
| 5 | No visible or structured modification date |
| 3 | The content references facts, prices or versions that are clearly out of date |
| 2 | `dateModified` in schema disagrees with the visible date |

## Reading the total

- **80–100** — the engines can find, read and quote it; work on distribution and authority.
- **60–79** — fixable in a day; usually answer shape and schema.
- **40–59** — the page was written for people scanning, not for engines extracting; rewrite
  the top and add evidence.
- **below 40** — access or rendering problems come first; nothing else matters until the
  fetchers get a 200 with content.
