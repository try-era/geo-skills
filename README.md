# Era GEO Skills for Claude Code

**GEO (Generative Engine Optimization) and SEO skills for [Claude Code](https://claude.ai/claude-code), by [Era](https://tryera.ai).** Fourteen skills that audit how AI answer engines see a site, pull real AI-visibility data from Era, research AI-search demand, write content that gets cited, and run a content calendar end to end — plus a router that picks the right one.

[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-blue)](https://code.claude.com/docs/en/plugins)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-14%20%2B%20router-8A2BE2)](skills/)
[![Era MCP](https://img.shields.io/badge/Era-MCP%20server-00A67E)](https://app.tryera.ai/docs/mcp/overview)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Why this exists.** Search is splitting in two: classic SEO still decides who ranks on Google, and GEO decides who gets *named and cited* when someone asks ChatGPT, Perplexity, Gemini or Claude. Most SEO skill packs stop at the first half. This one covers both, and the GEO half runs on measured data — which prompts mention you, which competitors win, which sources the engines trust — instead of guesses.

## Install

### Claude Code (plugin, recommended)

```bash
/plugin marketplace add try-era/geo-skills
/plugin install era-geo@try-era
```

The plugin bundles the Era MCP server. The first time a skill needs your data, Claude Code opens a browser window — sign in with your Era account and click **Allow**. There is no key to copy. Skills that audit public pages work without an Era account at all.

### Cursor, Codex, VS Code and other agents

Skills follow the open [Agent Skills](https://agentskills.io) format, so any client that reads `SKILL.md` can use them:

```bash
npx skills add try-era/geo-skills
```

Then connect the Era MCP server once (OAuth, no headers needed):

```json
{ "mcpServers": { "era": { "url": "https://app.tryera.ai/api/mcp" } } }
```

Client-specific snippets are in [Era's docs](https://app.tryera.ai/docs/mcp/connect).

### Manual

Copy any directory from `skills/` into `~/.claude/skills/` (or your project's `.claude/skills/`). Each skill is self-contained.

## Quick start

```text
/era-geo:era                                  # what can you do for acme.com?
/era-geo:geo-audit https://acme.com/pricing   # how do AI engines read this page?
/era-geo:ai-visibility-report Acme 30         # last 30 days: visibility, share of voice, sentiment, citations
/era-geo:competitor-gap Acme                  # which prompts do competitors win, and why
/era-geo:content-calendar Acme                # what is queued, what needs approval
```

Or just describe the job — *"why does Perplexity never mention us for 'best CRM for agencies'?"* — and Claude picks the skill.

## The skills

| Skill | What it does | Era data |
| --- | --- | :---: |
| `era` | Router. Understands the request, checks the Era connection, hands off to the right skill or chains several. | — |
| **AI visibility** | | |
| `ai-visibility-report` | Executive report for one brand: visibility, share of voice, sentiment, position and top citations per engine, with charts and a plain-language read of what moved. | ✓ |
| `competitor-gap` | Prompt-by-prompt comparison against tracked competitors: where they are named and you are not, what the engines said instead, and the content that would close each gap. | ✓ |
| `citation-sources` | The domains and URLs AI engines cite about your category, split into yours / competitors' / third-party, turned into a placement and PR shortlist. | ✓ |
| `ai-keyword-research` | AI-search keyword research on Era's measured AI volumes: clusters, intent, gaps versus Google volume, and what to add to the Keywords Database. | ✓ |
| `answer-engine-content` | Writes or rewrites a page so engines can lift it into an answer: direct answers first, quotable statistics, named sources, entity-dense headings. Uses the brand kit and tone of voice when Era is connected. | optional |
| **GEO on any site** | | |
| `geo-audit` | Audits a page or site for AI readiness: AI-crawler access in `robots.txt`, `llms.txt`, structured data, answer-shaped content, citability, freshness and author signals. Scored, with fixes. | optional |
| `llms-txt` | Generates and validates `llms.txt` and `llms-full.txt` from a site's real structure. | — |
| **Content calendar** | | |
| `content-brief` | Brief for one article from a keyword cluster, the competitor pages that currently win, and the brand kit — outline, entities, questions to answer, sources to cite. | ✓ |
| `content-calendar` | Reads the Era content calendar, explains what is queued, renames or approves topics (with the cost stated first), starts or pauses the workflow. | ✓ |
| `article-review` | Pulls a generated article with the brief behind it, reviews it for GEO, SEO and E-E-A-T, proposes a rewrite as a diff and applies it only after approval. | ✓ |
| `publish-to-site` | Connects a hand-built site as a Custom site destination (webhook or pull), verifies the handshake, and hands the dev the endpoint contract. | ✓ |
| **Classic SEO** | | |
| `technical-seo-audit` | Crawlability, indexability, canonicals, redirects, sitemaps, Core Web Vitals, hreflang — prioritised by impact. | — |
| `schema-markup` | Generates and validates JSON-LD (Organization, Product, Article, FAQ, HowTo, Breadcrumb…) tuned for both rich results and AI extraction. | — |
| `on-page-seo` | Title, meta, headings, internal links, image alt text and content gaps for one page against its target query. | — |

**Era data** ✓ = reads your workspace through the Era MCP server · *optional* = better with Era, works without · — = works on any public site.

## How the Era connection works

- **What it reads.** Era runs your monitoring prompts against ChatGPT, Claude, Gemini, Google AI, Perplexity and Grok on a schedule and stores every answer. The skills read the roll-ups (visibility, share of voice, sentiment, position, citations, search queries) and drill into the verbatim answers when a number needs explaining.
- **Read vs write.** Reporting skills only read. Calendar and keyword skills write — they need a write-scoped connection and they tell you before they change anything.
- **Money and allowances.** Approving a topic is a paid article generation; keyword volume checks and Suggest runs have monthly allowances. Every skill states the cost and waits for a yes. Nothing is approved, archived, deleted or published silently.
- **Without the plugin.** Any Streamable-HTTP MCP client can connect to `https://app.tryera.ai/api/mcp`. Automation can use an API key instead of OAuth: `Authorization: Bearer era_…` for MCP, `X-API-Key: era_…` for the REST API at `https://app.tryera.ai/api/v1` ([docs](https://app.tryera.ai/docs)).

A tool-by-tool reference of the MCP server is in [`docs/era-mcp-reference.md`](docs/era-mcp-reference.md).

## A typical week

1. `ai-visibility-report` on Monday — what moved, on which engine, and why.
2. `competitor-gap` — the prompts worth fighting for this week.
3. `ai-keyword-research` — turn those prompts into keywords Era can measure and plan from.
4. `content-calendar` — approve the next batch of topics with the cost in front of you.
5. `article-review` on each article in the editing window, then `publish-to-site` if your blog is hand-built.
6. `geo-audit` and `schema-markup` on the pages that got published.

## Requirements

- Claude Code 1.0.33 or newer for the plugin install path; any Agent-Skills-compatible client for the manual path.
- An Era workspace for the data-backed skills. Analytics skills work on every plan; the content-calendar skills need the Content plan.
- Audit and writing skills need nothing but a URL.

## Repository layout

```
.claude-plugin/   plugin.json and marketplace.json
.mcp.json         the bundled Era MCP server
skills/           one directory per skill, SKILL.md inside
agents/           subagents the router can fan out to
docs/             MCP tool reference and the authoring guide
```

## Contributing

Issues and pull requests are welcome. Read [`docs/AUTHORING.md`](docs/AUTHORING.md) first — it defines the skill anatomy, the Era conventions (brand resolution, spend guards, wording) and the pre-commit checklist. Run `claude plugin validate .` before opening a PR.

## License

[MIT](LICENSE) © 2026 Era.
