#!/usr/bin/env bash
# check_ai_access.sh — what AI answer engines get when they fetch a site.
#
# Usage: check_ai_access.sh <url>
# Prints: robots.txt rules for AI agents, status of llms.txt / llms-full.txt / sitemap,
#         and the HTTP status the page returns to several AI user-agents.
# Needs only curl. Read-only; makes a handful of GET requests.

set -u
URL="${1:-}"
if [ -z "$URL" ]; then echo "usage: $0 <url>" >&2; exit 2; fi
case "$URL" in http://*|https://*) ;; *) URL="https://$URL" ;; esac
ORIGIN="$(printf '%s' "$URL" | sed -E 's#^(https?://[^/]+).*#\1#')"
UA_DEFAULT="Mozilla/5.0 (compatible; era-geo-audit/1.0; +https://tryera.ai)"

fetch() { # fetch <url> <user-agent> -> "<status> <bytes>"
  curl -sS -L -o /tmp/era_geo_body.$$ -w '%{http_code} %{size_download}' \
    -A "$2" --max-time 20 "$1" 2>/dev/null || echo "000 0"
}

echo "== $ORIGIN"
echo
echo "-- robots.txt"
ROBOTS_STATUS="$(fetch "$ORIGIN/robots.txt" "$UA_DEFAULT")"
echo "status: $ROBOTS_STATUS"
if [ "${ROBOTS_STATUS%% *}" = "200" ]; then
  AGENTS='GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-SearchBot|Claude-User|anthropic-ai|Googlebot|Google-Extended|PerplexityBot|Perplexity-User|Bingbot|Applebot|Applebot-Extended|Meta-ExternalAgent|Amazonbot|DuckAssistBot|CCBot|Bytespider|cohere-ai'
  awk -v IGNORECASE=1 -v agents="$AGENTS" '
    BEGIN { n = split(agents, A, "|") }
    /^[Uu]ser-agent:/ { ua = $0; sub(/^[Uu]ser-agent:[ \t]*/, "", ua); sub(/[ \t]*$/, "", ua); cur = ua; next }
    /^([Dd]isallow|[Aa]llow):/ {
      if (cur == "*") { print "  [*] " $0; next }
      for (i = 1; i <= n; i++) if (tolower(cur) == tolower(A[i])) { print "  [" cur "] " $0 }
    }' /tmp/era_geo_body.$$
  echo "  (agents with no block of their own follow the [*] rules)"
fi

echo
echo "-- files"
for f in llms.txt llms-full.txt sitemap.xml sitemap_index.xml; do
  printf '  %-18s %s\n' "$f" "$(fetch "$ORIGIN/$f" "$UA_DEFAULT")"
done

echo
echo "-- page as seen by AI user-agents  (status bytes)"
while IFS='|' read -r label ua; do
  r="$(fetch "$URL" "$ua")"
  printf '  %-12s %s\n' "$r" "$label"
done <<EOF
GPTBot|GPTBot/1.2 (+https://openai.com/gptbot)
OAI-SearchBot|OAI-SearchBot/1.0; +https://openai.com/searchbot
ChatGPT-User|ChatGPT-User/1.0; +https://openai.com/bot
ClaudeBot|ClaudeBot/1.0; +claudebot@anthropic.com
Claude-User|Claude-User/1.0; +Claude-User@anthropic.com
PerplexityBot|PerplexityBot/1.0; +https://perplexity.ai/perplexitybot
Perplexity-User|Perplexity-User/1.0; +https://perplexity.ai/perplexity-user
Googlebot|Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
bingbot|Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)
browser|$UA_DEFAULT
EOF

echo
echo "-- page headers (default agent)"
curl -sS -L -I -A "$UA_DEFAULT" --max-time 20 "$URL" 2>/dev/null \
  | grep -i -E '^(HTTP/|content-type|x-robots-tag|link:|last-modified|cache-control|cf-|server:)' | sed 's/^/  /'

echo
echo "-- in-page signals (default agent)"
fetch "$URL" "$UA_DEFAULT" >/dev/null
B=/tmp/era_geo_body.$$
printf '  canonical:      %s\n' "$(grep -o -i '<link[^>]*rel=["'"'"']canonical["'"'"'][^>]*>' "$B" | head -1 | grep -o -i 'href=["'"'"'][^"'"'"']*' | sed 's/href=.//')"
printf '  robots meta:    %s\n' "$(grep -o -i '<meta[^>]*name=["'"'"']robots["'"'"'][^>]*>' "$B" | head -1 | grep -o -i 'content=["'"'"'][^"'"'"']*' | sed 's/content=.//')"
printf '  json-ld blocks: %s\n' "$(grep -o -i 'application/ld+json' "$B" | wc -l | tr -d ' ')"
printf '  h1:             %s\n' "$(sed -n 's/.*<h1[^>]*>\(.*\)<\/h1>.*/\1/ip' "$B" | head -1 | sed 's/<[^>]*>//g' | cut -c1-120)"
printf '  text bytes:     %s (of %s html)\n' "$(sed 's/<[^>]*>//g' "$B" | tr -s '[:space:]' ' ' | wc -c | tr -d ' ')" "$(wc -c < "$B" | tr -d ' ')"
rm -f /tmp/era_geo_body.$$
