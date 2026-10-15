# AI crawlers and fetchers

Engines use different agents for *training*, *search indexing* and *on-demand fetching*.
A `robots.txt` rule hits one of them, not all three. Audit each family separately and name
the effect, not just the rule.

| Engine family | User-agent | What it does | Blocking it means |
| --- | --- | --- | --- |
| OpenAI / ChatGPT | `GPTBot` | Collects pages for model training | No effect on ChatGPT search results |
| | `OAI-SearchBot` | Builds the index ChatGPT search answers from | The site cannot appear as a ChatGPT search source |
| | `ChatGPT-User` | Fetches a page when a user asks about it or pastes a link | ChatGPT cannot read the page on request |
| Anthropic / Claude | `ClaudeBot` | Training crawler | No effect on Claude's search or fetch |
| | `Claude-SearchBot` | Search indexing | Pages drop from Claude's search results |
| | `Claude-User` | On-demand fetch during a conversation | Claude cannot read the page when asked |
| Google | `Googlebot` | The web index that AI Overviews and AI Mode draw from | Removal from Google search and AI Overviews |
| | `Google-Extended` | Controls use for Gemini training and grounding | Gemini may not use the content; Google search unaffected |
| Perplexity | `PerplexityBot` | Index for Perplexity answers | Pages drop from Perplexity sources |
| | `Perplexity-User` | On-demand fetch for a user request | Perplexity cannot open the page when asked |
| Microsoft / Copilot | `Bingbot` | Bing index, used by Copilot | Removal from Bing and Copilot answers |
| Apple | `Applebot` | Siri / Spotlight index | Removal from Apple surfaces |
| | `Applebot-Extended` | Apple foundation-model training | Search unaffected |
| Meta | `Meta-ExternalAgent` | Training and product crawling | |
| Amazon | `Amazonbot` | Alexa answers | |
| DuckDuckGo | `DuckAssistBot` | DuckDuckGo AI answers | |
| Common Crawl | `CCBot` | Open crawl many models train on | |
| ByteDance | `Bytespider` | Training crawler | |
| Cohere | `cohere-ai` | Training crawler | |

## Reading the rules

- A `User-agent: *` block applies to every agent that has no block of its own. Most AI
  agents honour a specific block over the wildcard.
- `Disallow: /` under a training agent is a legitimate choice. `Disallow: /` under a search
  or fetch agent removes the site from that engine's answers — flag it as a finding unless
  the user confirms it is intended.
- `noindex` removes the page from indexes; `nosnippet` and `max-snippet:0` stop engines
  from quoting it even when indexed. Both are score-relevant.
- `Crawl-delay` is ignored by most AI agents; do not count on it.
- Check the CDN or WAF too: a bot-management rule that returns 403 to unknown agents blocks
  every fetcher in this table regardless of `robots.txt`. The `check_ai_access.sh` script
  requests the page with several of these user-agents and reports the status codes.

## Recommended baseline

For a page that should be cited: allow `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`,
`Claude-User`, `PerplexityBot`, `Perplexity-User`, `Googlebot`, `Bingbot`, `Applebot`,
`DuckAssistBot`. Decide on the training agents (`GPTBot`, `ClaudeBot`, `Google-Extended`,
`Applebot-Extended`, `CCBot`, `Bytespider`, `Meta-ExternalAgent`) as a policy question and
write the answer down in `robots.txt` explicitly, so the choice is visible.
