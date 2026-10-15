---
name: llms-txt
description: Generate and validate llms.txt and llms-full.txt for a website. Reads the sitemap and navigation, picks canonical evergreen pages, writes one-line descriptions from the pages' own content, and checks an existing file for dead links, redirects, duplicates and structure errors. Use when the user asks for an llms.txt, llms-full.txt, or to make a site readable for LLMs and AI agents.
argument-hint: <site-url> [--validate] [--full]
---

# llms.txt

Produce a short, curated `llms.txt` (and, when asked, an `llms-full.txt`) that tells an AI
agent what a site is and which pages to read first, built from the site's real structure
and checked link by link. For an existing file, report what is wrong and give the fixed
version.

## When to use

- "Create an llms.txt", "write llms-full.txt", "make our docs readable by AI agents".
- "Check / fix our llms.txt", or after a redesign or migration that moved URLs.
- A `geo-audit` finding says `llms.txt` is missing or malformed.

Not for: whether AI crawlers can reach the site, or an overall AI-readiness score
(`geo-audit`); sitemap, robots and canonical problems found along the way
(`technical-seo-audit`); rewriting pages whose purpose cannot be described in one line
(`answer-engine-content`).

**Set expectations once.** `llms.txt` is a proposal published at llmstxt.org, not a
standard. At the time of writing, no major search or answer engine has documented that it reads the file to rank
or cite pages; it is read today by agents and developer tools that fetch documentation on
demand. Say so, then do the work: the file is cheap to produce and harmless to publish.
To test whether it matters on this site, check the server logs 30 days after publishing
for requests to `/llms.txt` from AI user-agents such as `OAI-SearchBot`, `ChatGPT-User`,
`Claude-User`, `PerplexityBot` and `Perplexity-User`.

## Inputs

- **Site URL** — the origin, for example `https://example.com`. Use the canonical host
  (the one the home page redirects to).
- **Mode** — generate (no file yet), validate (a file exists), or both. Find out by
  fetching `/llms.txt`; do not ask the user what you can read.
- **Full file?** — ask whether they want `llms-full.txt`. Default: yes for documentation
  sites, no for marketing sites.
- **Priorities** (optional) — sections that must be in, pages that must stay out, the
  language to cover if the site is multilingual.

## Steps

1. **Fetch what exists.** `GET /llms.txt`, `/llms-full.txt`, `/robots.txt` (read the
   `Sitemap:` lines) and the sitemap. For each file record status, final URL, content
   type and size. A `200` with `text/html` for `/llms.txt` means the server returns its
   app shell for unknown paths: treat the file as missing and say why.
2. **Collect candidates.** Read every URL from the sitemap, following sitemap index files.
   Add the links from the home page header, footer and, for docs, the sidebar. With a
   shell, run `scripts/llms_txt_skeleton.py <sitemap-url>`: it prints a draft grouped by
   first path segment with titles and meta descriptions, and lists on stderr what it
   dropped and why. Without a shell, fetch the sitemap and the key pages with the web
   tool and build the same grouping by hand. The draft is raw material, not the answer.
3. **Select pages.** Keep a page only if it passes every test; record the first test it
   fails for the exclusion table.

   | Test | Exclude when |
   | --- | --- |
   | Canonical | it redirects, or its canonical points elsewhere |
   | Reachable | status is not 200, or it needs a login |
   | Indexable | `noindex` in the meta tag or `X-Robots-Tag` |
   | Evergreen | it is dated news, an expired event, a time-limited campaign |
   | Substantive | fewer than about 150 words of unique content, or a pure listing |
   | Distinct | another selected page covers the same question better |
   | Useful to an agent | tag, author or archive pages, pagination, search, cart, thank-you |

   Prefer hubs (a docs home, a pricing page, a products index) over every leaf. Prefer
   pages that state facts: limits, prices, specifications, definitions, procedures.
4. **Fetch the selected pages** and read each one's title, H1, meta description and first
   paragraph. Note duplicates: pages that share one `<title>` or description (common on
   templated sites) need a description written from the body, and the duplication is a
   finding for `on-page-seo`.
5. **Write the file** in this order, following `references/llms-txt-format.md`:
   - `# Site name` — the name the site uses for itself.
   - `> Summary` — one to three sentences: what it is, who it is for, what the file
     covers. Facts only.
   - Optional free paragraph — only facts an agent would get wrong: current version,
     currency, API base URL, supported regions.
   - `## Sections` ordered by importance, each item `- [Page name](absolute-url): note`.
   - `## Optional` last, for secondary material (blog hub, changelog, legal).

   A note says what the reader will find, in at most about 160 characters, from the page's
   own words. No "comprehensive", "powerful", "best". If the page does not say what it
   is for, write the note from its H1 and first paragraph and flag the page.
6. **Markdown versions.** For each selected URL, request `<url>.md`. If it returns 200
   with Markdown, link that instead and say so. If not, link the HTML page. Never invent
   a `.md` URL.
7. **Build `llms-full.txt`** (if asked). For each link in the main sections, in file order,
   fetch the page, keep the main content only, convert to Markdown, demote headings, and
   write a block: page title, `Source:` line, body, separator. Leave `## Optional` out
   unless asked. Count characters and estimate tokens (characters / 4). Above about
   200,000 tokens, split by section and link the split files from `llms.txt`.
8. **Validate** the result with the checks V1–V16 in `references/llms-txt-format.md`. Fetch
   every linked URL and confirm status, redirects and canonical. Fix and re-run until no
   error remains. For an existing file, run the same checks on it first and report them
   before showing the new version.
9. **Placement and upkeep.** The file goes at `/llms.txt` on the canonical host root,
   served `text/plain; charset=utf-8` (or `text/markdown`), status 200, no redirect, not
   blocked in `robots.txt`. Give the user the exact path or CMS step if the platform
   is known (a static file in `public/`, a route in the framework, a plugin setting).
   Recommend regenerating it from the sitemap in the build, or reviewing it whenever pages
   are added, removed or renamed; a quick check is that every listed URL is still in the
   sitemap.

## Output

Generate mode:

```
llms.txt — {site}
Summary: {N} pages listed in {M} sections · {K} excluded · {W} words of notes
Existing file: none / present (see validation)
Verdict: {one sentence — e.g. "Ready to publish; 3 descriptions are inferred and marked."}
```

Then, in this order:

1. **The file** in a fenced `markdown` block, ready to paste, with no working notes
   inside it. List the entries whose note was inferred from thin content in a line under
   the block, so the user can check them.
2. **Pages table** — url · decision (included / excluded) · reason. Cover every URL the
   script or sitemap pass considered; group long exclusion runs (for example, 40 tag
   pages) into one row with the count.
3. **llms-full.txt** (if built) — size in characters and estimated tokens, whether it was
   split, and the first block in a fenced block as a sample. Offer the full text as a file
   rather than pasting it.
4. **Placement** — path, content type, and the check that confirms it is live
   (`curl -sSI https://host/llms.txt`).

Validate mode:

```
llms.txt validation — {site}
Verdict: valid / valid with warnings / broken
Errors {n} · Warnings {n} · Info {n}
```

- **Checks table** — ID · check · result · evidence (the status code, the line, the URL)
  · fix. Only failing and warning checks get a row; list passing IDs in one line.
- **Dead and redirected links** — url · status · where it redirects · replacement from the
  sitemap, if one exists.
- **Coverage** — important sitemap pages missing from the file (pricing, docs hub, about)
  and listed pages missing from the sitemap.
- **The corrected file** in a fenced block, with a short list of what changed.

## Guardrails

- Fetch only URLs the user gave, the sitemap lists, or that the pages themselves link to
  within the same site. The only URLs you construct are `/llms.txt`, `/llms-full.txt`,
  `/robots.txt` and `<listed-url>.md`. Never log in, submit forms or fetch gated pages.
- Every description is derived from the page. Do not add features, prices, numbers or
  claims the page does not state.
- The file is public. Do not list staging hosts, admin paths, private documents or
  anything behind a login, and warn the user if the sitemap lists some.
- Do not overwrite the user's file. Produce the new content and the placement step; the
  user publishes it.
- Do not promise ranking, citation or traffic gains. The honest claim is "a curated map
  for agents that read it"; the test is the log check above.
- A listed URL is not protected or promoted by being listed, and an omitted one is not
  blocked. Access control belongs in `robots.txt` and server rules.

## Era tools used

None. This skill works on public pages only and needs no Era account.

## Hand-offs

- `geo-audit` — whether AI crawlers can reach the site, and the wider AI-readiness score.
- `technical-seo-audit` — when validation finds sitemap, canonical or redirect problems
  that go beyond this file.
- `answer-engine-content` — for pages that cannot be summarised in one line because they
  never say what they are.
