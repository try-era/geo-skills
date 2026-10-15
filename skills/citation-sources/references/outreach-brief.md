# Outreach brief

One page per target. It has two halves: an internal evidence box that never leaves your
team, and the pitch that does. Draft it, hand it to the user, and stop. The skill does not
send anything.

```markdown
# Outreach brief — {publication or site}

## Evidence (internal)
- Target page: {url}   Type: {review site / press / directory / community / reference}
- Cited {n} times in the last {days} days ({share}% of external citations), on {engines}.
- Prompts where it was cited: "{prompt 1}", "{prompt 2}"   (answer_id: {id}, {id})
- The sentence it supports in the answer: "{verbatim fragment}"
- Brand on the page: {checked present / checked absent / not checked}
- Competitors on the page: {names, or "none" / "not checked"}
- Contact: {name and role from the site's masthead or contact page; never guess an address}

## Angle (pick one)
{see table below}

## Pitch
Subject options (pick one, under 60 characters):
1. {specific to their page: "A missing option for your {category} roundup"}
2. {the data point: "{n}% of {audience} do X — new numbers for your {topic} piece"}

Hi {first name},

{One sentence on their page, by title, and what it does well for readers.}

{One sentence on what is missing or outdated, stated as a verifiable fact:
"It lists {n} tools for {job}; it does not cover {capability / segment / region}."}

{What you offer, concrete: a dataset with its method and date, a named expert with a
quote on the topic, a product account for testing, a corrected fact with its source.}

{The ask, small and easy to refuse: "Would a short note on {X} fit the piece?" or
"Happy to send the full data if useful."}

{Name, role, company, one link that proves you exist.}

## Disclosure
{Say what the relationship is: vendor, customer-supplied data, affiliate, sponsored.
Anything paid is labelled by the publisher in their usual way.}

## Follow-up
One reminder after seven days with new information (not "just checking in"). Then stop.

## Check
Look for {domain or url} in `list_cited_domains` / `get_top_citations` after 4-6 weeks,
and re-read "{prompt}" on {engine}. Outcome: {brand named on the page / brand named in the
answer / nothing changed}.
```

## Choosing the angle

| Situation (from the evidence box) | Angle | What to bring |
| --- | --- | --- |
| A roundup or comparison cited often, brand absent | Inclusion | Facts a reviewer can verify: pricing page, feature list, a free trial or test account |
| A statistic the engines quote, from an old source | Fresh data | Your own dataset with sample size, method and date |
| Press page about the category | Expert quote | A named person with real credentials and a clear, short opinion |
| A page that states something wrong about the brand | Correction | The correct fact, the primary source, a polite one-line request |
| A directory or marketplace listing | Listing update | Complete fields, current description, consistent name and category |
| A tutorial or guide cited for how-to prompts | Contribution | A worked example, a template, a screenshot they may credit |

## Community version (replaces the pitch)

Communities are not pitched, they are answered. For a thread that the engines cite:

1. Read the rules and the thread. Skip it if self-promotion is banned or the thread is old
   and closed.
2. Write the answer to the original question first, useful without any link.
3. Say who you are and your connection to the product in one clause.
4. Link only where the link is the evidence, and say what is on the other end.
5. Reply to follow-up questions. Do not post the same text in several threads.

## Quality checklist

- The first sentence is about their reader, not about you.
- Every claim about your product can be checked on a public page.
- Numbers carry a source and a date.
- There is one ask.
- The relationship is disclosed.
- No mention of AI citations unless the publisher would care; if you mention them, state
  the count and the window as measured, nothing more.
- Under 150 words in the pitch body.

## Example (names and numbers invented)

Target: a regional review site's "best scheduling tools for clinics" page, cited 14 times
in 30 days across Perplexity and Gemini.

> Subject: A missing option for your clinic scheduling roundup
>
> Hi Dana, your clinic scheduling guide is the clearest comparison I found for small
> practices. It covers five tools; none supports SMS reminders in Polish or German, which
> matters to the cross-border clinics we work with. Our product does (docs: example.com/sms,
> updated 12 March 2026). I can give you a test account and a short table of supported
> languages and message limits. Would a line on this fit the piece? — Sam, partnerships,
> Example Scheduler (we are the vendor)
