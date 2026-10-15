# Webhook contract

What Era sends to a Custom site with `webhook` delivery, what the endpoint must answer, and
what happens when it does not. Hand this to whoever builds the endpoint. The pull
(`api`) delivery is covered at the end.

Source of truth: Era's guide "Publish to a custom site" (app.tryera.ai/docs/guides/publish-to-custom-site).
If something here disagrees with the connection's settings page or the guide, the guide wins.

## Summary for the developer

One public HTTPS route that accepts `POST` with a JSON body and does four things, in order:

1. **Verify** the signature on the raw body. Reject anything that fails with `401`.
2. **Upsert** the article by `article.id`. Never key on `slug`.
3. **Publish** the post on the site.
4. **Reply** `2xx`, with `{"url": "...", "id": "..."}` when the post is already live.

Answer pings too. Ignore event types you do not know, but still answer `2xx`.

## Request

Method `POST`, to the connection's webhook URL (an absolute `https` URL, publicly
reachable, no credentials, no redirect).

| Header | Value |
| --- | --- |
| `Content-Type` | `application/json` |
| `User-Agent` | `Era-Webhooks/1.0` |
| `X-Era-Event` | `ping` or `article.publish` |
| `X-Era-Delivery` | UUID of this delivery; the same across the automatic retries of one delivery |
| `X-Era-Timestamp` | Unix time in seconds at which the request was signed |
| `X-Era-Signature` | `v1=<hex>`, an HMAC-SHA256 of the timestamp and the raw body |

### Ping

Sent by the connection test (and by the dashboard when it saves the connection). It only
checks that the endpoint verifies signatures and answers.

```json
{ "event": "ping", "delivery_id": "6f1c0e52-9b7a-4d63-8f0e-2a5c1d9e7b34", "sent_at": "2026-10-09T12:00:00Z" }
```

### Article

```json
{
  "event": "article.publish",
  "action": "create",
  "delivery_id": "6f1c0e52-9b7a-4d63-8f0e-2a5c1d9e7b34",
  "sent_at": "2026-10-09T12:00:00Z",
  "article": {
    "id": "0b6e4f1a-3c2d-4a8b-9e17-5d6f7a8b9c0d",
    "title": "How to choose a trail running shoe",
    "slug": "how-to-choose-a-trail-running-shoe",
    "excerpt": "Grip, drop, and cushioning: what actually matters off-road.",
    "html": "<h2>Start with the terrain</h2><p>…</p><figure><img src=\"https://app.tryera.ai/api/storage/…\" alt=\"…\"><figcaption>…</figcaption></figure>",
    "markdown": "## Start with the terrain\n\n…",
    "featured_image": { "url": "https://app.tryera.ai/api/storage/…", "alt": "A runner on a ridge trail" },
    "social_image": { "url": "https://app.tryera.ai/api/storage/…", "alt": "…" },
    "infographics": [{ "number": 1, "url": "https://app.tryera.ai/api/storage/…", "alt": "…" }],
    "sub_product": null
  },
  "previous": null
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `event` | string | `ping` or `article.publish`; same as `X-Era-Event`. |
| `action` | string | `article.publish` only. `create` the first time Era delivers this article to the connection; `update` when it re-sends one the site already has. |
| `delivery_id`, `sent_at` | string | Same as `X-Era-Delivery`; ISO 8601 UTC. |
| `previous` | object or null | `null` on `create`. On `update`: `{"external_id", "url"}`, what Era has on record: the `id` the endpoint returned (or the article id if it never returned one) and the post's URL (`null` if Era never learned it). |
| `article.id` | string | Stable Era id. The upsert key. |
| `article.title` | string | Not repeated inside `html`; render it yourself. |
| `article.slug` | string | A suggested slug. Not guaranteed unique forever; do not key on it. |
| `article.excerpt` | string | Short summary for meta descriptions and index pages; falls back to the title when the article has no prose paragraph. |
| `article.html` | string | The body as an HTML fragment: no `<html>`, no `<body>`, no title. Images are inline `<figure>` elements. |
| `article.markdown` | string or null | The same body as Markdown. |
| `article.featured_image`, `article.social_image` | object or null | `{url, alt}`. The social image is sized for link previews. |
| `article.infographics` | array | `{number, url, alt}`; already inlined in `html`. May be empty. |
| `article.sub_product` | object or null | `{id, name, url}` when the brand has sub-products; the article closes with a call to action to that `url`. Use it to file the post by product. The key is always present. |

Image URLs are public: hotlink them or re-host them.

### Updates

Era re-sends an article as `update` when, for example, a newer article goes live and the
links in an older one are refreshed, or when its images move to new storage. Update the
existing post in place and keep its URL stable. Never create a second post.

## Signature

```text
signature = "v1=" + hex( HMAC_SHA256( key = signing secret (UTF-8),
                                       message = X-Era-Timestamp + "." + raw request body ) )
```

Verify in this order:

1. Read the **raw body bytes** before any JSON parsing. Re-serialised JSON has different
   bytes and will not match.
2. Reject the request if `X-Era-Timestamp` is not an integer, or is more than **5 minutes**
   from your clock.
3. Compute the expected value and compare it to `X-Era-Signature` with a **constant-time**
   comparison.
4. Only then parse the JSON.

The signing secret is shown once, when the connection is created through the API or the
agent tools, and cannot be recovered or rotated. Store it on the server (environment
variable `ERA_SIGNING_SECRET`), never in front-end code, a repository or a log. In the
dashboard the user chooses it instead (at least 32 characters; a Generate button fills one in).

Test the verification before connecting by sending a signed ping from a terminal; the
command is in `handler-examples.md`.

## Response

Any `2xx` means delivered. Optional JSON body:

```json
{ "url": "https://example.com/blog/how-to-choose-a-trail-running-shoe", "id": "post_8812" }
```

| Field | What Era does with it |
| --- | --- |
| `url` | Becomes the Visit page link in the content calendar and is used for links between articles. A relative path is joined to the connection's blog URL; a URL on a private or internal address is ignored. |
| `id` | The site's own id for the post. Era sends it back as `previous.external_id` on updates. If omitted, Era keeps the id it has, or uses the article id the first time. |

If publishing takes a while (a static-site rebuild), answer `202 Accepted` at once without a
`url`. Era marks the article posted but has no link to show. When the post is live, send the
URL with `report_article_published` (or `POST /api/v1/articles/{article_id}/published`, which
needs a write-scoped key). The first URL reported this way also makes Era re-send, as
`update` deliveries, the older articles that link to the new post.

## Retries and limits

| The endpoint returns | Era does |
| --- | --- |
| `2xx` | Delivered. |
| `3xx` | Treated as an error. Redirects are never followed; put the final URL in the connection. |
| `4xx` except `408` and `429` | Failed, not retried. Fix the cause, then press Retry on the article in the calendar. |
| `5xx`, `408`, `429`, no answer within 15 seconds, connection error | Retried up to two more times (after about 2 s, then about 8 s) within the same delivery, then marked failed. |
| TLS certificate error | Failed at once, not retried. |

- 15 seconds per attempt and about 70 seconds per whole delivery. Do slow work in the
  background and answer first.
- Era reads at most 64 KB of the response.
- `https` only. Private and internal addresses (`localhost`, `10.x`, `192.168.x`) are
  refused when the connection is tested, so the endpoint must be public; use a tunnel while
  developing.
- The certificate is verified against the host in the webhook URL.
- Raise the server's request-body limit: long articles exceed the 100 KB default of common
  frameworks.
- The error message is shown on the article in the calendar.

## Idempotency

Retries and manual Retry presses can deliver an article the site already processed,
sometimes while the first attempt is still running.

- Upsert by `article.id`, with a unique index so concurrent requests cannot both insert.
- Do not regenerate the slug on update.
- `X-Era-Delivery` repeats across the automatic retries of one delivery; use it to drop
  exact duplicates if you want to.

## Connection states

| `status` | Meaning |
| --- | --- |
| `error` | New webhook connection ("Awaiting verification"), or a test that failed. Receives nothing. |
| `active` | A test passed. Can be a publishing destination. |
| `disabled` | Set with `update_publishing_destination(status="disabled")`. A passing test re-activates it. |

- `create_publishing_destination` starts a webhook as `error`; an `api` connection is `active`
  at once and has no secret.
- Editing never pings. A new webhook URL puts the connection back to `error` until it is tested.
- The delivery mode is fixed at creation (`DELIVERY_IMMUTABLE`). There is no delete: to switch
  mode, create a new connection and disable the old one.
- `test_publishing_destination` returns `ok: false` and the reason in `error` for a failed ping;
  that is not an HTTP error.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Test fails, `ok: false` | The ping must get a `2xx` that is not an HTML page: a catch-all route or login page answering 200 is rejected. The endpoint must be reachable from the internet, answer pings, and hold the same secret. A `401` from your own verification is the most common cause. |
| Signature never matches | A body parser ran before the handler, or JSON was re-serialised; the signed string is not `"<timestamp>."` plus the bytes; the secret has stray whitespace or quotes. |
| Error mentions a redirect | The URL answers `3xx` (`http` to `https`, `www` to the bare domain, a missing trailing slash). Use the final URL. |
| Private or internal address refused | Use a public host or a tunnel. |
| `413 Payload Too Large` | Raise the body limit. |
| Deliveries time out | Answer inside 15 seconds; move rebuilds and image work to the background. |
| TLS handshake error | The certificate is expired, self-signed, or for another host. |
| Duplicate posts | The handler inserts on every request; look up by `article.id`. |
| No Visit page link | The response had no `url`; return it, or report it later. |
| Article failed after a `4xx` | `4xx` is not retried. Fix it and press Retry on the article. |

## Pull delivery (`api`)

Era sends nothing. The site, a job, or an agent asks for ready articles and reports URLs.

| Step | MCP tool | REST (`/api/v1`) |
| --- | --- | --- |
| Find the connection | `list_publishing_destinations(brand_id)` | `GET /brands/{brand_id}/publishing-connections` |
| List what is due | `list_articles(brand_id, ready_to_publish=True, due_before=<today>, connection_id, limit, offset)` | `GET /brands/{brand_id}/articles?ready_to_publish=true&due_before=YYYY-MM-DD` |
| Fetch publish-ready article | `get_article(article_id, include_html=True, connection_id)` | `GET /articles/{article_id}?include=html` |
| Report the live URL | `report_article_published(article_id, url, connection_id, external_id, published_at)` | `POST /articles/{article_id}/published` |

- `ready_to_publish=True` returns blog articles whose text and images are done and that this
  site has not published; it implies `platform="blog"` and replaces `editable_only`.
  `due_before` takes a date; articles with no date count as due.
- Pages: `limit` is at most 100; keep going until `offset + len(items) >= total_count`.
- `html` has no title; render `title` yourself. Publish `html`, not the stored Markdown.
- Several Custom sites on the brand: pass `connection_id` to all three calls.
- Reporting is idempotent; the same URL again changes nothing, a different URL replaces the
  earlier one. Once reported, the article leaves the ready list and is locked against edits.

| Status | Code | Action |
| --- | --- | --- |
| 409 | `NO_CUSTOM_SITE_CONNECTION` | No enabled Custom site on the brand. Create one with delivery `api`. |
| 409 | `CONNECTION_DISABLED` | A passing connection test re-activates it, or report against another site. |
| 409 | `ARTICLE_NOT_READY` | Try again on a later run. Not an error to surface. |
| 409 | `NOT_A_BLOG_ARTICLE`, `TEST_ARTICLE` | Era publishes that lane itself, or it is a test. Skip; do not retry. |
| 422 | `CONNECTION_ID_REQUIRED` | The brand has several Custom sites. Pass `connection_id`. |
| 422 | `URL_NOT_PUBLIC` | Private address or a host that does not resolve. Report the real public URL. |
| 422 | `ARTICLE_HAS_NO_BRAND` | Only brand articles can be reported. Do not retry. |
| 404 | `CONNECTION_NOT_FOUND` | Not a Custom site of this brand. Take the id from the destinations list. |
| 404 | `PUBLISHING_DISABLED` | Publishing is switched off for the environment. Stop and tell the user. |
| 403 | none | Reporting needs a write-scoped key, and the brand must be on the Content plan. |
| 401 | none | Missing or invalid `X-API-Key`. |

Do not retry `4xx` responses unchanged, except `ARTICLE_NOT_READY`. `5xx` responses are safe
to retry with backoff because every call is idempotent.
