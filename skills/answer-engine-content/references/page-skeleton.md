# Page skeleton

The order of blocks for a page meant to be quoted. Fill the template, then remove blocks
the page type does not need (see the table below). The numbers in brackets point to the
patterns in `geo-writing-patterns.md`.

```markdown
# {H1: the target question, or a claim that answers it}

{Byline: By {Name}, {role or credential}, {Organisation}. Published {date}. Updated
{date}: {what changed}.}                                                      [8][10]

{DIRECT ANSWER: one to three sentences. States the answer, the main condition, and what the
page covers next.}                                                            [1][4]

**Key facts**
- {Fact with number, source and date.}                                         [3]
- {Fact.}
- {Fact.}

## What is {entity}?
{Definition in one sentence that names the entity, then one sentence on what it is for.
Name {Entity} the same way on every mention.}                                 [2][5]

## {Question 2: how / why does it work?}
{First sentence answers. Then the reasoning, the numbers with sources, and the
exceptions.}                                                                  [2][3][9]

## {Question 3: how do the options compare?}
{One sentence naming the criteria.}

| Option | Best for | {Criterion 1} | {Criterion 2} | Last checked |
| --- | --- | --- | --- | --- |
| {Name} | {Use} | {Value} | {Value} | {date} |
                                                                              [6][10]

## How do I {do the task}?
1. {Verb + object. Expected result.}
2. {Verb + object.}
3. {Verb + object.}                                                           [6]

## {Question 5: what does it cost, what are the risks, when does it not apply?}
{First sentence answers. State limits plainly; they make the rest credible.}  [4]

## Frequently asked questions
### {Adjacent question 1}
{One to three sentences; the first is the answer.}
### {Adjacent question 2}
{…}                                                                           [7]

## Sources
- {Publisher}, "{Title}", {year}. {url}
- {…}                                                                         [9]

*{About the author: one line with credentials. About the organisation: one line.}*  [8]
```

## What each block is for

| Block | Purpose | Typical size |
| --- | --- | --- |
| H1 | States the question the page answers | one line |
| Byline and dates | Trust and freshness signals in plain text | one line |
| Direct answer | The passage an engine lifts first | 1 to 3 sentences |
| Key facts | Extractable facts with provenance | 3 to 6 bullets |
| Definition section | Anchors the entity and its name | 2 sentences |
| Question sections | One per sub-query; first sentence answers | 80 to 200 words each |
| Table | Comparison or specification, in text | 3 to 8 rows |
| Steps | Procedure, one action each | 3 to 10 steps |
| FAQ | Adjacent questions from real sub-queries | 4 to 8 items |
| Sources | The primary sources behind the claims | as many as were used |

Sizes are working guidance, not limits. A page that answers its question in fewer words
than the template implies is fine.

## Blocks by page type

| Page type | Keep | Drop or shrink |
| --- | --- | --- |
| Guide | All | Table, if there is nothing to compare |
| Comparison | Direct answer naming the pick and the condition, criteria, table, limits, FAQ | Steps |
| How-to | Direct answer (the shortest path), prerequisites, steps, troubleshooting as FAQ | Definition, table |
| Glossary entry | Definition as the direct answer, related terms, one example, FAQ | Table, steps |
| Product or landing page | Direct answer (what it does and for whom), key facts, table of plans, FAQ, sources for any claim | Long definition; keep marketing claims specific and sourced |
| FAQ page | Direct answer for the page theme, then the question list grouped by topic | Everything except sources and byline |

## Rewrite procedure

1. Pull the existing page apart into the blocks above and label each existing paragraph.
2. Move the sentence that answers the target query to the top; cut or compress what it
   replaces.
3. Turn label headings into question headings; make the first sentence under each answer it.
4. Move numbers into sentences that carry their source and date; flag those that cannot.
5. Convert comparisons buried in prose into a table; convert instructions into numbered steps.
6. Add the adjacent-question FAQ from real sub-queries, then the byline, dates and sources.
7. Keep every fact, link, product name and `<IMAGE_INFOGRAPHICS_N>` marker the original had,
   unless the user asked to remove it.
8. Show the result as before and after per block, and list each pattern applied.

## Hand-off notes for the next skills

- `schema-markup`: page type (`Article`, `Product` or `HowTo`), author and organisation,
  `datePublished` and `dateModified` matching the visible dates, `FAQPage` only for a visible FAQ.
- `on-page-seo`: title and meta description drawn from the direct answer, one H1, internal
  links to the pages that answer the sub-questions, descriptive image alt text.
- `geo-audit`: re-score the live URL after publication.
