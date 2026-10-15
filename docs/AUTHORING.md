# Authoring guide

How every skill in this repository is written. Read it before adding or editing a skill.

## Anatomy

```
skills/<skill-name>/
├── SKILL.md            # required — the skill itself
├── references/         # optional — checklists, templates, specs the skill reads on demand
└── scripts/            # optional — small, dependency-free helpers (bash/python) the skill may run
```

- One directory per skill, `kebab-case`, same string as the `name` in the frontmatter.
- `SKILL.md` is 100–260 lines. Anything longer belongs in `references/` and is loaded only
  when the step needs it — Claude reads SKILL.md in full every time the skill triggers,
  so keep it lean.
- Every skill is **self-contained**: it must work when copied alone into
  `~/.claude/skills/<name>/` (that is how `npx skills add` installs it). Never link to a
  file in another skill's directory.

## Frontmatter

```yaml
---
name: geo-audit
description: Audit a page or site for AI-search readiness — citability, AI-crawler access, llms.txt, structured data, answer-shaped content. Use when the user asks how ChatGPT, Perplexity, Gemini or Claude see a URL, or wants a GEO / AEO audit.
argument-hint: <url> [--site]
---
```

- `description` is what makes the skill trigger. Write it as *what it does* + *when to use
  it* in third person, include the words users actually say (GEO, AEO, AI search, ChatGPT,
  Perplexity, citations…). 1–3 sentences, under 400 characters.
- `argument-hint` shows in the slash-command palette. Keep it short.
- No other frontmatter keys unless a skill needs `allowed-tools`.

## Section order inside SKILL.md

1. **One-line summary** of the outcome.
2. **When to use / when not to** (2–4 bullets, name the sibling skill for the "not" cases).
3. **Inputs** — what to ask for if missing (brand name, URL, window in days…). Never guess a
   `brand_id`: get it from `list_brands`.
4. **Steps** — numbered, each step says which tool it calls and what to do with the result.
5. **Output** — the exact shape of the deliverable (headings, tables). Lead with a 5-line
   summary, then detail. Findings carry evidence (the number, the quote, the URL).
6. **Guardrails** — spend, destructive actions, what never to claim.
7. **Era tools used** — bullet list of tool names, read vs write.
8. **Without Era** (data skills only) — what the skill can still do from public pages.

## Era conventions

- The data layer is the **Era MCP server** (`https://app.tryera.ai/api/mcp`, bundled with the
  plugin as `.mcp.json`). Call tools by name: `list_brands`, `get_brand_dashboard`,
  `get_share_of_voice`, `list_cited_domains`, … The full catalogue is in
  [`docs/era-mcp-reference.md`](era-mcp-reference.md).
- If the MCP server is not connected, tell the user how to connect (`claude mcp add
  --transport http era https://app.tryera.ai/api/mcp`) **or** fall back to the REST API:
  `https://app.tryera.ai/api/v1/...` with header `X-API-Key: era_…` (read from the
  `ERA_API_KEY` environment variable; never ask the user to paste a key into chat).
- Always begin with `list_brands` to resolve the brand the user names into a `brand_id`.
  If several brands match, ask.
- Default analytics window: `days=30`. Say the window in the output.
- **Spend guards** — some write tools cost money or a monthly allowance. The skill must
  state the cost and get an explicit "yes" before calling:
  - `approve_topics` — every approved topic is one paid article generation; at most 10 per call.
  - `add_keywords` (with volume checks on) and `check_keyword_volumes` — one of the brand's
    50 monthly volume checks per call, however many keywords. Batch, don't loop.
  - `suggest_keywords` — one of 5 monthly Suggest runs.
  - `run_test_article` — one paid generation, one at a time, 3 per day.
  - Check `get_keyword_usage` before any keyword spend and show what is left.
- **Destructive tools** (`apply_article_edit`, `archive_keyword`, `delete_competitor`,
  `delete_prompt`, `delete_tone`) are called only after the user has seen exactly what will
  change and confirmed.
- Article bodies contain `<IMAGE_INFOGRAPHICS_N>…</IMAGE_INFOGRAPHICS_N>` markers. Keep every
  one of them when proposing an edit.

## Wording

- Era's content feature is the **content calendar** (or **content plan**). Do not write
  "season" anywhere in user-facing text, even though some tool payloads still carry the word.
- "AI answer engines" / "AI search" for the category; name engines as ChatGPT, Perplexity,
  Gemini, Google AI Overviews, Claude, Grok.
- Metrics use Era's definitions (see `get_glossary`): **visibility** = share of monitored
  answers that mention the brand; **share of voice** = the brand's share of all brand
  mentions; **position** = order of mention, 1 is best; **citation** = a source URL/domain an
  engine references.
- Plain, direct English. No hype, no emoji in SKILL.md, no exclamation marks.
- Every recommendation is falsifiable: say what evidence it rests on and how the user would
  see it worked.

## Originality

The structure of this pack is informed by the popular open-source SEO/GEO skill packs. The
text is written from scratch. Do not paste sentences, tables or checklists from other
repositories — rewrite from understanding, in this guide's voice.

## Checklist before committing a skill

- [ ] `name` equals the directory name; `description` triggers on the right phrases.
- [ ] Starts with `list_brands` when it needs brand data; states the window.
- [ ] Every paid or destructive call has a confirmation step.
- [ ] Output section shows the deliverable shape.
- [ ] No "season", no copied text, no secrets, no `..` paths.
- [ ] `claude plugin validate .` passes from the repository root.
