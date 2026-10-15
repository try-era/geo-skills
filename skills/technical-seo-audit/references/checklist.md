# Technical SEO checklist

Every item has an ID, how to check it with a public fetch (`curl` or the web fetch tool),
and why it matters. Items marked **[needs tool]** cannot be settled from public fetches
alone; the audit lists them under "Could not check" with the tool that answers them.

Conventions used in the commands:

```
UA='Mozilla/5.0 (compatible; seo-audit/1.0)'      # a plain, honest agent string
MOBILE='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36'
H() { curl -sS -A "$UA" -D - -o /dev/null "$@"; }       # headers only (single hop)
B() { curl -sSL -A "$UA" --max-time 20 "$@"; }          # body, following redirects
```

Pause about a second between requests, and keep to roughly 60 requests for a first pass.

## 1. Transport and HTTPS

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| T1 | HTTPS works on every URL with a valid certificate | `curl -sSI https://host/` returns headers, not a TLS error; expiry: `echo \| openssl s_client -connect host:443 -servername host 2>/dev/null \| openssl x509 -noout -dates` | An invalid or expired certificate shows users a full-page warning and stops most of them |
| T2 | HTTP redirects to HTTPS in one hop with a 301 or 308 | `H http://host/` and read `HTTP/` and `Location:` | Signals consolidate on one protocol; extra hops slow every first visit |
| T3 | One canonical host: apex and `www` resolve to one, by redirect | Run the four combinations (http/https x apex/www) and compare final URLs | Two live hosts split links and duplicate every page |
| T4 | HSTS header on HTTPS responses | `H https://host/` and look for `strict-transport-security` | Removes the insecure first hop for returning users; hygiene, not a ranking factor |
| T5 | No mixed content (http resources on https pages) | `B URL` then `grep -o -i -e 'src="http://[^"]*"' -e 'href="http://[^"]*"'` | Browsers block active mixed content, so scripts and styles silently fail |
| T6 | Server response time (TTFB) is low and stable | `curl -o /dev/null -sS -w '%{time_starttransfer}\n' URL`, five times | Slow or erratic servers get crawled less and delay LCP. Under about 0.8 s is a common target |
| T7 | Text responses are compressed | `curl -sI -H 'Accept-Encoding: br, gzip' URL` and read `content-encoding` | Smaller HTML and CSS means faster loads for the same content |
| T8 | No intermittent 5xx or 429 under light load | Request the same URL ten times at one per second; list status codes | Repeated server errors make crawlers slow down or back off |
| T9 | Bot protection does not block legitimate crawlers | Compare status and size for `UA` versus a search-engine UA string on one URL; any difference is a lead, not proof | A WAF that challenges crawlers removes pages from the index. Confirm real Googlebot behaviour in Search Console URL Inspection **[needs tool]** |

## 2. Status codes and redirects

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| R1 | Important pages return 200 | Status of every sampled URL | Anything else is not indexed as that page |
| R2 | A made-up URL returns 404 or 410, not 200 | `curl -s -o /dev/null -w '%{http_code}\n' https://host/zz-audit-$(date +%s)` | A 200 on junk URLs (a soft 404) wastes crawl budget and pollutes the index |
| R3 | Redirect chains are one hop | `curl -sSIL -o /dev/null -w '%{num_redirects} %{url_effective}\n' URL` | Each hop adds latency; Google follows a limited number of hops and may drop the rest |
| R4 | Permanent moves use 301 or 308; 302 and 307 only for temporary moves | Read the status of each hop in a chain | Permanent codes are a strong signal that the target is the canonical; temporary codes are a weak one |
| R5 | No redirect loops | `curl -sSIL --max-redirs 10 URL` ends in an error about redirects | A loop is an unreachable page |
| R6 | Internal links point at final URLs, not at redirecting ones | Extract internal `href`s from a page, request each without following | Every redirecting internal link adds a hop and signals sloppy structure |
| R7 | Removed pages go to an equivalent page or return 404/410, not to the home page | Test three known-removed URLs | Redirecting everything to the home page is treated as a soft 404 |
| R8 | Trailing-slash and letter-case variants redirect to one form | Request `/path` and `/path/`, and an upper-case variant | Otherwise each variant is a separate duplicate URL |
| R9 | Redirects are server-side, not meta refresh or JavaScript | Read the HTML for `http-equiv="refresh"` and `location.replace` | Meta and JS redirects are slower and weaker signals |
| R10 | The 404 page returns status 404 and links back into the site | Fetch the made-up URL from R2 and read both status and body | A helpful 404 keeps users; a 200 turns it into a soft 404 |

## 3. robots.txt

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| RB1 | `/robots.txt` returns 200 (a 404 means "allow everything") | `H https://host/robots.txt` | A 5xx or 429 is treated by Google as if the whole site were disallowed for a while |
| RB2 | No leftover `Disallow: /` for all agents on production | Read the file | A staging rule shipped to production removes the site from crawling |
| RB3 | CSS, JS and image paths needed for rendering are not blocked | Look for `Disallow` lines covering asset directories (`/assets/`, `/static/`, `/wp-content/`) | Blocked assets stop crawlers rendering the page as users see it |
| RB4 | Important sections are not disallowed; junk sections are | Match 10 sampled URLs against the rules by hand. Python's `urllib.robotparser` does not reliably implement the `*` and `$` pattern matching Google uses, so do not trust it for patterned rules | Over-blocking hides pages; under-blocking wastes crawl on search, cart and parameter URLs |
| RB5 | `Sitemap:` lines are present and absolute | Read the file | It is the standard way for every crawler to find the sitemap |
| RB6 | Syntax is valid and the file is small | One directive per line, groups start with `User-agent`, file under 500 KiB | Google ignores everything after 500 KiB |
| RB7 | Robots disallow is not used as a deindexing tool | Find disallowed URLs that are indexed or linked | A blocked URL can stay indexed without content; to remove a page, allow crawling and use `noindex` |
| RB8 | AI-crawler rules are deliberate | Read the AI user-agent blocks | Out of scope here; the AI-readiness audit covers it |

## 4. Indexability signals

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| I1 | No `noindex` on pages meant to rank | `B URL` then `grep -i -o -e '<meta[^>]*name=.robots.[^>]*>' -e '<meta[^>]*name=.googlebot.[^>]*>'` | A stray `noindex` is the most common cause of "my page is not indexed" |
| I2 | No `X-Robots-Tag: noindex` header | `H URL` and read `x-robots-tag`; repeat for PDFs and images | Headers override what the page source says and are invisible in the CMS |
| I3 | `noindex` and robots disallow are not combined on the same URL | Compare the two for noindexed URLs | A crawler cannot see a `noindex` on a page it may not fetch |
| I4 | `nofollow`, `nosnippet`, `max-snippet`, `noarchive` are intended | Read the meta robots and `X-Robots-Tag` values | `nosnippet` and a low `max-snippet` stop search and AI features from quoting the page |
| I5 | Staging and preview hosts are protected or `noindex` | Check the hosts the site links to or that appear in canonicals | Indexed staging copies compete with production |
| I6 | The launch did not carry a staging `noindex` into production | Check the home page, one category and one article | Frequent after migrations and redesigns |
| I7 | Pages listed in the sitemap are indexable | Cross-check 20 sitemap URLs for I1 and I2 | A sitemap that lists `noindex` URLs sends contradictory instructions |
| I8 | Index coverage and "crawled, not indexed" reasons **[needs tool]** | Search Console, Pages report | Only the search engine knows why it chose not to index a page |

## 5. Canonicals

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| C1 | Each indexable page has exactly one canonical, absolute, in the head | `grep -i -o '<link[^>]*rel=.canonical.[^>]*>'` and count results | Two canonicals, or a relative one, may be ignored |
| C2 | Unique pages are self-canonical | Compare the canonical with the final URL | Self-canonicals protect against parameter and tracking duplicates |
| C3 | The canonical target returns 200, is indexable, and does not redirect | Request the target; check I1 and I2 on it | A canonical pointing at a redirect or `noindex` page is ignored |
| C4 | The canonical uses the preferred protocol, host and slash style | Compare with T2, T3 and R8 | Mixed forms split signals |
| C5 | No canonical chains (A to B to C) | Follow the canonical of the canonical | Search engines may pick a different page than intended |
| C6 | Not canonicalised en masse to the home page or one hub | Compare canonicals across 10 different pages | Mass canonicals to one page are treated as errors and ignored |
| C7 | Paginated pages canonicalise to themselves | Check `?page=2` or `/page/2/` | Pointing page 2 at page 1 hides the items on page 2 |
| C8 | Parameter URLs canonicalise to the clean URL | Request the page with `?utm_source=x&sort=price` and read the canonical | Stops tracking and sort parameters becoming duplicates |
| C9 | Raw HTML and rendered HTML agree on the canonical | Compare the canonical in `curl` output with the rendered DOM (see J1) | A script that rewrites the canonical late gives crawlers two answers |

A canonical is a hint, not a directive. Report it as "the site asks for X", not "the page
will be indexed as X".

## 6. Sitemaps

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| S1 | A sitemap exists, returns 200, is valid XML and is listed in `robots.txt` | Fetch it; look for `<urlset>` or `<sitemapindex>` | It is the main discovery aid for new and deep pages |
| S2 | It lists only canonical, 200, indexable URLs | Sample 20 URLs; apply R1, I1, I2, C2 | A sitemap full of redirects and noindex pages teaches crawlers to distrust it |
| S3 | Each file has at most 50,000 URLs and 50 MB uncompressed; larger sites use an index | Count `<loc>`; check `Content-Length` | Files over the limit are truncated or rejected |
| S4 | URLs are absolute and match the canonical protocol and host | Read the `<loc>` values | Wrong-host entries are ignored |
| S5 | `<lastmod>` is accurate, in W3C date format | Compare `lastmod` with the page's real modified date for five URLs | Google uses `lastmod` only if it has been reliable; `priority` and `changefreq` are ignored |
| S6 | New and key pages are present | Compare the sitemap with the main navigation | Missing key templates are invisible to discovery |
| S7 | No sitemap URL is disallowed in `robots.txt` | Apply RB4 to a sample | Conflicting instructions |
| S8 | The sitemap is submitted and processed without errors **[needs tool]** | Search Console, Sitemaps report | Shows discovered versus indexed counts |

## 7. Architecture and internal links

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| A1 | Important pages are within about three clicks of the home page | Follow links from the home page to a sample of 10 key URLs | Deep pages are crawled less and receive less internal authority |
| A2 | Navigation and content links are real `<a href>` elements | `B URL` and count `<a ` with `href`; look for `onclick`-only, `href="#"`, `javascript:` | Crawlers follow `<a href>`; they do not click |
| A3 | Navigation is in the raw HTML | Is the menu present in `curl` output? | Menus injected by JavaScript may not be seen |
| A4 | No orphan pages (in the sitemap, linked from nowhere) **[needs tool]** | A crawl compared with the sitemap | Orphans rank poorly and are crawled rarely. With fetches only, test the 10 newest sitemap URLs for any inbound link on the home page and hubs |
| A5 | Internal links are not broken | Request every internal link on the sampled pages; list non-200 | Dead links waste crawl and frustrate users |
| A6 | Anchor text is descriptive | Read the anchors of the main nav and in-content links | Anchors tell crawlers what the target is about |
| A7 | Breadcrumbs exist on deep pages and match the URL hierarchy | Read one product or article page | Clarifies structure for users and engines |
| A8 | URLs are lowercase, hyphenated, free of session IDs, and stable | Read 20 URLs | Messy URLs create duplicates and fragile links |
| A9 | `rel="nofollow"` is not used on ordinary internal links | Search the nav HTML | It can stop the link passing signals to the target |

## 8. Duplicate content and URL hygiene

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| D1 | Protocol and host variants collapse to one URL | Run T2 and T3 | Four live versions of every page is the textbook duplicate |
| D2 | `index.html`, `index.php` and `default.aspx` variants redirect to the folder | Request `/index.html` | Another silent duplicate of the home page |
| D3 | Tracking and sort parameters do not create indexable duplicates | Request `?utm_source=x`, `?sort=price`, `?sessionid=1`; read canonical and meta robots | Parameter duplicates multiply crawl and split signals |
| D4 | Templated pages have distinct titles, H1s and body text | Compare the titles and H1s of 20 pages from one template | Near-identical pages compete with each other |
| D5 | Syndicated or copied content points to the original or is differentiated | Search a distinctive sentence from a page, if a search tool is available | Copies without a canonical can outrank the original |
| D6 | Separate mobile or print URLs have the right annotations | Look for `m.` hosts, `/print/` URLs, `rel="alternate"` | Unannotated variants are duplicates |
| D7 | Tag, category and author archives do not overlap and are not thin | Open three archive pages | Thin archives dilute the index |

## 9. Pagination and facets

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| P1 | Each page of a series has its own crawlable URL linked with `<a href>` | Open a listing, find "next" and page numbers in the raw HTML | Items on later pages are only discoverable through those links |
| P2 | "Load more" and infinite scroll fall back to paginated URLs | Check the HTML for page links beside the script | Crawlers do not scroll or click |
| P3 | Page 2 onward is self-canonical and has a distinct title | Apply C7; compare titles | Prevents duplicate titles and hidden items |
| P4 | `rel="next"` and `rel="prev"` are not relied on | Note their presence | Google stopped using them as an indexing signal; they are harmless but do not fix a structure problem |
| P5 | Faceted navigation cannot create unlimited URLs | Click or construct three filter combinations; are they crawlable, canonical, blocked? | Unbounded combinations are a crawl trap |
| P6 | No crawl traps (calendars, relative-link loops, endless parameters) | Look for `next month` chains, repeated path segments such as `/a/b/a/b/` | Crawlers can spend their whole visit in a trap |

## 10. hreflang

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| H1 | Annotations exist in one place only: head tags, HTTP headers or the sitemap | `grep -i -o '<link[^>]*hreflang[^>]*>'`; check the sitemap for `xhtml:link` | Mixing methods invites conflicts |
| H2 | Every alternate links back (return tags) | Fetch the page at each alternate URL and confirm it lists the first page | One-way annotations are ignored |
| H3 | Each page lists itself | Look for its own URL and language in its set | Required for a complete set |
| H4 | Codes are valid: ISO 639-1 language, optional ISO 3166-1 alpha-2 region | Read the codes: `en-GB` is valid, `en-UK` is not | Invalid codes are ignored |
| H5 | Every alternate returns 200, is canonical, is indexable, and is absolute | Apply R1, C2 and I1 to each | Alternates that redirect or noindex break the set |
| H6 | `x-default` is present where there is a language picker or fallback | Read the set | Tells engines which page to use for unmatched users |
| H7 | `<html lang>` matches the page's real language | Read the `lang` attribute | A wrong value contradicts the annotations |
| H8 | Visitors are not force-redirected by IP or `Accept-Language` | Request with different `Accept-Language` headers and compare | Crawlers that arrive from one location may never see the other versions |

## 11. Mobile

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| M1 | A viewport meta tag is present | `grep -i -o '<meta[^>]*name=.viewport.[^>]*>'` should contain `width=device-width` | Without it, mobile browsers render a shrunken desktop page |
| M2 | Mobile and desktop serve the same content, links, canonical, robots and structured data | `B` with `UA` and with `MOBILE`; compare word counts, link counts, canonicals | Google indexes the mobile version first; content missing there is missing from the index |
| M3 | Content does not depend on scroll or click events to load | Check lazy-loading code for `IntersectionObserver` or native `loading="lazy"` versus scroll listeners | Crawlers do not scroll |
| M4 | No full-screen interstitial covers content on arrival **[needs tool]** | Load the page in a mobile emulator | Intrusive interstitials are a documented negative page-experience signal |
| M5 | Tap targets and text size are usable **[needs tool]** | Lighthouse or a device | Poor mobile usability loses users before any ranking effect |

## 12. JavaScript rendering

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| J1 | Title, H1, main text, internal links, canonical, meta robots and structured data are in the raw HTML | `B URL` and look for them. An empty `<div id="root">` or `id="__next"` with little text signals client-side rendering | Crawlers that do not run scripts see only the raw HTML |
| J2 | Rendered output matches raw HTML for the signals in J1 **[needs tool]** | Compare `curl` with the rendered DOM from a browser tool, the Rich Results Test, or Search Console URL Inspection | Differences show what depends on rendering |
| J3 | Links are `<a href>`; routes are real paths, not `#` fragments | Apply A2; look for `/#/` in links and the address bar | Client routers must expose real URLs, because crawlers ignore everything after `#` |
| J4 | Error routes return real 404 status codes | Fetch the R2 URL and read the status, not the page text | A single-page app that returns 200 for everything creates soft 404s |
| J5 | Content behind tabs and accordions is in the DOM on load | Look for the hidden text in the raw HTML | Content that loads only on click is not indexed |
| J6 | JS and CSS are not blocked (RB3) and load without errors | Apply RB3; check the console in a browser tool | Rendering fails if assets fail |
| J7 | Do not assume AI fetchers render JavaScript | Compare J1 results | Most AI crawlers are not documented to execute scripts, so server-rendered content is the safe choice |
| J8 | Critical tags are not injected late by scripts | Compare head tags in raw versus rendered HTML | Late injection is processed unreliably and by fewer crawlers |

## 13. Performance and Core Web Vitals

Field data is the source of truth. What a plain fetch can and cannot do is stated in the
skill's Step 8.

| ID | Check | How to check | Why it matters |
| --- | --- | --- | --- |
| W1 | Core Web Vitals pass at the 75th percentile on mobile and desktop: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less **[needs tool]** | PageSpeed Insights (field section), the CrUX API or dashboard, Search Console Core Web Vitals report | These are the thresholds Google uses; lab numbers do not replace them |
| W2 | HTML is small and compressed | `curl -sS -o /dev/null -w '%{size_download}\n' -H 'Accept-Encoding: gzip' URL` | Large documents delay first paint |
| W3 | Render-blocking scripts in the head are few | Count `<script src` in `<head>` without `async`, `defer` or `type="module"` | Each one delays rendering |
| W4 | The likely LCP image is preloaded, high priority and not lazy | Find the first large `<img>` or CSS hero; look for `fetchpriority="high"`, `loading="lazy"` | A lazy-loaded hero is a common cause of a slow LCP |
| W5 | Images are modern formats, sized to the layout, with `width` and `height` | List `<img>` attributes; `curl -sI` each image for `content-length` and `content-type` | Oversized images dominate transfer; missing dimensions cause layout shift |
| W6 | Fonts use `font-display` and critical fonts are preloaded | Read `@font-face` rules and `<link rel="preload">` | Late fonts cause invisible text or shifts |
| W7 | Third-party script load is limited | List external hosts in `<script src>` and `<iframe>` | Tags and widgets are a leading cause of slow INP and long tasks |
| W8 | Static assets are cacheable | `curl -sI` a hashed asset and read `cache-control` | Repeat visits and CDN hits depend on it |
| W9 | Space is reserved for ads, embeds and banners **[needs tool]** | Watch the page load in a browser with layout-shift highlighting | Late-inserted content moves what the user is reading |
| W10 | Interaction latency (INP) is acceptable **[needs tool]** | Field data in CrUX; lab profiling in a browser | INP needs real interactions; it cannot be fetched |

## 14. Adjacent checks (note, then hand off)

| ID | Check | Where it goes |
| --- | --- | --- |
| O1 | Titles and meta descriptions exist and are unique across the sample | `on-page-seo` |
| O2 | Structured data is present and valid | `schema-markup` |
| O3 | AI crawler rules, `llms.txt`, citability | `geo-audit`, `llms-txt` |
| O4 | Image alt text and heading structure | `on-page-seo` |
