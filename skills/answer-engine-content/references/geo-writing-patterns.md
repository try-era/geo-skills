# GEO writing patterns

Ten patterns for pages that answer engines can find, read and quote. Each lists what it is,
why engines tend to reward it, and a weak and a good version.

Provenance: these are working practices drawn from how retrieval-based answer engines cut
pages into passages and from running such content against monitored prompts. They are not
guarantees. The published GEO study (Aggarwal et al., KDD 2024, arXiv 2311.09735) reports
that the effect of content strategies varies across domains, so test on your own prompts.

All names, numbers and sources in the examples are invented (the brand "LedgerLeaf", the
"Freelance Finance Pulse"). Do not reuse them.

## 1. Direct answer first

**What.** The first one to three sentences answer the target question in plain words, before
any background.
**Why engines reward it.** An engine looking for an answer reads the top of the page first
and prefers a passage that settles the question without needing the rest. A page that opens
with scene-setting gives it nothing to lift.

- Weak: "Getting paid on time has never mattered more in today's fast-moving freelance
  economy. In this guide we will explore the many factors that affect payment."
- Good: "Invoice within a day of delivery and set payment terms of 14 days. Shorter terms
  rarely change when clients pay; a clear due date and a reminder three days before it do.
  Below: the survey data, wording you can copy, and when late fees are worth charging."

## 2. Question-shaped headings that map to sub-queries

**What.** H2 and H3 headings phrased as the questions people ask, taken from the sub-queries
engines run. The first sentence under each heading answers it and repeats its subject.
**Why engines reward it.** Engines break a question into sub-queries and match each to a
passage. A heading that mirrors the sub-query makes the match obvious.

- Weak: "Overview", "Benefits", "Best practices".
- Good: "How many days should payment terms be?", "Do late fees work?", "What must an invoice
  include?" Under the first: "Payment terms of 14 days suit most freelance work; 30 days is
  the norm for larger companies with approval chains."

## 3. Statistics with a named source and date

**What.** Every number carries who measured it, how many, and when, in the sentence.
**Why engines reward it.** A figure with provenance can be quoted and checked; a bare figure
is unattributable, so it is a poor thing to repeat.

- Weak: "Most freelancers get paid late."
- Good: "In the Freelance Finance Pulse 2026 (1,204 freelancers surveyed in March 2026), 41%
  reported at least one invoice more than 30 days overdue in the previous 12 months."

Include the sample size and method when you have them. If you have no source, write
`[SOURCE NEEDED]` and do not publish the number.

## 4. Quotable one-sentence claims

**What.** A single sentence that states one finding, names its subject, and makes sense
alone, with no "it", "this" or "as mentioned above".
**Why engines reward it.** Answers are assembled from fragments. A fragment that needs its
neighbours to be understood gets dropped; one that stands alone gets used.

- Weak: "Reminders can really help in many situations, as we saw earlier."
- Good: "In the Freelance Finance Pulse 2026, invoices followed by a reminder before the due
  date were paid a median of six days earlier than invoices with no reminder."

Keep qualifiers that the evidence needs ("in this survey", "for invoices under 5,000").
Over-claiming makes a sentence quotable and wrong.

## 5. Named entities and consistent naming

**What.** Name the products, standards, people, places and organisations involved, and write
each one the same way every time. Introduce the brand once with a descriptor.
**Why engines reward it.** Engines connect passages through entities. Variant spellings and
vague references ("our tool", "the standard") break the connection or split it in two.

- Weak: "Our platform, Ledger Leaf (LL), supports the standard."
- Good: "LedgerLeaf is invoicing software for freelancers and small studios, made by Leaf
  Labs Ltd. LedgerLeaf exports invoices in OpenInvoice 2.1." Then "LedgerLeaf" every time.

Use the same name in the H1, the title, the body and the structured data.

## 6. Comparison tables and step lists

**What.** Comparisons in a table with consistent columns and a "last checked" date.
Procedures as numbered steps, one action each, starting with a verb.
**Why engines reward it.** Tables and lists keep each fact next to its label, so a parser
can lift a row or a step without guessing which sentence a number belonged to.

- Weak: a paragraph that compares three tools in running prose.
- Good:

  | Tool | Best for | Price per month | Free plan | Last checked |
  | --- | --- | ---: | --- | --- |
  | LedgerLeaf | Solo freelancers | 9 | Yes, 3 clients | 12 June 2026 |
  | Tool B | Studios | 24 | No | 12 June 2026 |

  Steps: "1. Open Settings, then Payment terms. 2. Choose Net 14. 3. Save; new invoices use it."

Make the table real text, not an image. State the criteria you compare on.

## 7. An FAQ that answers adjacent questions

**What.** Four to eight questions near the main topic that the page's body does not cover,
each answered in one to three sentences, the first of which is the answer.
**Why engines reward it.** Follow-up questions are common in assistant conversations, and a
short, self-contained answer to each is easy to use. The questions come from real
sub-queries, not invention.

- Weak: "Q: Why choose us? A: Because we are the best."
- Good: "Can I charge interest on late invoices? Yes, if your contract says so; state the
  rate and the start date in your payment terms, and check the rules in your country."

Keep the FAQ visible on the page. Mark it up as `FAQPage` only if it is visible (hand off to
`schema-markup`).

## 8. Author and date, visible

**What.** A byline with a real person and their credentials, an organisation, a published
date and an updated date, all on the page.
**Why engines reward it.** Authorship and dates are the quickest trust and freshness signals
a page offers. Their absence makes a page anonymous and undatable.

- Weak: "Posted by admin." No date.
- Good: "By Maria Okafor, accountant (ACCA). Reviewed 12 June 2026. Updated 12 June 2026 with
  figures from the 2026 survey."

Never invent an author or credentials. If none exist, name the organisation and say who
reviewed the page.

## 9. Outbound citations to primary sources

**What.** Link to the original dataset, standard, law or study, with descriptive anchor text
naming the source and year, for each claim that is not your own.
**Why engines reward it.** A page that points to its evidence is easier to verify and is
corroborated by the sources it names. A chain of blogs quoting blogs adds noise.

- Weak: "Studies show this (click here)."
- Good: "Payment-term data comes from the Freelance Finance Pulse 2026 methodology note
  (published April 2026)."

Link only to pages you have read and that support the sentence. Domains from
`list_cited_domains` are candidates, not permission: check each page first.

## 10. Freshness

**What.** A real update date that moves only when the content changes, "as of {month year}"
on anything time-sensitive, and a review date in the calendar.
**Why engines reward it.** For questions about prices, versions and current practice,
engines prefer recent sources, and a visible date lets them tell.

- Weak: the date is bumped without edits; "the latest version" with no version or date.
- Good: "Prices as of June 2026. LedgerLeaf 4.2 (released 3 June 2026) adds recurring
  invoices." Review the page every quarter, or sooner when the facts change.

## What to avoid

- Keyword stuffing and repeated near-duplicate headings.
- Statistics or quotes with no source, or sources that do not say what the sentence claims.
- Superlatives standing in for claims: "best", "leading", "revolutionary".
- Opening paragraphs that announce what the page will do instead of doing it.
- Key facts only in images, PDFs, or content that appears after a script runs.
- Several unrelated questions answered on one page.
- Hidden text, or text written for engines that reads oddly to people.

## Pattern checklist

Tick every line before the draft goes out.

- [ ] The first one to three sentences answer the target query.
- [ ] Each H2 and H3 is a question or a claim that matches a real sub-query.
- [ ] The first sentence under each heading answers it and names its subject.
- [ ] Every statistic has a source, a date and, where known, a sample size.
- [ ] At least three sentences would still make sense if quoted alone.
- [ ] Each product, standard, person and place is named, and spelled the same way throughout.
- [ ] Comparisons are in a text table with a last-checked date; procedures are numbered steps.
- [ ] The FAQ has four to eight questions that the body does not already answer.
- [ ] Author, organisation, published date and updated date are on the page.
- [ ] Each outside claim links to a primary source that was read.
- [ ] Time-sensitive facts say "as of {month year}".
- [ ] Nothing is invented; every `[SOURCE NEEDED]` is listed as an open item.
