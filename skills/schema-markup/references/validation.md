# Validating JSON-LD

Two layers: structural self-checks that this skill runs itself, and external validators the
user runs because they need Google's or schema.org's services. Report which layer each
result came from, and never write "valid" for a check that was not run.

## 1. Structural self-checks (run by the skill)

| ID | Check | Severity |
| --- | --- | --- |
| V1 | Every block parses as JSON: straight quotes, no trailing commas, no comments, strings escape quotes and newlines | error |
| V2 | `@context` is `https://schema.org` (the `http://` form also works) at the top of each block | error |
| V3 | Every node has an `@type`, spelled with schema.org's capitalisation (`BlogPosting`, not `Blogposting`) | error |
| V4 | Required properties for the type are present (table below) | error |
| V5 | Every `{"@id": "..."}` reference resolves to a node in the same graph, or is an absolute URL on purpose | error |
| V6 | Each `@id` is defined once; no two nodes share one | error |
| V7 | `url`, `image`, `logo`, `thumbnailUrl`, `item`, `sameAs`, `embedUrl`, `contentUrl` are absolute `https` URLs | error |
| V8 | Dates are ISO 8601: `2026-10-15`, `2026-10-15T09:30:00+00:00`; durations `PT1H30M` | error |
| V9 | `price` is a bare number in a string or number; `priceCurrency` is an ISO 4217 code; `availability` is a full schema.org URL | error |
| V10 | No empty strings, `null`, placeholder text (`Lorem`, `TODO`, `example.com` on a real site), or HTML in plain-text fields | warning |
| V11 | Each real-world entity appears once per page. Two `Organization` or two `WebPage` nodes usually mean a theme and a plugin both emit markup | warning |
| V12 | Every marked-up fact is visible on the page (see section 3) | error |
| V13 | `sameAs` URLs resolve (status 200 after redirects) and point at the same entity. Social sites often answer scripts with 403 or 999; report those as unverified, not broken | warning |
| V14 | Image URLs resolve and meet the size Google asks for the type (an article image should be large enough for a 1200 px preview) | warning |

### Required properties, by type

Use this table for V4. "Eligible" means eligible for the matching Google rich result.

| Type | Required for eligibility |
| --- | --- |
| Organization | none; `name` and `url` in practice |
| WebSite | `url`; `name` for the site-name feature |
| Article / BlogPosting / NewsArticle | none; `headline`, `image`, `datePublished`, `author` in practice |
| Product (snippet) | `name` + one of `offers`, `aggregateRating`, `review` |
| Product (merchant listing) | `name`, `image`, `offers.price`, `offers.priceCurrency` |
| Offer | `price`, `priceCurrency` |
| AggregateRating | `ratingValue` + `reviewCount` or `ratingCount` |
| FAQPage | `mainEntity` with `Question.name` and `acceptedAnswer.text` |
| HowTo | `name`, `step` with `HowToStep.text` |
| BreadcrumbList | `itemListElement` with `position`, `name`; `item` on all but the last |
| LocalBusiness | `name`, `address` |
| SoftwareApplication | `name`, `offers.price`, and `aggregateRating` or `review` |
| Person | `name` |
| Event | `name`, `startDate`, `location` |
| VideoObject | `name`, `thumbnailUrl`, `uploadDate` |

### Extracting and checking a page's JSON-LD

This stdlib-only snippet fetches a page (or reads a saved file), pulls out every
`application/ld+json` block, and runs V1, V2, V5, V7, V8, V10 and V11. It makes one GET
request. Replace `URL_OR_FILE`.

```bash
python3 -I - URL_OR_FILE <<'PY'
import json, re, sys, urllib.request
src = sys.argv[1]
if src.startswith("http"):
    req = urllib.request.Request(src, headers={"User-Agent": "schema-check/1.0"})
    html = urllib.request.urlopen(req, timeout=20).read(3_000_000).decode("utf-8", "replace")
else:
    html = open(src, encoding="utf-8").read()
pat = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
blocks = re.findall(pat, html, re.S | re.I)
print(len(blocks), "JSON-LD block(s);", "microdata" if "itemscope" in html else "no microdata")
ids, refs, types, problems = set(), [], [], []
ISO = re.compile(r"^\d{4}(-\d{2}(-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?)?)?)?$")
URLKEYS = {"url", "image", "logo", "thumbnailUrl", "item", "sameAs", "embedUrl", "contentUrl", "@id"}
DATEKEYS = {"datePublished", "dateModified", "uploadDate", "startDate", "endDate", "foundingDate", "priceValidUntil"}
def walk(o, path):
    if isinstance(o, dict):
        if "@id" in o:
            (ids.add if len(o) > 1 else refs.append)(o["@id"])
        if "@type" in o:
            types.append(o["@type"] if isinstance(o["@type"], str) else "/".join(o["@type"]))
        for k, v in o.items():
            if k in URLKEYS:
                for u in (v if isinstance(v, list) else [v]):
                    if isinstance(u, str) and not re.match(r"^https?://", u):
                        problems.append(f"{path}.{k}: not an absolute URL: {u[:60]}")
            if k in DATEKEYS and isinstance(v, str) and not ISO.match(v):
                problems.append(f"{path}.{k}: not ISO 8601: {v}")
            if isinstance(v, str) and v.strip() == "":
                problems.append(f"{path}.{k}: empty string")
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")
for n, raw in enumerate(blocks, 1):
    try:
        data = json.loads(raw)
    except ValueError as e:
        problems.append(f"block {n}: invalid JSON: {e}")
        continue
    ctxs = [data.get("@context")] if isinstance(data, dict) else [d.get("@context") for d in data if isinstance(d, dict)]
    if not any(c and "schema.org" in json.dumps(c) for c in ctxs):
        problems.append(f"block {n}: no schema.org @context")
    walk(data, f"block{n}")
problems += [f"unresolved reference: {r}" for r in refs if r not in ids]
dupes = sorted({t for t in types if types.count(t) > 1})
print("types:", ", ".join(types) or "none")
if dupes:
    print("types appearing more than once (check for duplicate plugin output):", ", ".join(dupes))
print("\n".join(problems) or ("no structural problems found" if blocks else "no JSON-LD in the raw HTML"))
PY
```

It reads the raw HTML. If it reports no JSON-LD on a page that shows rich results in a
browser, the markup is injected by JavaScript; say so, because crawlers that do not run
scripts will not see it.

## 2. External validators (run by the user)

| Tool | Address | What it tells you | How to use |
| --- | --- | --- | --- |
| Schema Markup Validator | `https://validator.schema.org/` | Whether the markup is valid schema.org: types, properties, nesting. It does not know Google's rules | Paste the code or give a public URL |
| Rich Results Test | `https://search.google.com/test/rich-results` | Whether Google can read the markup and which rich results it is eligible for, with errors and warnings. It renders the page | Give a public URL, or paste code |
| Search Console, Enhancements reports | Search Console, per type | How the live site's markup is doing at scale: valid items, warnings, errors, trends | Check one to two weeks after deployment |

This skill cannot run these services. Hand the user the paste-ready block and the two
links, and say what a clean result looks like: no errors in the Rich Results Test for the
types the page targets, and the same types listed in the validator. A warning for a
recommended property is not a failure; an error on a required property is.

## 3. Consistency with the visible page (V12)

Compare each marked-up fact with what a visitor sees. Check these first:

| Markup | Must match on the page |
| --- | --- |
| `headline`, `name` | The H1 or visible title |
| `datePublished`, `dateModified` | The dates shown. If the page shows none, do not invent them from the CMS without telling the user |
| `author.name` | A visible byline |
| `price`, `priceCurrency`, `availability` | The price and stock state a visitor sees |
| `aggregateRating`, `review` | A visible rating and the reviews it summarises |
| `FAQPage` Q&A | Every question and answer is rendered on the page |
| `HowTo` steps | The steps appear, in the same order |
| `BreadcrumbList` | The visible trail or the actual site hierarchy |
| `telephone`, `address`, `openingHours` | The contact details shown, character for character |
| `video` / `VideoObject` | A video the visitor can play on the page |

When the markup says something the page does not, remove the markup; do not edit the page
to fit it unless the user asks. Structured data that misrepresents the page can cost the
site its rich results and can trigger a manual action.

## 4. Common errors and the fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| "Unexpected token" or the block is ignored | Trailing comma, curly quotes, unescaped quote or line break inside a string | Re-serialise with a JSON tool; escape `"` as `\"` and line breaks as `\n` |
| Two `Organization` nodes with different names | A theme and an SEO plugin both output markup | Keep one source; disable the other or merge them under one `@id` |
| `price` shows as an error | A currency symbol or thousands separator in the value | Use `"1499.00"` and put the code in `priceCurrency` |
| `availability` ignored | Bare word `InStock` | Use the full URL `https://schema.org/InStock` |
| Warning: missing field `image` | Article or product without an image | Add an absolute image URL, or accept the warning if the page has no image |
| AggregateRating flagged | No visible reviews on the page, or the rating is of the organisation itself | Remove it, or show the real reviews and rate the product |
| Reference to `#organization` does not resolve | The `@id` is defined on another page only | Define the node in the same graph, or use the absolute URL of the node that does exist |
| Dates rejected | `15/10/2026`, `Oct 15, 2026` | `2026-10-15` |
| Markup works in the test but not in the index | It is injected by JavaScript, or the page is `noindex` or blocked | Render it on the server; check indexability with the technical audit |

## 5. After deployment

1. Fetch the live page with the snippet above and confirm the block is in the raw HTML
   and unchanged by the CMS (some minify or escape it).
2. Test three pages per template, not one: a template bug repeats on every page.
3. Re-run the Rich Results Test on the live URL.
4. Look at the Search Console Enhancements report after one to two weeks. A rich result
   is not guaranteed even when the markup is valid; eligibility is not the same as
   display.
5. Re-validate whenever the template, the price feed or the review source changes.
