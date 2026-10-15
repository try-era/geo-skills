# Schema types: when, required, recommended, example

Examples use a fictional company, Kestrel Billing (`https://www.kestrelbilling.example`),
and illustrative profile URLs. Replace every value with facts from the page being marked up.

How to read the lists:

- **Required** is what Google's documentation requires for the matching rich result. For
  most types schema.org itself requires nothing; "required" here means "without it the
  markup is not eligible or not useful".
- **Recommended** properties add information and are worth including when the page shows
  them.
- Google's list of supported rich results changes. Confirm the current state in Google's
  structured-data gallery
  (`developers.google.com/search/docs/appearance/structured-data/search-gallery`) before
  telling a user that a rich result is available.
- Each example is one node. In a page, nodes sit inside one `@graph` array (see the full
  example first) and reference each other with `{"@id": "..."}`.

## The full graph: a blog post

One `<script type="application/ld+json">` block. Five nodes linked by `@id`.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.kestrelbilling.example/#organization",
      "name": "Kestrel Billing",
      "url": "https://www.kestrelbilling.example/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://www.kestrelbilling.example/#logo",
        "url": "https://www.kestrelbilling.example/static/logo-512.png",
        "width": 512,
        "height": 512
      },
      "sameAs": [
        "https://www.linkedin.com/company/example-kestrel-billing",
        "https://github.com/example-kestrel-billing"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.kestrelbilling.example/#website",
      "url": "https://www.kestrelbilling.example/",
      "name": "Kestrel Billing",
      "publisher": { "@id": "https://www.kestrelbilling.example/#organization" },
      "inLanguage": "en"
    },
    {
      "@type": "WebPage",
      "@id": "https://www.kestrelbilling.example/guides/prorations#webpage",
      "url": "https://www.kestrelbilling.example/guides/prorations",
      "name": "Prorations explained",
      "isPartOf": { "@id": "https://www.kestrelbilling.example/#website" },
      "primaryImageOfPage": { "@id": "https://www.kestrelbilling.example/guides/prorations#image" },
      "breadcrumb": { "@id": "https://www.kestrelbilling.example/guides/prorations#breadcrumb" },
      "datePublished": "2026-03-02",
      "dateModified": "2026-09-18",
      "inLanguage": "en"
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.kestrelbilling.example/guides/prorations#breadcrumb",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.kestrelbilling.example/" },
        { "@type": "ListItem", "position": 2, "name": "Guides", "item": "https://www.kestrelbilling.example/guides" },
        { "@type": "ListItem", "position": 3, "name": "Prorations explained" }
      ]
    },
    {
      "@type": "BlogPosting",
      "@id": "https://www.kestrelbilling.example/guides/prorations#article",
      "headline": "Prorations explained",
      "description": "The three proration modes, with a numeric example for each.",
      "mainEntityOfPage": { "@id": "https://www.kestrelbilling.example/guides/prorations#webpage" },
      "image": {
        "@type": "ImageObject",
        "@id": "https://www.kestrelbilling.example/guides/prorations#image",
        "url": "https://www.kestrelbilling.example/img/prorations-1200x630.png",
        "width": 1200,
        "height": 630
      },
      "datePublished": "2026-03-02",
      "dateModified": "2026-09-18",
      "author": { "@id": "https://www.kestrelbilling.example/team/ines-varga#person" },
      "publisher": { "@id": "https://www.kestrelbilling.example/#organization" },
      "inLanguage": "en"
    },
    {
      "@type": "Person",
      "@id": "https://www.kestrelbilling.example/team/ines-varga#person",
      "name": "Ines Varga",
      "url": "https://www.kestrelbilling.example/team/ines-varga",
      "jobTitle": "Head of Billing Engineering",
      "worksFor": { "@id": "https://www.kestrelbilling.example/#organization" },
      "sameAs": ["https://www.linkedin.com/in/example-ines-varga"]
    }
  ]
}
```

What the linking does: the `WebPage` is part of the `WebSite`; the article is the main
entity of the page; the author and publisher are referenced, not repeated. The
`Organization`, `WebSite` and `Person` nodes keep the same `@id` on every page that
mentions them, so a consumer can tell it is one entity across the site.

## Organization

- **When:** every site, defined in full once (home page or about page) and referenced by
  `@id` elsewhere. Use a subtype where one fits (`Corporation`, `NGO`, `OnlineStore`).
- **Required:** none for Google. In practice `name` and `url`.
- **Recommended:** `logo` (an `ImageObject`; Google wants at least 112 x 112 px),
  `sameAs`, `description`, `legalName`, `foundingDate`, `contactPoint`, `address`.
- **Identity:** `sameAs` lists the entity's other canonical profiles (Wikipedia,
  Wikidata, LinkedIn, GitHub, Crunchbase, YouTube). Only list profiles that exist and
  that the organisation controls or that are about it.

```json
{
  "@type": "Organization",
  "@id": "https://www.kestrelbilling.example/#organization",
  "name": "Kestrel Billing",
  "legalName": "Kestrel Billing, Inc.",
  "url": "https://www.kestrelbilling.example/",
  "logo": "https://www.kestrelbilling.example/static/logo-512.png",
  "foundingDate": "2021",
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "support@kestrelbilling.example",
    "availableLanguage": ["en"]
  },
  "sameAs": ["https://www.linkedin.com/company/example-kestrel-billing"]
}
```

## WebSite

- **When:** once per site, usually on the home page (the same node can be repeated on
  other pages with the same `@id`).
- **Required:** `url`. `name` (and optionally `alternateName`) is what Google's site-name
  feature reads.
- **Recommended:** `publisher` (reference to the `Organization`), `inLanguage`.
- **Note:** Google retired the sitelinks search box in 2024, so a `SearchAction` no longer
  produces a Google feature. Add one only if the site has an internal search and a
  machine-readable description of it is useful.

```json
{
  "@type": "WebSite",
  "@id": "https://www.kestrelbilling.example/#website",
  "url": "https://www.kestrelbilling.example/",
  "name": "Kestrel Billing",
  "alternateName": "Kestrel",
  "publisher": { "@id": "https://www.kestrelbilling.example/#organization" },
  "inLanguage": "en"
}
```

## WebPage (and subtypes)

- **When:** every page. It is the glue node: it ties the page to the site, the
  breadcrumb, the main entity and the dates. Use a subtype when accurate: `AboutPage`,
  `ContactPage`, `CollectionPage`, `ItemPage`, `ProfilePage`, `FAQPage`, `QAPage`.
- **Required:** none. Include `url` and `name`.
- **Recommended:** `isPartOf` (the `WebSite`), `breadcrumb`, `primaryImageOfPage`,
  `datePublished`, `dateModified`, `inLanguage`, `about` or `mainEntity`.

```json
{
  "@type": "AboutPage",
  "@id": "https://www.kestrelbilling.example/about#webpage",
  "url": "https://www.kestrelbilling.example/about",
  "name": "About Kestrel Billing",
  "isPartOf": { "@id": "https://www.kestrelbilling.example/#website" },
  "about": { "@id": "https://www.kestrelbilling.example/#organization" },
  "dateModified": "2026-08-30"
}
```

## Article, BlogPosting, NewsArticle

- **When:** an editorial page with an author and a date. `BlogPosting` for blog posts,
  `NewsArticle` for reported news, `TechArticle` for technical documentation, `Article`
  when none fits.
- **Required:** none for Google; markup without the recommended set adds little.
- **Recommended:** `headline` (keep it concise; Google suggests brevity, around 110
  characters at most), `image` (one or more URLs, large enough for previews), `datePublished`,
  `dateModified`, `author` (a `Person` or `Organization` with `name` and a `url` that
  identifies them), `publisher`, `mainEntityOfPage`, `description`.
- **Consistency:** the dates must match the dates shown on the page. Do not bump
  `dateModified` without a real change.

```json
{
  "@type": "NewsArticle",
  "@id": "https://www.kestrelbilling.example/news/soc2-type2#article",
  "headline": "Kestrel Billing completes SOC 2 Type II audit",
  "image": ["https://www.kestrelbilling.example/img/soc2-1200x630.png"],
  "datePublished": "2026-09-10T08:00:00+00:00",
  "dateModified": "2026-09-10T08:00:00+00:00",
  "author": { "@type": "Organization", "name": "Kestrel Billing", "url": "https://www.kestrelbilling.example/" },
  "publisher": { "@id": "https://www.kestrelbilling.example/#organization" },
  "mainEntityOfPage": { "@id": "https://www.kestrelbilling.example/news/soc2-type2#webpage" }
}
```

## Product, Offer, AggregateRating, Review

- **When:** a page for one product or one plan that can be bought or priced. Not for a
  category page listing many products (use `CollectionPage` with an `ItemList`).
- **Required (product snippet):** `name`, and at least one of `offers`, `aggregateRating`
  or `review`. **For merchant listings:** `name`, `image`, and `offers` with `price` and
  `priceCurrency`.
- **Recommended:** `image`, `description`, `sku`, `brand`, a global identifier (`gtin`,
  `mpn`), `offers.availability`, `offers.url`, `offers.priceValidUntil`,
  `offers.itemCondition`, shipping and return policy details.
- **Offer format:** `price` is a plain number (`49.00`), no symbol, no thousands
  separator; `priceCurrency` is an ISO 4217 code; `availability` is a full schema.org URL
  such as `https://schema.org/InStock`.
- **AggregateRating:** `ratingValue` and `reviewCount` (or `ratingCount`) are required;
  `bestRating` and `worstRating` default to 5 and 1. Include it only when the page shows
  the rating and the reviews behind it. Reviews of the organisation by itself
  ("self-serving" reviews) are not eligible for review snippets.

```json
{
  "@type": "Product",
  "@id": "https://www.kestrelbilling.example/pricing#growth",
  "name": "Kestrel Billing Growth plan",
  "description": "Usage-based billing for up to 5 million events per month.",
  "image": "https://www.kestrelbilling.example/img/growth-plan.png",
  "sku": "KB-GROWTH",
  "brand": { "@id": "https://www.kestrelbilling.example/#organization" },
  "offers": {
    "@type": "Offer",
    "url": "https://www.kestrelbilling.example/pricing",
    "price": "499.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2027-03-31"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "reviewCount": "87"
  }
}
```

## FAQPage

- **When:** the page contains a visible list of questions with the site's own answers.
  User-submitted questions with several answers are `QAPage`, not `FAQPage`.
- **Required:** `mainEntity`: a list of `Question` nodes, each with `name` and an
  `acceptedAnswer` of type `Answer` with `text`.
- **Answer text** may contain limited HTML (links, lists, bold, paragraphs).
- **Limits:** Google restricted FAQ rich results in 2023 to well-known government and
  health sites, so most sites will not see them. The markup is still valid, and it states
  the question-and-answer pairs unambiguously to any consumer that reads JSON-LD. Do not
  promise a visible result; do not add FAQ markup for content that is not on the page.

```json
{
  "@type": "FAQPage",
  "@id": "https://www.kestrelbilling.example/pricing#faq",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Can I change plans mid-cycle?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Upgrades apply immediately and are prorated; downgrades apply at the next renewal."
      }
    },
    {
      "@type": "Question",
      "name": "What happens when I exceed my event allowance?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Events beyond the allowance are billed at the overage rate shown on your plan, per 1,000 events."
      }
    }
  ]
}
```

## HowTo

- **When:** a page whose main content is an ordered procedure with distinct steps.
- **Required:** `name` and `step`: a list of `HowToStep` (each with `text`; `name`, `url`
  and `image` are optional but useful).
- **Recommended:** `image`, `totalTime` (ISO 8601 duration), `estimatedCost`, `supply`,
  `tool`.
- **Limits:** Google no longer shows HowTo rich results in search. The schema.org type
  remains valid and the steps are explicit for machine readers. Mark up only procedures
  that are on the page, in the same order.

```json
{
  "@type": "HowTo",
  "name": "Send your first usage event",
  "totalTime": "PT10M",
  "step": [
    { "@type": "HowToStep", "name": "Create a test-mode API key", "text": "In the dashboard, open Developers and create a key with the events:write scope." },
    { "@type": "HowToStep", "name": "Define a meter", "text": "Create a meter named api_calls that sums the quantity field of each event." },
    { "@type": "HowToStep", "name": "Post an event", "text": "Send a POST request to /v3/usage-events with the customer ID, meter name and quantity." }
  ]
}
```

## BreadcrumbList

- **When:** any page below the top level that shows a breadcrumb trail, or has a clear
  hierarchy.
- **Required:** `itemListElement`: `ListItem` nodes with `position` (starting at 1) and
  `name`; `item` (the URL) is required for every item except the last.
- **Consistency:** it mirrors the visible trail. Use canonical URLs for `item`.

```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.kestrelbilling.example/" },
    { "@type": "ListItem", "position": 2, "name": "API reference", "item": "https://www.kestrelbilling.example/api" },
    { "@type": "ListItem", "position": 3, "name": "Usage events" }
  ]
}
```

## LocalBusiness

- **When:** a business with a physical location or service area that customers visit or
  that serves a defined area. Use the most specific subtype (`Restaurant`, `Dentist`,
  `Store`, `ProfessionalService`).
- **Required:** `name` and `address` (a `PostalAddress`).
- **Recommended:** `telephone`, `url`, `geo`, `openingHoursSpecification`, `priceRange`,
  `image`, `areaServed`, `sameAs`.
- **Consistency:** name, address and phone must match the visible page and the business's
  other listings exactly. Mismatches weaken the entity.

```json
{
  "@type": "ProfessionalService",
  "@id": "https://www.kestrelbilling.example/contact#localbusiness",
  "name": "Kestrel Billing Lisbon Office",
  "url": "https://www.kestrelbilling.example/contact",
  "telephone": "+351-21-555-0100",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua Exemplo 10",
    "addressLocality": "Lisbon",
    "postalCode": "1200-001",
    "addressCountry": "PT"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:30"
    }
  ]
}
```

## SoftwareApplication

- **When:** a page for a downloadable or web application. Use `WebApplication` or
  `MobileApplication` where they fit.
- **Required (Google):** `name`, `offers` (with `price`, which may be `0`), and either
  `aggregateRating` or `review`.
- **Recommended:** `applicationCategory`, `operatingSystem`, `description`, `screenshot`,
  `softwareVersion`.
- **Note:** without ratings or reviews the markup is valid but not eligible for Google's
  software rich result. It still declares what the product is and what it costs.

```json
{
  "@type": "WebApplication",
  "@id": "https://www.kestrelbilling.example/product#app",
  "name": "Kestrel Billing",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free test mode" },
  "publisher": { "@id": "https://www.kestrelbilling.example/#organization" }
}
```

## Person

- **When:** an author page, a team page, a founder profile. Pair it with `ProfilePage` on
  the page that is about the person.
- **Required:** `name`. There is no Google rich result for it; its value is identity.
- **Recommended:** `url` (the page about the person), `image`, `jobTitle`, `worksFor`
  (reference to the `Organization`), `sameAs` (profiles that are verifiably the same
  person), `description`, `knowsAbout`.
- **Consistency:** the `Person` named in an article's `author` should be the same node
  (same `@id`) as the one on the author page.

```json
{
  "@type": "Person",
  "@id": "https://www.kestrelbilling.example/team/ines-varga#person",
  "name": "Ines Varga",
  "url": "https://www.kestrelbilling.example/team/ines-varga",
  "jobTitle": "Head of Billing Engineering",
  "worksFor": { "@id": "https://www.kestrelbilling.example/#organization" },
  "knowsAbout": ["usage-based billing", "revenue recognition"],
  "sameAs": ["https://www.linkedin.com/in/example-ines-varga"]
}
```

## Event

- **When:** a page for one event with a date, in person, online or both.
- **Required (Google):** `name`, `startDate` (ISO 8601; include the time zone offset when
  a time is given) and `location`: a `Place` with `name` and `address`, or a
  `VirtualLocation` with `url`.
- **Recommended:** `endDate`, `eventStatus`, `eventAttendanceMode`, `image`,
  `description`, `offers`, `organizer`, `performer`.
- **Upkeep:** update `eventStatus` for cancellations and postponements; remove or retire
  the markup when the event has passed and the page no longer promotes it.

```json
{
  "@type": "Event",
  "name": "Usage-based pricing workshop",
  "startDate": "2026-11-12T16:00:00+00:00",
  "endDate": "2026-11-12T17:30:00+00:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": { "@type": "VirtualLocation", "url": "https://www.kestrelbilling.example/events/pricing-workshop" },
  "organizer": { "@id": "https://www.kestrelbilling.example/#organization" },
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://www.kestrelbilling.example/events/pricing-workshop"
  }
}
```

## VideoObject

- **When:** a page where a video is the main content or a significant element, embedded
  in the page.
- **Required (Google):** `name`, `thumbnailUrl`, `uploadDate`.
- **Recommended:** `description`, `contentUrl` or `embedUrl`, `duration` (ISO 8601, for
  example `PT4M30S`), `hasPart` (`Clip` nodes for key moments), `expires`.
- **Consistency:** the video must be visible on the page and playable there.

```json
{
  "@type": "VideoObject",
  "name": "Prorations in four minutes",
  "description": "A walkthrough of the three proration modes with a worked example.",
  "thumbnailUrl": "https://www.kestrelbilling.example/img/prorations-video-thumb.jpg",
  "uploadDate": "2026-06-14T09:00:00+00:00",
  "duration": "PT4M12S",
  "embedUrl": "https://www.youtube.com/embed/EXAMPLE_VIDEO_ID"
}
```
