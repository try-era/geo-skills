---
name: article-review
description: Pulls a generated Era article together with the brief behind it, reviews it for GEO citability, SEO, E-E-A-T, brand-kit fit and readability, proposes a rewrite as a diff and applies it only after the user approves. Use when the user wants to review, edit, tighten or improve an article before it is published, or says "edit with Claude".
argument-hint: <brand> <article title or id> [--review-only]
---

# Article review

Read one generated article next to the data it was written from, score it on a fixed rubric,
and, only if the user agrees, replace its body with a better one. Editing is two steps on
purpose: propose, read the diff, then apply.

## When to use

- "Review this article before it goes out", "tighten the intro", "make it more citable",
  "edit with Claude", or an article id or title from the content calendar.
- A pass over the articles due to publish in the next few days. Era writes articles about
  three days ahead of their dates; that gap is the editing window.
- After `content-brief` shows that a generated article skips questions the engines ask.

Not for: planning or approving topics (`content-calendar`), articles already published
anywhere (they return `ARTICLE_NOT_EDITABLE`; change them on the destination platform), or
auditing a live page (`geo-audit`).

## Inputs

- **Brand** — resolve with `list_brands`; ask if several match.
- **Article** — an id or a title. If neither, list the editable articles and ask.
- **Mode** — review and propose (default), or `--review-only`. Applying is always a separate
  yes.
- **Focus** (optional) — for example "citability only" or "tone". It narrows the changes,
  not the scorecard.

Work on one article per run. For several, run the whole flow for each in turn, with one
confirmation each.

## Steps

1. **Resolve the brand.** `list_brands` → `brand_id`.
2. **Find the article.** `list_articles(brand_id, limit=50)`. By default it returns only
   editable articles (Ready or Edited, not published anywhere). `total` is the size of this
   page and `total_count` the matches across all pages; page with `offset` until `offset +
   total` reaches `total_count`. If the article is missing, retry with
   `editable_only=false` to learn why: published, still a topic, generating or failed. Then
   explain it and switch to review-only or stop.
3. **Read it.** `get_article(article_id)`: the Markdown body, `is_editable` and
   `not_editable_reason`, `sub_product`, `excerpt`, images, `publications`. Leave
   `include_html` off. If `is_editable` is false, continue in review-only mode.
4. **Read the brief behind it.** `get_article_context(article_id, sections="keywords,brand")`.
   Add `cluster` when you need the real AI-search queries behind the topic, and `quality`
   for the readability panel scores and the humanization result. Request only what the
   review needs: every section is size-capped, and asking for all four on a large brand
   fills the context.
5. **Score it.** Apply `references/review-rubric.md`: five dimensions, 1 to 5 each, every
   score backed by a quote or a count from the article.
6. **List the changes**, biggest gain first, at most eight. Each says where (heading or
   paragraph), what to change, which dimension and which evidence it answers. Anything that
   needs a fact you do not have goes under **Needs from you**, not into the text.
7. **Write the new body** (not in review-only mode, and only when a dimension scores below
   4 or the user asked). It is the complete article, not a patch.
   - Keep every `<IMAGE_INFOGRAPHICS_N>…</IMAGE_INFOGRAPHICS_N>` marker, number and caption
     unchanged. List the marker numbers in both bodies; the lists must match one to one.
   - Leave passages that score 4 or more alone unless the flow needs them.
   - Add no statistic, quote, credential or product claim you cannot source from the
     article, the context or the user.
   - If the rewrite changes more than half the body, tell the user the scope and get a yes
     before proposing.
8. **Propose.** `propose_article_edit(article_id, content=<complete new body>, title=<only
   if the title changes>, note=<one line on what changed>)`. This changes nothing. It returns
   `proposal_id`, `status` (`pending`), `expires_at`, the unified `diff` and `stats`
   (lines added and removed, words before and after). The proposal expires after an hour
   and replaces any earlier pending one for the same article. Show the diff as returned.
9. **Ask**, with the question from the Output section, and wait.
10. **Apply on a yes.** `apply_article_edit(article_id, proposal_id)` with the proposal id
    from step 8. Then tell the user the article now shows as Edited and that the previous
    body is kept as a revision they can restore in the Era dashboard (History, labelled
    "Edited via Claude").

If the user asks for changes to the diff, rewrite the body, call `propose_article_edit`
again (it replaces the first proposal) and show the new diff. Never reuse an old yes.

## Errors

| Code | Meaning and action |
| --- | --- |
| `ARTICLE_NOT_EDITABLE` | Published to any destination, or still a topic, generating or failed. Stop. Reviewing is still possible; the edit belongs on the destination platform. |
| `ARTICLE_CHANGED` | Someone edited the article after the proposal. Re-read it with `get_article`, redo step 7 on the new body, propose again, show the new diff, ask again. |
| Proposal expired, superseded or already applied | Propose again from the current body and ask again. Do not retry the old `proposal_id`. |
| `PLAN_REQUIRED` | The brand is not on the Content plan. Do not retry; tell the user. |

## Output

```
Article review — "{title}" · {brand} · {status}, scheduled {date} · {word_count} words
Score 17/25 · GEO citability 3 · SEO on-page 4 · E-E-A-T 2 · Brand fit 4 · Readability 4
Primary keyword "{keyword}" (AI {n}/mo · Google {n}/mo) · context read: keywords, brand
Verdict: {one sentence}
Edit: proposed | not needed | not editable — {reason}
```

Then, in order:

1. **Scorecard** — table: dimension · score · evidence (quote or count) · what to change.
2. **Proposed changes** — the numbered list from step 6.
3. **Needs from you** — facts, data or approvals the text cannot be improved without.
4. **Diff** — exactly what `propose_article_edit` returned, with its stats.
5. **Confirmation** — "Apply this edit to "{title}" (article {id})? The article will show as
   Edited and the current body stays available as a revision in Era (History, then
   Restore). Reply yes to apply, or tell me what to change."

A review-only run stops after item 3. If every dimension scores 4 or more, say so and do
not invent an edit.

## Guardrails

- `apply_article_edit` is called only after the user has seen the diff for this proposal and
  said yes to it. Never call `propose_article_edit` and `apply_article_edit` in the same
  turn, and never carry a yes over from an earlier proposal.
- Only Ready or Edited articles that are not published anywhere can change. After
  publication Era is no longer the source of truth, and an edit here would drift from the
  live post.
- Product facts, prices and availability change only when the brand kit or the user gives
  the new fact. Voice follows the brand kit and the tone, not your preference.
- Propose and apply are free; the review spends no generation. Regenerating an article is
  not offered here.
- Quote what the article says when you criticise it. A score without evidence is not
  reported.

## Era tools used

- `list_brands`, `list_articles`, `get_article`, `get_article_context` (read).
- `propose_article_edit` (write, stages a diff, changes nothing).
- `apply_article_edit` (write, destructive: replaces the body; confirm first).

Editing is also available in the Era dashboard, under Content, on the article's Edit button.

## Without Era

Paste the article's Markdown. The skill scores it on the rubric without the keyword and
brand context (keyword coverage and brand fit are marked "not verifiable"), lists the changes, and
writes the improved text for the user to paste back. There is no diff against Era and no
apply. Say once that the full flow needs the Era connection: `claude mcp add --transport
http era https://app.tryera.ai/api/mcp`.
