# Review rubric

Five dimensions, scored 1 to 5, in this order. Every score cites evidence from the article:
a quote, a count, a heading. A dimension with no evidence either way is "not verifiable" and
is left out of the total, which is then shown out of the remaining maximum.

Scale for all five: **1** the problem is pervasive, **2** present in most sections, **3** mixed:
the basics are there, with clear gaps, **4** sound, with small fixes, **5** nothing worth
changing.

## 1. GEO citability

Can an engine lift a passage out of this article and quote it with confidence?

| Check | Evidence to collect |
| --- | --- |
| Direct answer | Does the first 100 words answer the title question in one to three sentences that make sense alone? Quote them. |
| Question headings | Count H2 and H3 headings phrased as questions or claims, out of all headings. Compare with the questions in the `cluster` section when you fetched it. |
| Sourced statistics | Count figures with a named source and a year; count figures with neither. |
| Entities | Count named products, standards, people, organisations and places beyond the brand. Is the brand named the same way throughout? |
| Extractable units | Lists, tables and short definition blocks versus long paragraphs holding the key facts. |
| Quotable claims | One-sentence statements that stand on their own. Flag vague adjectives that no engine can cite ("leading", "best-in-class"). |

Anchors: **1** no direct answer, no sourced figure, label headings ("Overview"); **3** a
direct answer exists but late or long, a few sourced figures, about half the headings are
questions; **5** direct answer in the first two sentences, a sourced figure in most sections,
most headings answerable, key facts in lists or tables.

Typical changes: move or write the direct answer to the top; turn label headings into the
questions engines ask; replace an adjective with a figure the article already supports;
put a comparison into a table; name the standard or product instead of "the industry".

## 2. SEO on-page

| Check | Evidence to collect |
| --- | --- |
| Title | Primary keyword near the start, about 60 characters or fewer, promises what the article delivers. |
| Heading structure | Follow the body's own convention. Era renders the title separately, so the body normally starts at H2 with H3 beneath; flag a stray H1 or skipped levels. |
| Keyword coverage | From the `keywords` section: is the primary keyword in the title, the first 100 words and at least one H2? List each supporting keyword as covered or missing. Do not stuff; one natural use each is enough. |
| Search intent | Does the article's shape match `main_intent` (informational, commercial, transactional)? |
| Internal links | Links to the brand's other articles or pages, with descriptive anchors. A sub-product article should close with a call to action linking to `sub_product.url`. |
| Excerpt | `excerpt` falls back to the title when the article has no prose paragraph; flag that. |
| Images | Alt text present on the featured image. |

Anchors: **1** the primary keyword is missing from title and opening, no internal links;
**3** keyword present in title but not in the opening or any H2, one or two links; **5**
keyword in title, opening and an H2, supporting keywords covered, two or more descriptive
internal links, closing call to action in place.

## 3. E-E-A-T

| Check | Evidence to collect |
| --- | --- |
| Experience | First-hand detail: something tested, observed or measured by the brand. Quote it, or note that there is none. |
| Expertise | Does the text show working knowledge (specifics, trade-offs) rather than a summary of other pages? An author byline usually lives in the site template, not the body; say so instead of marking it missing. |
| Authoritativeness | Primary sources named and linked; claims that lean on a competitor's page instead of the original. |
| Trust | Claims a reader can verify, dates on time-sensitive facts, balanced comparisons (a versus or top-five article says who each option fits), no overclaiming. |

Anchors: **1** generic text, no sources, absolute claims; **3** some specifics and sources,
no first-hand material; **5** first-hand detail from the brand, primary sources linked,
trade-offs stated.

First-hand detail cannot be invented. When it is missing, the change is a question to the
user under **Needs from you**, not a sentence in the body.

## 4. Brand-kit adherence

Compare the article with the `brand` section: `about_brand`, `ideal_customer_profile`,
`brand_point_of_view`, the tone's master prompt and the confirmed competitors.

| Check | Evidence to collect |
| --- | --- |
| Reader | Is the ideal customer named or clearly addressed in the opening? Do the examples fit them? |
| Point of view | Does the article argue the brand's position, or could any vendor have written it? |
| Tone | Does the voice follow the tone's rules, including what it forbids? Quote one passage that complies and one that does not. |
| Facts | Do product descriptions agree with `about_brand`? |
| Competitors | Named fairly and only where the topic calls for it. |

When a kit field is `null`, that part is "not verifiable"; recommend filling the kit, since
the generator had less to work from.

Anchors: **1** contradicts the kit or ignores the reader; **3** right reader, generic voice;
**5** the brand's view is visible, the tone holds throughout, and facts match the kit.

## 5. Readability

Use the `quality` section (readability panel scores, humanization result) as an input when
you fetched it, then read the text yourself; the scores are not a verdict.

| Check | Evidence to collect |
| --- | --- |
| Paragraphs | Length; more than four sentences without a break is a flag. |
| Sentences | Long chains of clauses; the same opening word repeated three times in a row. |
| Filler | Stock openers ("In today's fast-paced world"), padding transitions, and phrases that read as machine-written that the humanization pass left in. |
| Structure | Steps as numbered lists, options as bullets or a table, one idea per section. |
| Flow | Each section opens by answering its heading. |

Anchors: **1** dense, repetitive, padded; **3** clear in places, with filler and long
paragraphs; **5** short paragraphs, direct sentences, structure that matches the content.

## Reading the total

- **22–25** — ship it. Propose only fixes with a clear gain, or none.
- **16–21** — a targeted edit. Start with the lowest-scoring dimension.
- **15 or below** — rework the top of the article (direct answer, headings) and the
  evidence first. A diff this large needs the user's yes on its scope before you propose.

A dimension marked "not verifiable" is excluded; scale the thresholds to the remaining
maximum.

## What the edit may and may not do

- It may reorder, tighten, retitle headings, add the direct answer, convert prose to a list
  or table, add internal links, and use facts from the article, the context or the user.
- It may not add a statistic, a quote, a customer, a credential or a product claim that no
  source supports, and it may not remove or renumber an `<IMAGE_INFOGRAPHICS_N>` marker.
- It is judged afterwards by the signal a reviewer can see: after publishing, whether the
  URL shows up among the brand's own-domain citations (`get_top_citations`,
  `list_cited_domains`) over the following four to six weeks.
