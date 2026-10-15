---
name: content-calendar
description: Reads and steers a brand's Era content calendar — what is planned, written and published, and what needs a decision. Renames topics, approves topics (each one a paid article generation, confirmed first), starts or pauses the workflow, runs a test article, changes content settings. Use for "what's in the content calendar", "approve next topics", "pause content".
argument-hint: <brand> [view | approve | settings | pause | test]
---

# Content calendar

Show what Era has planned, written and published for one brand, name the decisions that are
waiting on the user, and carry them out. Nothing that spends money runs until the user has
seen the number of paid generations and said yes.

## When to use

- "What's in the content calendar?", "what is going out this week?", "what needs approval?"
- "Rename that topic", "approve these three", "pause content", "start the workflow", "write
  a test article to check the voice".
- Setting up content for a brand that is not running yet (the order is in Steps).

Not for: planning a single article in depth (`content-brief`), editing a written article
(`article-review`), or connecting a hand-built site (`publish-to-site`).

## Inputs

- **Brand** — resolve with `list_brands`; ask if several match.
- **Action** — view (default), rename, approve, settings, pause or start, test article.
- **Scope** (optional) — a sub-product, a status, or the next plan instead of the plan in
  progress. Default: the plan in progress, all statuses.

Era keeps one continuous feed: a plan in progress (30 days, `plan_size` articles) and the
next plan built ahead. Tool payloads can use an older word for the plan; in replies say
"plan", "the plan in progress" and "the next plan". Times are UTC.

## Steps

1. **Resolve the brand.** `list_brands` → `brand_id`. If no Era tool is available, give the
   connect command (`claude mcp add --transport http era https://app.tryera.ai/api/mcp`)
   and stop.
2. **Read the settings.** `get_content_settings(brand_id)`. `PLAN_REQUIRED` means the brand
   is not on the Content plan: say so, point to the upgrade in the Era dashboard, and do
   not retry. Keep `is_running`, `categories_confirmed`, `plan_size`, `category_mix`,
   `steps`, `tone_of_voice_id`, `publish_hour_utc`, `publish_destination_ids`,
   `blog_publish_enabled`, `publish_lanes`, `plan_status`, `upgrade_available`.
3. **Read the plan.** `get_content_plan(brand_id)` → `active` (the plan in progress) and
   `scheduled` (the next plan, or null). Take `plan_id` from `active.id`; `counts` gives
   topics, approved, generated, published. Both null means the workflow never started: go
   to Setup order below.
4. **List the topics.** `list_plan_topics(plan_id, limit=100)`; page with `offset` until it
   reaches `total`. Narrow with `status` (`topic` = awaiting approval; also `approved`,
   `draft`, `generating`, `generated`, `edited`, `failed`) or `sub_product_id` (from
   `list_sub_products`, or `hub`). List the next plan only when asked.
5. **Name things.** `list_publishing_destinations(brand_id)` for destination names and
   `list_tones(brand_id)` for the tone name, only if the view shows them.
6. **Build the view** from `references/calendar-view.md` and the list of decisions.
7. **Act on one decision at a time**, then re-read with `get_content_plan` and
   `list_plan_topics` and show what changed.
   - **Rename** — `update_plan_topic(plan_id, article_id, title)`. Free. Works on topics
     still awaiting approval, in either plan. A written article is edited with
     `article-review` instead (`NOT_A_TOPIC`).
   - **Approve** — through the approval gate below.
   - **Settings** — `update_content_settings`; see the two warnings in Guardrails.
   - **Pause** — `stop_content_workflow`: generation and publishing stop from the next
     scheduled run, articles already generating finish, nothing is deleted.
   - **Start** — `start_content_workflow` after a yes. Result `status`: `started`
     (generating the plan's topics first), `topping_up`, `ok` (enough queued), `blocked`
     (the content subscription is not active; not an error).
   - **Test article** — `run_test_article` after a yes. Returns `test_article_id` at once;
     read it a few minutes later with `get_article`. It stays off the calendar and is never
     published.

## Approval gate

Approving is the one place this skill spends money: **each approved topic is one full paid
generation** (research, text and, with `generate_images`, images). Before calling
`approve_topics`:

1. Take `plan_id` from `active`, never from `scheduled` (`PLAN_NOT_IN_PROGRESS`).
2. Take the ids from `list_plan_topics(status="topic")`. One call takes 1–10 ids, all or
   nothing; there is no approve-all. For more than ten, state the whole split up front
   (for example 10, 10, 3) and get one yes for that plan.
3. Remind the user that the running workflow approves topics a few days ahead of their
   dates on its own; approving here only writes specific ones sooner.
4. Show exactly this, with real values, and wait:

```
Approve {n} topic(s) in the plan in progress?
  1. {title} ({date}, {category})
  2. …
This starts {n} paid article generation(s), {with | without} images, now.
Reply "yes" to approve, or name the ones to drop.
```

The tools do not expose a price per generation, so state the count and do not quote a
currency amount; the user can check pricing in the Era dashboard. A yes covers only the
call as shown. Then call `approve_topics(plan_id, article_ids, generate_images)` with
`generate_images` set explicitly to what you told the user. The result lists `approved` and
`articles_enqueued`; written articles appear in `list_articles` after a few minutes, where
`article-review` takes over.

The other two paid calls use the same gate, with their own wording:

- Start: "Start the content workflow for {brand}? It spends generation budget: from now on
  Era approves each topic a few days before its date, writes it and publishes it once a
  schedule is saved. Reply yes to start."
- Test article: "Write one test article from a random topic? It is one paid generation
  (text and images), stays off the calendar and is never published. At most three a day.
  Reply yes to run it."

## Setup order (workflow not started)

1. **Brand kit and tone.** `get_brand_kit`, `list_tones`. An empty kit is the first thing to
   fix: `update_brand_kit` is free and applies to articles written from now on.
2. **Settings.** `update_content_settings`: `category_mix` (all five counts summing to
   `plan_size`; sending it confirms it, and nothing can be generated before that), tone,
   steps (only while stopped).
3. **Publishing schedule.** `publish_hour_utc` and `publish_destination_ids` (active
   destinations only). A hand-built site needs its connection created and tested first
   (`publish-to-site`).
4. **Start.** `start_content_workflow`, after a yes.
5. **Review topics.** `list_plan_topics(status="topic")`; empty for a few minutes while the
   topics are generated.
6. **Approve** only what the user wants written sooner.

## Output

Lead with a five-line summary, then the table and the decisions:

```
{Brand} content calendar · dates {first}–{last} · read {YYYY-MM-DD HH:MM} UTC
Workflow running | paused · publishes at {hour}:00 UTC to {destinations | nowhere yet}
Plan in progress {plan_size} articles: {topics} awaiting approval · {approved} approved · {generated} written · {published} published
Tone {name | default blog tone} · mix keyword {n} · glossary {n} · versus {n} · top5 {n} · howto {n}
Needs a decision {n}
```

Then the table (date · title · category · status · sub-product · destination), **Needs a
decision** (numbered, each with the action that resolves it), and, when approval is on the
table, the approval prompt above. `references/calendar-view.md` has the column rules and
the decision rules.

## Guardrails

- No `approve_topics`, `start_content_workflow` or `run_test_article` without a yes given
  after the count was shown. An earlier yes never covers a new call.
- **A changed mix re-plans.** The un-started rest of the plan in progress is planned again
  and the next plan is dropped and rebuilt, at most three times a day per brand. Show the
  new mix and get a yes first; report `regenerating_plan_id`, `scheduled_successor_reset`
  and `regeneration_skipped` from the response.
- **Saving a schedule can start publishing at once** (`auto_publishing_started: true` when
  the workflow is running). Confirm before saving one.
- Steps change only while the workflow is stopped (`WORKFLOW_RUNNING`): stop, change,
  start again, and ask before the start.
- Publishing a post now, regenerating an article and approve-all are not available. For a
  `failed` article, send the user to the Era dashboard.
- Test articles: one at a time, three a day per brand.

## Errors

| Code | Meaning and action |
| --- | --- |
| `PLAN_REQUIRED`, `GENERATION_BLOCKED`, `TEST_ARTICLE_DAILY_CAP`, `PUBLISHING_DISABLED` | Do not retry. Not on the Content plan; subscription not live (renew in the dashboard); today's three tests used (resets 00:00 UTC); publishing switched off. Tell the user. |
| `PLAN_NOT_FOUND`, `ARTICLE_NOT_FOUND`, `PLAN_NOT_IN_PROGRESS`, `NOT_A_TOPIC` | Re-read ids with `get_content_plan` and `list_plan_topics(status="topic")`; approve only in `active`; an approved topic cannot be approved or renamed again. |
| `MIX_INVALID`, `MIX_NOT_CONFIRMED`, `STEP_REQUIRED`, `TONE_NOT_IN_BRAND` | Resend all five counts summing to `plan_size`; confirm with `confirm_categories=true`; a required step cannot go off; use a tone id from `list_tones`. |
| `INVALID_DESTINATION`, `PUBLISH_HOUR_REQUIRED`, `PUBLISH_STEP_CONFLICT` | Use only active destinations (not API-delivery sites); send `publish_hour_utc` with them; leave `steps.publish_blog` out. |
| `WORKFLOW_RUNNING`, `NO_ACTIVE_PLAN` | Stop before changing steps; start the workflow before a test article. |
| `NO_TOPICS`, `TEST_ARTICLE_RUNNING` | Transient. Wait a few minutes and call again. |

## Era tools used

- `list_brands`, `get_content_settings`, `get_content_plan`, `list_plan_topics`,
  `list_publishing_destinations`, `list_tones`, `list_sub_products`, `get_brand_kit`,
  `get_article` (read).
- `update_plan_topic`, `update_content_settings`, `stop_content_workflow` (write, free).
- `approve_topics`, `start_content_workflow`, `run_test_article` (write, paid: confirm).

REST equivalents under `/api/v1` with `X-API-Key`: `/brands/{brand_id}/content-settings`,
`/content-plan`, `/content-plans/{plan_id}/topics`, `/content-plans/{plan_id}/topics/approve`,
`/brands/{brand_id}/content-workflow/start`, `/stop`, `/test-article`.
