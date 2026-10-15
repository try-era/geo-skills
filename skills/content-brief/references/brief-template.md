# Brief template

Use the headings verbatim so briefs from different weeks can be compared. Delete a section
only when there is genuinely nothing to put in it, and say why in Open items. A brief is a
working document, so placeholders in braces are fine here; they are never copied into an
article.

```markdown
# Brief — {working title}
{brand}{ · sub-product} · pulled {date} · citation window {days} days

## 1. Title options
1. {title with the primary keyword near the start, about 60 characters or fewer}
2. {a question-form title}
3. {a title that states the angle or the number}
Pick for: {which one suits which goal}. If the topic is still awaiting approval in the
content calendar, rename it with the chosen title before approving.

## 2. Target query and keyword cluster
| Keyword | Role | AI volume/mo | Google volume/mo | Difficulty | Intent |
| --- | --- | ---: | ---: | ---: | --- |
| {primary} | primary | 1,900 | 14,800 | 41 | commercial |
| {supporting} | supporting | 210 | not measured | — | commercial |
Cluster: {name}, priority #{rank}, {member_count} keywords. Not measured: {keywords}.

## 3. Intent and reader
- Reader: {ideal customer profile, one sentence, from the brand kit}
- What they want when they ask this: {informational | commercial | transactional | navigational}
- What they do next: {the action the closing call to action should serve}

## 4. Direct answer
Opens the article, one to three sentences, readable without the rest of the page:
"{Entity} is {category} that {does X} for {reader}; {the one number or fact that
settles it}."
Facts needed to write it: {list; mark any not yet sourced}.

## 5. Outline
Sections add up to the length in section 10.

| # | Heading (as a question) | Source of the question | Answer in one sentence | Evidence to place |
| --- | --- | --- | --- | --- |
| H2-1 | {question} | sub-query, {count} runs | {sentence} | {stat + source} |
| H2-2 | {question} | winner page A | {sentence} | {table or list} |
| H2-3 | {question} | derived from keyword | {sentence} | {first-hand detail from the brand} |
Closing section: {summary} and the call to action to {sub-product url or brand page}.

## 6. Entities to name
Products, standards, people, organisations and places the article must name, with the
spelling to use: {list}. Competitors to mention: {names, only if the category is versus or
top five, or a question requires it}.

## 7. Statistics and sources to cite
| Figure | Source | URL | Year | Checked at the primary source |
| --- | --- | --- | ---: | :---: |
| {figure} | {publisher} | {url} | {year} | yes / no |
A figure marked "no" is not used until someone opens the original.

## 8. Pages that win today
| URL | Type | Opens with a direct answer | Length | Sourced stats | What it misses |
| --- | --- | :---: | ---: | ---: | --- |
| {url} | own / competitor / third-party | yes / no | {words} | {n} | {gap} |

## 9. Internal links
- {anchor text} → {live URL, or "planned, no URL yet"}
Three to five links to the brand's own articles or pages, with descriptive anchors.

## 10. Schema, format and length
- Length: {range} words, measured from the pages read ({n} pages, {low}–{high} words).
  Write "not measured" when fewer than two pages were read. Length follows the questions
  to answer, not the other way round.
- Page type: Article, plus FAQPage only if the page has a visible question and answer
  block. Choose schema for entity clarity, not for rich results; Google has largely retired
  HowTo and FAQ rich results.
- Format by category: glossary — definition first, then examples; versus — comparison
  table, then who each option fits; top five — numbered list with a "best for" line each;
  how-to — numbered steps with the expected result; keyword — answer, evidence, next step.

## 11. Tone and brand
- Tone: {name}; three rules from its master prompt: {1}, {2}, {3}
- Point of view to carry: {brand_point_of_view, or "not set"}
- Words the brand uses / avoids: {from the kit and tone, or "not specified"}

## 12. What to avoid
- Claims no source supports ("best", "leading", "fastest") — replace with a figure or cut.
- Copying structure sentence by sentence from the pages read; they show gaps, not a script.
- {Topic-specific traps: outdated versions, prices, regulations}

## 13. Open items
Things a human must supply before writing: {facts, first-hand data, approvals, missing
brand-kit fields, keywords without volumes}.

## How we will know
Re-run `get_top_citations` and `list_cited_domains` in four to six weeks. Success: the
published URL appears among the brand's own-domain citations, and `own_brand_cited_count`
is above today's {count}. If it is not cited by then, compare the page with the winners
in section 8 before rewriting anything.
```

Reading the data:

- `ai_search_volume` is monthly searches in AI assistants; `search_volume` is Google's. A
  keyword with high Google volume and little AI volume is a classic SEO term the engines
  rarely ask about; say so rather than ranking by Google alone.
- A sub-query count is how often engines ran that query in the brand's monitoring, not a
  market-wide figure.
- Citation lists describe the whole category. A page is "winning" for this topic only when
  its title or path matches it.
