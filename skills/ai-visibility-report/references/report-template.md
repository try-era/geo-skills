# Report template

Use the headings verbatim so reports are comparable week to week. Replace every
placeholder; delete a section only when there is genuinely no data for it, and say so in
the Method line.

```markdown
# {Brand} — AI visibility, {date_from} to {date_to}

{Five-line summary block}

## What moved and why
- {Metric} {direction} {delta} on {engine}. Evidence: "{quoted fragment of an answer}"
  ({engine}, {date}, prompt: "{prompt}"). The engine now {names X / cites Y / answers without brands}.
- …(two to four bullets, biggest move first)

## Engine by engine
| Engine | Visibility | Δ | Avg position | Share of voice | Answers in window |
| --- | ---: | ---: | ---: | ---: | ---: |
| ChatGPT | 48% | +4 | 1.8 | 31% | 120 |
| Perplexity | 61% | +9 | 1.4 | 35% | 118 |
| … | | | | | |

## Competitors
| Brand | Share of voice | Δ | Visibility | Avg position |
| --- | ---: | ---: | ---: | ---: |
| Competitor A | 34% | −2 | 55% | 1.6 |
| **{Brand}** | 27% | +3 | 42% | 2.1 |
| … | | | | | |

## Where the engines get their facts
| Domain | Citations | Share | Type |
| --- | ---: | ---: | --- |
| g2.com | 23 | 19% | third-party |
| {brand domain} | 9 | 8% | own |
| competitor.com | 7 | 6% | competitor |
| … | | | |

## Three actions
1. **{Action}** — should move {metric} on {engine}; check in {n} weeks by {how}.
2. …
3. …

## Method
{days}-day window · {n} prompts · {providers} · visibility = share of monitored answers
naming the brand · share of voice = brand mentions ÷ all tracked-brand mentions ·
position = order of mention (1 = first) · data: Era monitoring, pulled {timestamp}.
```

Practitioner version: add a **Prompt table** (prompt, engines where mentioned, position,
last answer date) built from `list_prompts` + `list_answers`, and an **Answers appendix**
with the quoted fragments and their `answer_id`s.
