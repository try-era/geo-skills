# Research template

Use the headings verbatim so research runs compare. Every table names its segment: the
hub, or the sub-product. Numbers come from the tool payloads; a missing value is `—`
(never estimated), and a `null` AI volume is written `unchecked`. Intent is written as
Era returns it in `main_intent`; use `—` when it is empty.

```markdown
# {Brand} — AI keyword research, {segment}, {date}

{Five-line summary block from SKILL.md}

## Allowance
Volume checks {used}/{limit} used ({left} left) · Suggest runs {used}/{limit} used
({left} left) · resets {resets_at, date only}.

## Clusters
| # | Cluster | Keywords | AI volume | Google volume | Intent | Covered by content? |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | trail shoes for wide feet | 18 | 3,100 | 9,400 | commercial | no |
| 2 | trail shoe sizing | 11 | 1,250 | 2,900 | — | yes: "Trail shoe sizing guide" |
| … | | | | | | |

## Gaps
### Sub-queries engines run that no keyword covers
| Sub-query | Count | Engines | Closest cluster | Source |
| --- | ---: | --- | --- | --- |
| waterproof trail shoes under 150 | 41 | ChatGPT, Perplexity | none | list_search_queries |

### Wording from lost prompts
| Prompt (verbatim) | Engine | Candidate phrase | Source |
| --- | --- | --- | --- |
| best trail shoes for flat feet | Gemini | trail shoes for flat feet | competitor-gap #4 |

## Proposed additions — {segment}
| # | Phrase | Why it is here | Already in database? |
| ---: | --- | --- | --- |
| 1 | waterproof trail shoes under 150 | 41 sub-queries, no keyword | no |
| 2 | trail shoes for flat feet | lost prompt, Gemini | no |
| … | | | |

Expected cost: 1 volume check for the whole list ({n} phrases).
Alternative: add without measuring (`check_volumes=false`), cost 0; phrases are stored
`hidden` until checked.

{Exact confirmation question — see below}

## After the run
| Phrase | Status | AI volume | Google volume | Intent |
| --- | --- | ---: | ---: | --- |
| waterproof trail shoes under 150 | active | 880 | 1,900 | commercial |

Checked {n} · dropped {n} · volumes_checked {true/false} · notice: {text or none}
Allowance now: checks {used}/{limit} · Suggest {used}/{limit}.

## Method
{rows of the database read (of total)} · {n} sub-queries read · coverage source {Era
articles / user URLs / unknown} · segment {name}. AI volume is Era's measured monthly
searches in AI assistants; Google volume is best effort.
```

## Reading AI volume against Google volume

Compare within a cluster, not against a fixed threshold.

| Pattern | Read it as | Do |
| --- | --- | --- |
| AI volume high, Google volume lower or unavailable | Demand that classic keyword tools understate | Answer it directly on a page; first in the queue |
| Both high | Established demand on both | Cover it; expect competition |
| AI volume low, Google volume high | A classic search term that assistants are rarely asked | Lower priority for AI visibility |
| `unchecked` | Unmeasured, not zero | Include it in the next batch if it matters |
| Question-shaped phrases with `commercial` intent | The prompts that decide a purchase | Check whether a monitored prompt exists for it |

Rank candidates by `ai_search_volume`, break ties by lower `keyword_difficulty`, and promote
any phrase that appears both in the sub-queries and in a lost prompt.

## Confirmation questions

Use these forms; fill every number from `get_keyword_usage`.

**Add and measure** (`add_keywords`, `check_volumes` on)

> Add these {n} phrases to {segment}? This uses 1 of your monthly volume checks ({used} of
> {limit} used, {left} left, resets {date}). It is one check however many phrases. Era
> measures their AI search volume and phrases with demand become active. {If any exist:
> {k} of them already sit in another segment and will be moved.} Reply yes to run it, or
> tell me what to remove.

**Preview only** (`check_keyword_volumes`)

> Check the AI search volume of these {n} phrases without adding them? This uses 1 of your
> monthly volume checks ({used} of {limit} used, {left} left, resets {date}). Reply yes to
> run it.

**Suggest** (`suggest_keywords`)

> Start a Suggest run for {brand or sub-product}? This uses 1 of 5 monthly runs ({used}
> used, {left} left, resets {date}) and takes several minutes; I will check until it
> finishes. A run that fails is not counted. Reply yes to start it.

**Move** (`assign_keywords`) — no spend

> Move these {n} keywords from {segment} to {segment}? Nothing is spent; the affected
> segments are re-clustered in the background. Reply yes to move them.

**Archive** (`archive_keyword`, one per call)

> Archive "{keyword}" ({status}, AI volume {value})? It stops feeding the content plan and
> Suggest will not add it back. It can be restored with `restore_keyword` using id {id}. Reply
> yes to archive it.

If the allowance is zero, replace the question with the reset date and offer the free
alternative (`check_volumes=false`) or waiting.
