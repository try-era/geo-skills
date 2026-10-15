#!/usr/bin/env python3
"""llms_txt_skeleton.py - print a draft llms.txt for a site.

Usage:
    python3 -I llms_txt_skeleton.py <source> [<source> ...] [options]

A <source> is one of:
    - a sitemap URL (urlset or sitemap index; .xml or .xml.gz),
    - a page URL (listed as a single page),
    - a path to a text file with one URL per line ('#' starts a comment),
    - '-' to read URLs from standard input.

Output:
    stdout  the draft llms.txt (H1, blockquote, H2 sections, "- [Title](url): description")
    stderr  what was included, what was dropped and why, and which entries need a human

The script is a starting point. It does not judge which pages matter; a person
(or the skill's selection step) still removes, merges and rewrites entries.
Only URLs found in the sources are fetched, only on the same host as the first
source, with a per-request timeout. One bad page never stops the run.
Standard library only; read-only GET requests.
"""

import argparse
import gzip
import html
import re
import socket
import ssl
import sys
import time
import zlib
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "era-geo-skills-llms-txt/1.0 (+https://tryera.ai)"
MAX_SITEMAP_BYTES = 20 * 1024 * 1024
MAX_PAGE_BYTES = 400 * 1024
MAX_SITEMAPS = 50
MAX_SITEMAP_DEPTH = 3
MAX_URLS_COLLECTED = 20000

# Paths that are almost never worth an AI agent's context.
EXCLUDE_RE = re.compile(
    r"(^|/)(cart|checkout|basket|login|log-in|signin|sign-in|signup|sign-up|register|"
    r"account|my-account|password|wp-admin|wp-json|cdn-cgi|feed|rss|search|tag|tags|"
    r"author|authors|404|thank-you|thanks|unsubscribe|preferences)(/|$)|"
    r"(^|/)page/\d+(/|$)|\.(pdf|jpg|jpeg|png|gif|webp|svg|zip|xml|json|css|js)$",
    re.IGNORECASE,
)
# Last-or-first segments that belong under "Optional".
OPTIONAL_SEGMENTS = {
    "privacy", "privacy-policy", "terms", "terms-of-service", "terms-and-conditions",
    "legal", "cookies", "cookie-policy", "careers", "jobs", "press", "media-kit",
    "security", "status", "accessibility", "imprint", "sitemap", "brand", "partners",
}
SECTION_PRIORITY = [
    "docs", "documentation", "guides", "guide", "learn", "tutorials", "api", "reference",
    "product", "products", "features", "solutions", "use-cases", "pricing", "plans",
    "integrations", "customers", "case-studies", "resources", "reports",
    "market-reports", "blog", "articles", "about", "company",
]
LOCALE_RE = re.compile(r"^[a-z]{2}(-[a-z]{2,4})?$", re.IGNORECASE)
TITLE_SEPARATORS = re.compile(r"\s+[|–—·:•-]+\s+|\s+::\s+")


def log(msg):
    print(msg, file=sys.stderr)


# --------------------------------------------------------------------------- fetching


def fetch(url, timeout, max_bytes):
    """Return (final_url, status, content_type, body_bytes). Raises on network errors."""
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*",
                                "Accept-Encoding": "gzip"})
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read(max_bytes + 1)
        ctype = resp.headers.get("Content-Type", "")
        if resp.headers.get("Content-Encoding", "").lower() == "gzip" or raw[:2] == b"\x1f\x8b":
            raw = gunzip(raw, max_bytes)
        return resp.geturl(), resp.status, ctype, raw[:max_bytes]


def gunzip(raw, max_bytes):
    """Decompress with a size cap so a decompression bomb cannot exhaust memory."""
    try:
        return zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(raw, max_bytes)
    except zlib.error:
        try:
            return gzip.decompress(raw)[:max_bytes]
        except Exception:
            return raw


def describe_error(exc):
    if isinstance(exc, HTTPError):
        return "HTTP %s" % exc.code
    if isinstance(exc, (socket.timeout, TimeoutError)):
        return "timeout"
    if isinstance(exc, URLError):
        reason = exc.reason
        if isinstance(reason, (socket.timeout, TimeoutError)):
            return "timeout"
        if isinstance(reason, ssl.SSLError):
            return "TLS error"
        return "network error: %s" % reason
    return "%s: %s" % (type(exc).__name__, exc)


# --------------------------------------------------------------------------- sitemaps

LOC_RE = re.compile(r"<loc>\s*(?:<!\[CDATA\[)?\s*(.*?)\s*(?:\]\]>)?\s*</loc>",
                    re.IGNORECASE | re.DOTALL)


def parse_sitemap(text):
    """Return ('index'|'urlset', [locs]). Regex on <loc> on purpose: no XML entity expansion."""
    kind = "index" if re.search(r"<sitemapindex", text, re.IGNORECASE) else "urlset"
    locs = [html.unescape(m.group(1)).strip() for m in LOC_RE.finditer(text)]
    return kind, [u for u in locs if u]


def decode(body, ctype=""):
    m = re.search(r"charset=([\w-]+)", ctype or "", re.IGNORECASE)
    for enc in ([m.group(1)] if m else []) + ["utf-8", "latin-1"]:
        try:
            return body.decode(enc, errors="replace")
        except LookupError:
            continue
    return body.decode("utf-8", errors="replace")


def looks_like_sitemap(url):
    try:
        path = urlparse(url).path.lower()
    except ValueError:
        return False
    return path.endswith((".xml", ".xml.gz")) or "sitemap" in path


def collect_from_sitemap(url, timeout, seen_maps, depth=0):
    """Yield page URLs from a sitemap or sitemap index, following index children."""
    if depth > MAX_SITEMAP_DEPTH or len(seen_maps) >= MAX_SITEMAPS or url in seen_maps:
        return
    seen_maps.add(url)
    try:
        final, status, ctype, body = fetch(url, timeout, MAX_SITEMAP_BYTES)
    except Exception as exc:  # noqa: BLE001 - report and continue
        log("sitemap skipped: %s (%s)" % (url, describe_error(exc)))
        return
    text = decode(body, ctype)
    if "<loc" not in text.lower():
        log("sitemap skipped: %s (no <loc> entries; status %s, %s)" % (url, status, ctype or "?"))
        return
    kind, locs = parse_sitemap(text)
    log("sitemap: %s -> %s, %d entries" % (url, kind, len(locs)))
    for loc in locs:
        if kind == "index":
            yield from collect_from_sitemap(loc, timeout, seen_maps, depth + 1)
        else:
            yield loc


# --------------------------------------------------------------------------- page parsing


class HeadParser(HTMLParser):
    """Collect title, meta description, canonical, robots, og tags, first h1, first paragraph."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.h1 = ""
        self.meta = {}
        self.canonical = ""
        self.first_p = ""
        self._in = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key and "content" in a and key not in self.meta:
                self.meta[key] = a["content"]
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = self.canonical or a.get("href", "")
        elif tag in ("title", "h1", "p"):
            if self._in is None and not (tag == "title" and self.title) \
                    and not (tag == "h1" and self.h1) and not (tag == "p" and self.first_p):
                self._in, self._buf = tag, []

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._in != tag:
            return
        text = clean(" ".join(self._buf))
        if tag == "title":
            self.title = text
        elif tag == "h1":
            self.h1 = text
        elif tag == "p" and len(text) >= 60:
            self.first_p = text
        self._in = None


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def parse_page(body, ctype):
    parser = HeadParser()
    try:
        parser.feed(decode(body, ctype))
        parser.close()
    except Exception:  # noqa: BLE001 - broken markup: keep whatever was collected
        pass
    return parser


# --------------------------------------------------------------------------- text helpers


def host_key(url):
    try:
        host = urlparse(url).netloc.lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def normalise(url):
    try:
        url, _ = urldefrag(url.strip())
    except ValueError:
        return url.strip()
    return url


def strip_site_name(title, site_name, host):
    """Drop 'Site | ' / ' - Site' decoration from a page title."""
    if not title:
        return ""
    parts = [p.strip() for p in TITLE_SEPARATORS.split(title) if p.strip()]
    if len(parts) < 2:
        return title.strip()
    flat = lambda t: re.sub(r"\W+", "", t.lower())  # noqa: E731 - "Era(R)" equals "era"
    label = flat(host.split(".")[0]) if host else ""
    names = {flat(site_name), label} - {""}
    kept = [p for p in parts if flat(p) not in names]
    return " - ".join(kept) if kept else parts[0]


def shorten(text, limit):
    text = clean(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:-")
    return cut + "..."


def md_escape(text):
    return text.replace("[", "(").replace("]", ")")


def title_case_segment(seg):
    return re.sub(r"[-_]+", " ", seg).strip().title() or "Pages"


def slug_title(url):
    segs = [s for s in urlparse(url).path.split("/") if s]
    return title_case_segment(segs[-1]) if segs else urlparse(url).netloc


# --------------------------------------------------------------------------- main logic


def read_sources(sources, timeout):
    """Return (ordered list of page URLs, primary host key)."""
    urls, host, seen_maps = [], None, set()
    for src in sources:
        if src == "-":
            items = [ln.strip() for ln in sys.stdin.read().splitlines()]
            found = [u for u in items if u and not u.startswith("#")]
        elif re.match(r"^https?://", src, re.IGNORECASE):
            if looks_like_sitemap(src):
                found = list(collect_from_sitemap(src, timeout, seen_maps))
                if not found:
                    log("note: %s gave no URLs; treating it as a page" % src)
                    found = [src]
            else:
                found = [src]
            host = host or host_key(src)
        else:
            try:
                with open(src, "r", encoding="utf-8", errors="replace") as fh:
                    found = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
            except OSError as exc:
                log("source skipped: %s (%s)" % (src, exc))
                continue
        urls.extend(found)
        if len(urls) > MAX_URLS_COLLECTED:
            urls = urls[:MAX_URLS_COLLECTED]
            log("note: stopped collecting at %d URLs" % MAX_URLS_COLLECTED)
            break
    if not host:
        for u in urls:
            if re.match(r"^https?://", u, re.IGNORECASE):
                host = host_key(u)
                break
    return urls, host


def prefilter(urls, host, locale_arg):
    """Drop off-host, non-HTTP, excluded-pattern and duplicate URLs. Returns (kept, dropped)."""
    kept, dropped, seen = [], [], set()
    for raw in urls:
        url = normalise(raw)
        try:
            parsed = urlparse(url)
        except ValueError:
            dropped.append((raw, "malformed URL"))
            continue
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            dropped.append((raw, "not an http(s) URL"))
        elif host and host_key(url) != host:
            dropped.append((url, "different host or port"))
        elif parsed.query:
            dropped.append((url, "has a query string (parameterised URL)"))
        elif EXCLUDE_RE.search(parsed.path):
            dropped.append((url, "utility or low-value path"))
        elif url in seen:
            dropped.append((url, "duplicate"))
        else:
            seen.add(url)
            kept.append(url)
    # Locale prefixes: keep one language, say so.
    first = [next((s for s in urlparse(u).path.split("/") if s), "") for u in kept]
    loc_counts = Counter(f.lower() for f in first if LOCALE_RE.match(f))
    if loc_counts and sum(loc_counts.values()) >= 0.3 * max(len(kept), 1):
        keep_loc = (locale_arg or loc_counts.most_common(1)[0][0]).lower()
        log("note: locale prefixes found %s; keeping /%s/ and unprefixed URLs "
            "(use --locale to change)" % (dict(loc_counts), keep_loc))
        still = []
        for u, f in zip(kept, first):
            if LOCALE_RE.match(f) and f.lower() != keep_loc:
                dropped.append((u, "other locale (/%s/)" % f.lower()))
            else:
                still.append(u)
        kept = still
    return kept, dropped


def pick_for_fetch(urls, limit):
    """Shallow pages first (hubs beat leaf pages), then sitemap order."""
    depth = lambda u: len([s for s in urlparse(u).path.split("/") if s])  # noqa: E731
    order = sorted(range(len(urls)), key=lambda i: (depth(urls[i]), i))
    chosen = set(order[:limit])
    return [u for i, u in enumerate(urls) if i in chosen]


def inspect_page(url, timeout):
    """Fetch one page; return a dict. Never raises."""
    try:
        return _inspect_page(url, timeout)
    except Exception as exc:  # noqa: BLE001 - last line of defence for one bad page
        return {"url": url, "ok": False, "reason": "unexpected error: %s" % describe_error(exc)}


def _inspect_page(url, timeout):
    info = {"url": url, "ok": False, "reason": ""}
    try:
        final, status, ctype, body = fetch(url, timeout, MAX_PAGE_BYTES)
    except Exception as exc:  # noqa: BLE001 - one bad page must not stop the run
        info["reason"] = describe_error(exc)
        return info
    if status != 200:
        info["reason"] = "HTTP %s" % status
        return info
    if "html" not in ctype.lower() and ctype:
        info["reason"] = "not HTML (%s)" % ctype.split(";")[0]
        return info
    if host_key(final) != host_key(url):
        info["reason"] = "redirects off-site to %s" % final
        return info
    page = parse_page(body, ctype)
    robots = page.meta.get("robots", "").lower()
    if "noindex" in robots:
        info["reason"] = "meta robots noindex"
        return info
    canonical = urldefrag(page.canonical.strip())[0] if page.canonical else ""
    if canonical and not re.match(r"^https?://", canonical):
        canonical = ""  # relative canonicals are reported as a warning by the skill, not resolved here
    info.update(
        ok=True,
        final=final,
        canonical=canonical,
        title=page.title or page.h1,
        h1=page.h1,
        site_name=page.meta.get("og:site_name", ""),
        description=(page.meta.get("description") or page.meta.get("og:description")
                     or page.first_p),
        from_first_p=not (page.meta.get("description") or page.meta.get("og:description"))
        and bool(page.first_p),
    )
    return info


def section_key(path_segments, sections):
    if not path_segments:
        return None
    first = path_segments[0].lower()
    return first if first in sections else None


def build_document(pages, args, host):
    """Group, order and print. Returns the llms.txt text."""
    site_name = args.site_name or next((p["site_name"] for p in pages if p.get("site_name")), "")
    site_name = site_name or (host.split(".")[0].replace("-", " ").title() if host else "Site")

    home = next((p for p in pages if urlparse(p["use_url"]).path in ("", "/")), None)
    summary = shorten(home["description"], 280) if home and home.get("description") else \
        "TODO: one or two sentences saying what this site or product is, who it is for, and what it covers."

    # A first segment is a "section" when at least two pages live under it.
    counts = Counter()
    for p in pages:
        segs = [s for s in urlparse(p["use_url"]).path.split("/") if s]
        if len(segs) >= 2:
            counts[segs[0].lower()] += 1
    sections = {k for k, n in counts.items() if n >= 2}

    groups = defaultdict(list)
    for p in pages:
        segs = [s for s in urlparse(p["use_url"]).path.split("/") if s]
        if segs and (segs[0].lower() in OPTIONAL_SEGMENTS or segs[-1].lower() in OPTIONAL_SEGMENTS):
            groups["__optional__"].append(p)
        else:
            groups[section_key(segs, sections) or "__key__"].append(p)

    def group_rank(name):
        if name == "__key__":
            return (0, 0, "")
        if name in SECTION_PRIORITY:
            return (1, SECTION_PRIORITY.index(name), name)
        return (2, 0, name)

    title_counts = Counter(p["title"] for p in pages if p["title"])
    desc_counts = Counter(p["description"] for p in pages if p.get("description"))

    lines = ["# %s" % md_escape(site_name), "", "> %s" % summary, ""]
    needs_work = 0
    names = sorted((g for g in groups if g != "__optional__"), key=group_rank)
    if "__optional__" in groups:
        names.append("__optional__")
    for name in names:
        items = sorted(groups[name], key=lambda p: (len([s for s in urlparse(p["use_url"]).path.split("/") if s]),
                                                    p["use_url"]))
        if name != "__optional__" and len(items) > args.max_per_group:
            log("group '%s': %d pages, listing the first %d (shallowest); pick the rest by hand"
                % (name, len(items), args.max_per_group))
            items = items[:args.max_per_group]
        heading = {"__key__": "Key pages", "__optional__": "Optional"}.get(name, title_case_segment(name))
        lines.append("## %s" % heading)
        lines.append("")
        for p in items:
            raw_title = p["title"]
            if title_counts[raw_title] > 1 and p["h1"] and p["h1"] != raw_title:
                raw_title = p["h1"]  # the <title> is shared with other pages; the H1 is more specific
            title = strip_site_name(raw_title, site_name, host) or slug_title(p["use_url"])
            if p.get("description") and desc_counts[p["description"]] > 1 and home is not p:
                desc = "TODO: this meta description is shared by %d pages; write one from the page" \
                    % desc_counts[p["description"]]
                needs_work += 1
            elif p.get("description") and not p["from_first_p"]:
                desc = shorten(p["description"], args.max_desc)
            elif p.get("description"):
                desc = "TODO (taken from first paragraph, check) " + shorten(p["description"], args.max_desc - 40)
                needs_work += 1
            else:
                desc = "TODO: describe what the reader finds here"
                needs_work += 1
            lines.append("- [%s](%s): %s" % (md_escape(shorten(title, 90)), p["use_url"], desc))
        lines.append("")
    log("entries needing a human description: %d" % needs_work)
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Print a draft llms.txt from a sitemap or URL list.",
                                 epilog="Diagnostics go to stderr; the draft goes to stdout.")
    ap.add_argument("sources", nargs="+", help="sitemap URL, page URL, file of URLs, or '-' for stdin")
    ap.add_argument("--limit", type=int, default=60, help="max pages to fetch (default 60)")
    ap.add_argument("--timeout", type=float, default=10.0, help="seconds per request (default 10)")
    ap.add_argument("--workers", type=int, default=4, help="parallel fetches (default 4)")
    ap.add_argument("--max-per-group", type=int, default=15, help="max entries per section (default 15)")
    ap.add_argument("--max-desc", type=int, default=160, help="max description length (default 160)")
    ap.add_argument("--site-name", default="", help="override the H1 / site name")
    ap.add_argument("--locale", default="", help="locale prefix to keep when URLs carry /en/, /de/ ...")
    args = ap.parse_args(argv)

    started = time.time()
    urls, host = read_sources(args.sources, args.timeout)
    if not urls:
        log("no URLs found in the given sources")
        return 1
    log("collected %d URLs; primary host: %s" % (len(urls), host or "unknown"))

    kept, dropped = prefilter(urls, host, args.locale)
    to_fetch = pick_for_fetch(kept, max(args.limit, 1))
    if len(kept) > len(to_fetch):
        log("note: %d candidate URLs; fetching the %d shallowest (--limit to change)"
            % (len(kept), len(to_fetch)))
        skipped = set(kept) - set(to_fetch)
        dropped.extend((u, "not fetched (over --limit)") for u in kept if u in skipped)

    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as pool:
        results = list(pool.map(lambda u: inspect_page(u, args.timeout), to_fetch))

    pages, seen_final = [], set()
    for info in results:
        if not info["ok"]:
            dropped.append((info["url"], info["reason"] or "failed"))
            continue
        use = info["canonical"] if info["canonical"] and host_key(info["canonical"]) == host else info["final"]
        use = normalise(use)
        if use != normalise(info["url"]):
            log("redirect/canonical: %s -> %s (listing the target)" % (info["url"], use))
        if use in seen_final:
            dropped.append((info["url"], "duplicate of %s after redirect/canonical" % use))
            continue
        seen_final.add(use)
        info["use_url"] = use
        pages.append(info)

    by_reason = defaultdict(list)
    for url, reason in dropped:
        by_reason[reason].append(url)
    for reason, items in by_reason.items():
        for url in items[:5]:
            log("excluded: %s  [%s]" % (url, reason))
        if len(items) > 5:
            log("excluded: ... and %d more  [%s]" % (len(items) - 5, reason))
    log("included: %d pages; excluded: %d; %.1fs" % (len(pages), len(dropped), time.time() - started))
    if not pages:
        log("nothing usable to write; check the sources and connectivity")
        return 1

    sys.stdout.write(build_document(pages, args, host or ""))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except BrokenPipeError:
        sys.exit(0)
