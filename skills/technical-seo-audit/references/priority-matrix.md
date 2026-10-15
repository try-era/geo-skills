# Priority matrix: impact x effort

Every finding gets one impact level and one effort level. The pair decides the fix order.
Both are judgements, so each rule below says what evidence moves a finding up or down.

## Impact

Impact is **severity x scope**, raised one level when revenue pages are involved.

| Severity | Meaning | Points |
| --- | --- | ---: |
| Blocks | The page cannot be crawled, rendered, or indexed (noindex, robots disallow, 5xx, empty raw HTML) | 3 |
| Degrades | The page is indexed but weakened (duplicate, slow, wrong canonical, wasted crawl, broken signals) | 2 |
| Hygiene | Correct but untidy; little measurable effect (missing HSTS, a few redirect hops) | 1 |

| Scope | Meaning | Points |
| --- | --- | ---: |
| Site | Every page, or every template | 3 |
| Template | One important template or section (products, articles, docs) | 2 |
| Few URLs | A handful of pages | 1 |

| Product | Impact |
| ---: | --- |
| 9 | **Critical** |
| 6 | **High** |
| 3 to 4 | **Medium** |
| 1 to 2 | **Low** |

Adjustments:

- Raise one level when the affected URLs are revenue or conversion pages (pricing, product,
  sign-up, checkout) or the pages that currently earn the most organic traffic.
- Lower one level, and say why, when the finding is **inferred** rather than observed. A
  finding is observed only if the evidence column holds a status code, a header, a tag or
  a count that was actually fetched. Never list an inferred finding as Critical.
- A finding that cannot be checked without a tool (for example Core Web Vitals field data)
  is not scored. It goes in "Could not check" with the tool that answers it.

## Effort

| Level | Meaning | Typical work |
| --- | --- | --- |
| S | Under half a day, one person, no release | A robots.txt line, a CMS setting, a header rule, a redirect rule, removing a plugin |
| M | One to a few days, a developer, a normal release | Template changes (canonicals, hreflang), server-side rendering for one route, image pipeline changes |
| L | A sprint or more, several teams, or a migration | Replatforming, moving a client-rendered site to SSR, restructuring URLs, rebuilding faceted navigation |

## The grid, with examples

| | Effort S | Effort M | Effort L |
| --- | --- | --- | --- |
| **Critical** | `noindex` or `Disallow: /` shipped to production; robots.txt returning 5xx; the staging password wall on the live host | A migration with no redirect map, leaving old URLs as 404; a framework configured for client-only rendering that supports server rendering | A client-rendered app with an empty raw HTML shell that needs a front-end rewrite to render on the server |
| **High** | A canonical on every page pointing at the home page; the sitemap listing only redirecting URLs; HTTP not redirected to HTTPS; robots rules blocking CSS and JS | hreflang without return tags across all locales; soft 404s on a whole template; faceted navigation generating unlimited crawlable URLs | Core Web Vitals failing across most templates because of the front-end architecture |
| **Medium** | Redirect chains of two or three hops on a few key URLs; stale `lastmod` values; a missing canonical on one template | Internal links pointing at redirecting URLs sitewide; missing `width` and `height` on images causing layout shift; duplicate parameter URLs without canonicals | Deep pages more than five clicks from home across a large section |
| **Low** | Missing HSTS; a trailing-slash variant that returns 200 on two pages; an unused sitemap file | Moving to HTTP/3; self-hosting fonts for a small LCP gain | Rewriting every legacy URL to a cleaner pattern when no problem has been measured |

## Fix order

1. **Critical, regardless of effort.** Anything that blocks crawling or indexing of
   important pages is fixed before everything else. Order within the group by scope.
2. **Quick wins: High or Medium impact with Effort S.** They are cheap, and they unblock
   the verification of later fixes.
3. **High impact, Effort M or L.** Schedule them; give each an owner and a way to verify.
4. **Medium impact, Effort M or L.** Backlog, ordered by how many revenue pages benefit.
5. **Low impact.** Do them only when they are Effort S or ride along with other work on
   the same template.

Dependencies override the order above. Fix in this sequence when findings overlap:

1. Access: robots.txt, status codes, server errors, bot protection.
2. Rendering: raw HTML content, links, real status codes on error routes.
3. Indexation signals: noindex, canonicals, redirects, URL variants.
4. Discovery: sitemaps, internal links, pagination, hreflang. The sitemap and hreflang
   list final canonical URLs, so they come after redirects and canonicals.
5. Performance and Core Web Vitals, measured again after the structural fixes, because
   rendering and image changes often move the numbers on their own.
6. Hygiene.

## How to verify each fix

Every fix in the report states the check that proves it. Reuse the original command and
show the before and after.

| Fix | Verify with |
| --- | --- |
| robots.txt change | Fetch `/robots.txt`; match three sampled URLs against the rules |
| noindex removed | `curl` the page; the meta tag and `x-robots-tag` header are absent. Then Search Console URL Inspection and "Request indexing" if the user has access |
| Redirect rule | `curl -sSIL -o /dev/null -w '%{num_redirects} %{http_code} %{url_effective}\n' URL` shows one hop and a 200 |
| Canonical template | Fetch five URLs from the template; the canonical equals the final URL |
| Sitemap clean-up | Sample 20 sitemap URLs; all return 200, are indexable and self-canonical |
| hreflang | Fetch two pages of a set; each lists the other and itself |
| Server-side rendering | `curl` shows the H1, main text and links without running scripts |
| Core Web Vitals | Field data only moves after real users have visited for about 28 days (the CrUX window); say so, and use a lab run as an early check |

A fix is "verified" only when the command output is shown. Otherwise write "shipped, not
yet verified".
