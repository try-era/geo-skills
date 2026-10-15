# Calendar view

How to lay out the calendar so it reads the same every time, and when a row becomes a
decision for the user.

## The table

One row per topic or article in the plan in progress, ordered by `scheduled_publish_date`
(rows without a date go last). Columns, in this order:

| Column | Source | Rule |
| --- | --- | --- |
| Date | `scheduled_publish_date` | `YYYY-MM-DD`, UTC. Blank when the item has none. |
| Title | `title` | As returned; shorten past 70 characters with an ellipsis. |
| Category | `content_intent` | `keyword`, `glossary`, `versus`, `top5` or `howto`, as planned. |
| Status | `status` | Label from the next table. |
| Sub-product | `sub_product.name` | `hub` when `sub_product` is null; omit the column when the brand has no sub-products. |
| Destination | `platform` plus settings | See below. |

Status labels:

| `status` | Show as | Meaning |
| --- | --- | --- |
| `topic` | awaiting approval | A title only; nothing written. Can be renamed. |
| `approved` | approved | Queued for writing. |
| `draft`, `generating` | writing | Being produced. |
| `generated` | ready | Written; editable until it is published. |
| `edited` | edited | Changed by hand or through `article-review`; still editable. |
| `failed` | failed | Generation failed. Needs the Era dashboard. |

Destination: for a `platform` of `blog`, the names of the destinations in
`publish_destination_ids` (from `list_publishing_destinations`), or "none set" when the
list is empty. For a Medium or Substack item, show the platform as returned. A published
article's live URL and per-destination status come from `get_article` → `publications`; do
not call it for every row, only for the ones the user asks about. Published totals come from
`get_content_plan` → `counts.published`.

Show up to 40 rows in full. Beyond that, show the next 14 days in full and one line per
week after, with counts by status, unless the user asks for the whole list.

## Needs a decision

Each rule is a condition, what it means, and what to offer. Number the ones that apply and
leave out the rest.

| Condition | What it means | Offer |
| --- | --- | --- |
| `is_running` is false | Nothing is generated or published on schedule. | Start the workflow (paid: state it). |
| `categories_confirmed` is false | A new plan cannot be generated. | Confirm the current mix, or send a new one. |
| Workflow stopped and topics awaiting approval are dated within three days | They will not be written unless approved. | Approve those topics (paid), or start the workflow. |
| `publish_hour_utc` null or `publish_destination_ids` empty and no lane in `publish_lanes` | Articles are written but not published automatically. | Set the schedule; connect a site first if needed. |
| `blog_publish_enabled` false while destinations exist | Blog publishing is off. | Check the schedule with the user before saving anything. |
| A destination in the settings is not `active` | Deliveries to it fail. | Test it (`publish-to-site`). |
| Items with status `failed` | Generation failed; no tool regenerates it. | Point to the Era dashboard. |
| Items `generated` or `edited` with a date in the next three days | The editing window is closing. | `article-review` before it goes out. |
| Titles that duplicate each other or miss the cluster | A paid generation on a weak topic. | Rename (free), using `content-brief` for the angle. |
| `scheduled` plan exists | The next plan is built ahead. | Mention it; its topics can be read and renamed, not approved. |
| `plan_status` is not `active` or `publishing` | The plan in progress is finished or failed. | Say so; approval is refused (`PLAN_NOT_IN_PROGRESS`). |
| `upgrade_available` is true | A higher plan is available. | Mention once; do not push. |

## Example

```
Trail Co content calendar · dates 2026-10-12–2026-11-10 · read 2026-10-15 09:20 UTC
Workflow running · publishes at 09:00 UTC to Company blog
Plan in progress 30 articles: 22 awaiting approval · 3 approved · 4 written · 1 published
Tone Trail coach · mix keyword 10 · glossary 4 · versus 6 · top5 6 · howto 4
Needs a decision 2

| Date | Title | Category | Status | Sub-product | Destination |
| --- | --- | --- | --- | --- | --- |
| 2026-10-15 | What is a rock plate in trail shoes? | glossary | ready | hub | Company blog |
| 2026-10-17 | Trail shoes vs road shoes: what changes | versus | approved | hub | Company blog |
| 2026-10-19 | How to choose a trail running shoe | keyword | awaiting approval | Shoe finder | Company blog |

Needs a decision
1. "What is a rock plate in trail shoes?" is ready and goes out today at 09:00 UTC.
   Review it first with article-review, or leave it.
2. 2026-10-19 "How to choose a trail running shoe" is awaiting approval; the workflow
   approves it on its own a few days before the date. Approve it now (1 paid generation)?
```

## Reading the numbers

- `counts.topics` is what still awaits approval; `approved` is queued; `generated` is
  written; `published` has gone out. They describe blog articles in the plan.
- `segment_quotas` shows how a brand with sub-products splits the plan between the hub and
  each product; use it to explain why a product has few rows.
- `plan_size` is set by Era and read-only here. To change it, the user contacts support.
