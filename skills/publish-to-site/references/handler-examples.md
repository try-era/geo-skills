# Handler examples

Minimal, working starting points for a webhook endpoint, plus a pull script. All of them
follow `webhook-contract.md`: verify the signature on the raw body, upsert by Era's article
id, keep the slug stable, answer with the post's URL. Replace the storage with the site's
own database or CMS call; the structure stays the same.

The signing secret is read from the environment (`ERA_SIGNING_SECRET`). Do not write it into
code, a config file in the repository, or a log.

## Node.js (Express)

Node 18 or later, `npm i express`, run as an ES module (`server.mjs`).

```js
import crypto from 'node:crypto';
import express from 'express';

const SECRET = process.env.ERA_SIGNING_SECRET;
if (!SECRET) throw new Error('ERA_SIGNING_SECRET is not set');
const BLOG_BASE_URL = (process.env.BLOG_BASE_URL ?? 'https://example.com/blog').replace(/\/$/, '');
const MAX_SKEW_SECONDS = 300;

// Stand-in for a database table with a UNIQUE index on era_article_id.
const posts = new Map(); // era_article_id -> post
const slugsInUse = new Set();

function signatureIsValid(timestamp, signature, rawBody) {
  if (!/^\d{1,12}$/.test(timestamp)) return false;
  if (Math.abs(Date.now() / 1000 - Number(timestamp)) > MAX_SKEW_SECONDS) return false;

  const expected = Buffer.from(
    'v1=' +
      crypto.createHmac('sha256', SECRET).update(`${timestamp}.`).update(rawBody).digest('hex'),
  );
  const received = Buffer.from(signature);
  // timingSafeEqual throws on different lengths, so compare lengths first.
  return expected.length === received.length && crypto.timingSafeEqual(expected, received);
}

function pickSlug(article) {
  let slug = article.slug || article.id;
  if (slugsInUse.has(slug)) slug = `${slug}-${article.id.slice(0, 8)}`;
  slugsInUse.add(slug);
  return slug;
}

function upsertPost(article) {
  const existing = posts.get(article.id);
  const post = {
    id: existing?.id ?? crypto.randomUUID(),
    slug: existing?.slug ?? pickSlug(article), // never move the URL on an update
    title: article.title, // html carries no title: render this yourself
    excerpt: article.excerpt,
    html: article.html,
    heroImage: article.featured_image?.url ?? null,
    product: article.sub_product?.name ?? null,
  };
  posts.set(article.id, post);
  return post;
}

const app = express();

// express.raw keeps the body as untouched bytes. Do not put express.json() in front of this
// route, and raise the limit: long articles exceed the 100 kB default.
app.post('/era-webhook', express.raw({ type: 'application/json', limit: '10mb' }), (req, res) => {
  const rawBody = req.body;
  const timestamp = req.get('X-Era-Timestamp') ?? '';
  const signature = req.get('X-Era-Signature') ?? '';
  if (!Buffer.isBuffer(rawBody) || !signatureIsValid(timestamp, signature, rawBody)) {
    return res.status(401).json({ error: 'invalid signature' });
  }

  let event;
  try {
    event = JSON.parse(rawBody.toString('utf8'));
  } catch {
    return res.status(400).json({ error: 'invalid json' });
  }

  if (event.event === 'ping') return res.status(200).json({ ok: true });

  if (event.event === 'article.publish') {
    const post = upsertPost(event.article);
    // If going live takes time (a rebuild), answer 202 here without a url and report the
    // url afterwards with report_article_published.
    return res.status(200).json({ url: `${BLOG_BASE_URL}/${post.slug}`, id: post.id });
  }

  return res.status(200).json({ ignored: event.event }); // unknown events still get a 2xx
});

app.listen(process.env.PORT ?? 3000);
```

With a real database, the upsert is one statement (SQLite and Postgres syntax). The slug is
left out of the `UPDATE` so the URL never moves:

```sql
INSERT INTO posts (id, era_article_id, slug, title, excerpt, html, hero_image_url)
VALUES ($1, $2, $3, $4, $5, $6, $7)
ON CONFLICT (era_article_id) DO UPDATE SET
  title = excluded.title, excerpt = excluded.excerpt,
  html = excluded.html, hero_image_url = excluded.hero_image_url;
```

## Python (FastAPI)

`pip install fastapi uvicorn`, run with `uvicorn app:app`. Storage is the standard-library
`sqlite3`, so the file runs as it is.

```python
import hashlib
import hmac
import json
import os
import sqlite3
import time
import uuid
from contextlib import closing

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

SECRET = os.environ["ERA_SIGNING_SECRET"].encode("utf-8")
BLOG_BASE_URL = os.environ.get("BLOG_BASE_URL", "https://example.com/blog").rstrip("/")
DB_PATH = os.environ.get("POSTS_DB", "posts.db")
MAX_SKEW_SECONDS = 300

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id             TEXT PRIMARY KEY,
    era_article_id TEXT NOT NULL UNIQUE,
    slug           TEXT NOT NULL UNIQUE,
    title          TEXT NOT NULL,
    excerpt        TEXT,
    html           TEXT NOT NULL,
    hero_image_url TEXT,
    product        TEXT
)
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    return conn


def signature_is_valid(timestamp: str, signature: str, raw_body: bytes) -> bool:
    if not (timestamp.isdigit() and len(timestamp) <= 12):
        return False
    if abs(time.time() - int(timestamp)) > MAX_SKEW_SECONDS:
        return False
    expected = "v1=" + hmac.new(
        SECRET, timestamp.encode() + b"." + raw_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected.encode(), signature.encode())


def upsert_post(article: dict) -> dict:
    slug = article.get("slug") or article["id"]
    with closing(connect()) as conn, conn:  # the inner "conn" commits on exit
        clash = conn.execute(
            "SELECT 1 FROM posts WHERE slug = ? AND era_article_id != ?", (slug, article["id"])
        ).fetchone()
        if clash:
            slug = f"{slug}-{article['id'][:8]}"
        # The slug is not in the UPDATE list, so a re-delivery never moves the URL.
        conn.execute(
            """
            INSERT INTO posts (id, era_article_id, slug, title, excerpt, html, hero_image_url, product)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (era_article_id) DO UPDATE SET
                title = excluded.title, excerpt = excluded.excerpt, html = excluded.html,
                hero_image_url = excluded.hero_image_url, product = excluded.product
            """,
            (
                str(uuid.uuid4()),
                article["id"],
                slug,
                article["title"],
                article.get("excerpt"),
                article["html"],
                (article.get("featured_image") or {}).get("url"),
                (article.get("sub_product") or {}).get("name"),
            ),
        )
        row = conn.execute(
            "SELECT id, slug FROM posts WHERE era_article_id = ?", (article["id"],)
        ).fetchone()
    return {"id": row[0], "slug": row[1]}


app = FastAPI()


@app.post("/era-webhook")
async def era_webhook(request: Request):
    raw_body = await request.body()  # bytes; do not declare a parsed body parameter
    if not signature_is_valid(
        request.headers.get("x-era-timestamp", ""),
        request.headers.get("x-era-signature", ""),
        raw_body,
    ):
        return JSONResponse({"error": "invalid signature"}, status_code=401)

    try:
        event = json.loads(raw_body)
    except ValueError:
        return JSONResponse({"error": "invalid json"}, status_code=400)

    if event.get("event") == "ping":
        return {"ok": True}

    if event.get("event") == "article.publish":
        post = await run_in_threadpool(upsert_post, event["article"])
        return {"url": f"{BLOG_BASE_URL}/{post['slug']}", "id": post["id"]}

    return {"ignored": event.get("event")}  # unknown events still get a 2xx
```

If two different articles race for the same slug, the `UNIQUE` constraint raises, the
request fails with a `5xx`, and Era retries it; the second attempt sees the clash and picks
the suffixed slug.

Flask instead of FastAPI: keep `signature_is_valid` and `upsert_post`, and change the route.

```python
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.post("/era-webhook")
def era_webhook():
    raw_body = request.get_data()  # read the bytes before touching request.json
    if not signature_is_valid(
        request.headers.get("X-Era-Timestamp", ""),
        request.headers.get("X-Era-Signature", ""),
        raw_body,
    ):
        return jsonify(error="invalid signature"), 401
    try:
        event = json.loads(raw_body)
    except ValueError:
        return jsonify(error="invalid json"), 400
    if event.get("event") == "ping":
        return jsonify(ok=True)
    if event.get("event") == "article.publish":
        post = upsert_post(event["article"])
        return jsonify(url=f"{BLOG_BASE_URL}/{post['slug']}", id=post["id"])
    return jsonify(ignored=event.get("event"))
```

## Send a signed ping from a terminal

Run this against the deployed endpoint (or a tunnel to a local one) before connecting it in
Era. `read -rs` keeps the secret out of the shell history.

```bash
read -rs SECRET                      # paste the signing secret, press Enter
BODY='{"event":"ping","delivery_id":"local-test","sent_at":"2026-10-09T12:00:00Z"}'
TS=$(date +%s)
SIG=$(printf '%s.%s' "$TS" "$BODY" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')

curl -i https://example.com/era-webhook \
  -H 'Content-Type: application/json' \
  -H 'X-Era-Event: ping' \
  -H 'X-Era-Delivery: local-test' \
  -H "X-Era-Timestamp: $TS" \
  -H "X-Era-Signature: v1=$SIG" \
  --data-binary "$BODY"
```

`200` means verification works. Change one character of `$SIG` and run it again: it must
answer `401`. A `401` on the correct signature points at the secret, the timestamp, or a
body parser that ran first.

## Pull script for `api` delivery

For a cron job or CI step (Python 3.10 or later). It needs a write-scoped key in
`ERA_API_KEY` (reporting needs write; reading works with any key) and `ERA_BRAND_ID`. Set
`ERA_CONNECTION_ID` only when the brand has several Custom sites. An agent does the same
through the MCP tools; see SKILL.md.

```python
import datetime
import os
import sys

import requests

ERA = "https://app.tryera.ai/api/v1"
BRAND_ID = os.environ["ERA_BRAND_ID"]
CONNECTION_ID = os.environ.get("ERA_CONNECTION_ID")

http = requests.Session()
http.headers["X-API-Key"] = os.environ["ERA_API_KEY"]


def error_code(resp: requests.Response) -> str | None:
    try:
        return resp.json()["detail"]["code"]
    except (ValueError, KeyError, TypeError):
        return None


def due_articles() -> list[dict]:
    """Every ready article due today or earlier, across all pages."""
    params = {
        "ready_to_publish": "true",
        "due_before": datetime.date.today().isoformat(),
        "limit": 100,
    }
    if CONNECTION_ID:
        params["connection_id"] = CONNECTION_ID
    items, offset = [], 0
    while True:
        resp = http.get(
            f"{ERA}/brands/{BRAND_ID}/articles", params={**params, "offset": offset}, timeout=30
        )
        resp.raise_for_status()
        page = resp.json()
        items += page["items"]
        offset += len(page["items"])
        if not page["items"] or offset >= page["total_count"]:
            return items


def publish_on_site(article: dict) -> str:
    """Create or update the post keyed by article["id"], deploy it, and return its live URL.
    Return only once the post is reachable: reporting tells Era it is published."""
    raise NotImplementedError


def main() -> None:
    for item in due_articles():  # collected first: reported articles leave the list
        try:
            params = {"include": "html"}
            if CONNECTION_ID:
                params["connection_id"] = CONNECTION_ID
            resp = http.get(f"{ERA}/articles/{item['id']}", params=params, timeout=60)
            resp.raise_for_status()
            url = publish_on_site(resp.json())

            body = {"url": url}
            if CONNECTION_ID:
                body["connection_id"] = CONNECTION_ID
            report = http.post(f"{ERA}/articles/{item['id']}/published", json=body, timeout=30)
            if error_code(report) == "PUBLISHING_DISABLED":
                sys.exit("Publishing is switched off for this Era environment; stopping.")
            report.raise_for_status()
            print("published", item["id"], url)
        except Exception as exc:  # the next run picks the article up again
            print("skipped", item["id"], exc)


if __name__ == "__main__":
    main()
```
