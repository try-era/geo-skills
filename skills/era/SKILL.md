---
name: era
description: Entry point for Era's GEO and SEO skills. Use when the user asks what can be done for a brand or site in AI search, mentions GEO, AEO or AI visibility without naming a specific task, or wants a plan that chains several steps (audit, keywords, content calendar, review, publish). Checks the Era connection and routes to the right skill.
argument-hint: [brand or url] [what you want]
---

# Era — router

Turn a loose request ("how do we show up in ChatGPT?", "do something for acme.com") into the
right skill, or the right sequence of skills, and make sure Era is reachable before any
data-backed step runs.

## When to use

- The user names a brand or a URL and a goal, but not a method.
- The user asks what this plugin can do.
- A job spans several skills (for example "audit the site, then plan content").

When the user already names a task ("audit this page", "approve next week's topics"), skip the
router and run that skill directly.

## Inputs

Ask only for what is missing:

- **Subject** — a brand name (resolved through Era) and/or a URL (works without Era).
- **Goal** — one of: *see where we stand*, *beat a competitor*, *find what to write*, *fix a
  page*, *run the calendar*, *ship content to our site*.
- **Window** — days of data for reporting; default 30.

## Steps

1. **Check the connection.** Call `whoami`. If it fails or the `era` MCP server is missing,
   say so once, give the one-line fix, and continue with the skills that work on public
   pages only:

   ```bash
   claude mcp add --transport http era https://app.tryera.ai/api/mcp
   ```

   For automation without a browser sign-in, an API key works instead:
   `--header "Authorization: Bearer $ERA_API_KEY"`. Never ask the user to paste a key into
   the chat.
2. **Resolve the brand.** Call `list_brands`. Match the user's name against brand names and
   websites. One match: use its `brand_id` and say which brand you picked. Several: ask.
   None: the data skills are off the table for this brand; offer the public-page skills.
3. **Pick the route** with the table below. Say in one sentence which skill(s) you will run
   and why, then run them. Chain at most four skills in one go; after that, stop and report.
4. **Hand off.** Each skill produces its own deliverable. When chaining, pass forward only
   what the next skill needs (brand_id, the gap list, the chosen keyword cluster), not the
   whole previous report.

## Routing table

| The user wants… | Run | Needs Era |
| --- | --- | :---: |
| to know how the brand is doing in AI answers | `ai-visibility-report` | ✓ |
| to know why a competitor is named and they are not | `competitor-gap` | ✓ |
| to know which sites the engines trust in their category | `citation-sources` | ✓ |
| keywords or demand for AI search | `ai-keyword-research` | ✓ |
| a page that AI engines will quote | `answer-engine-content` | optional |
| to know how engines read a URL / a GEO or AEO audit | `geo-audit` | optional |
| an `llms.txt` | `llms-txt` | — |
| a brief for an article | `content-brief` | ✓ |
| to see, rename, approve or pause planned articles | `content-calendar` | ✓ |
| to edit a generated article before it goes out | `article-review` | ✓ |
| articles delivered to a hand-built site | `publish-to-site` | ✓ |
| crawl, index, speed, canonical or sitemap problems | `technical-seo-audit` | — |
| JSON-LD / structured data | `schema-markup` | — |
| title, meta, headings, internal links for one page | `on-page-seo` | — |

Common chains:

- **Where do we stand** → `ai-visibility-report` → `competitor-gap` → `citation-sources`.
- **What should we write** → `competitor-gap` → `ai-keyword-research` → `content-brief`.
- **Fix a page** → `geo-audit` → `on-page-seo` → `schema-markup` → `answer-engine-content`.
- **Run the machine** → `content-calendar` → `article-review` → `publish-to-site`.

## Output

When routing, keep it to three lines: the brand/URL you resolved, the skill(s) you are
running, and anything the user must decide first (a window, a spend). The chained skills then
print their own reports in order. Finish with a short "next steps" list: the skills that
would be useful next and why.

## Guardrails

- Never start a skill that spends money or allowances (`approve_topics`, keyword volume
  checks, Suggest, test articles) from the router. Route to the owning skill, which asks.
- Never guess a `brand_id`; never run a data skill against a brand you could not resolve.
- If `whoami` reports a read-only key and the chosen skill needs write access, say so before
  starting rather than failing halfway.

## Era tools used

- `whoami` (read) — connection and scope check.
- `list_brands` (read) — brand resolution.

## Without Era

Route to `geo-audit`, `llms-txt`, `technical-seo-audit`, `schema-markup`, `on-page-seo` and
`answer-engine-content`. Mention once that the reporting and calendar skills need an Era
workspace, and move on.
