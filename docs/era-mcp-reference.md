# Era MCP tool reference

Server: `https://app.tryera.ai/api/mcp` (Streamable HTTP; OAuth sign-in, or `Authorization: Bearer era_…` for an API key). REST twin: `https://app.tryera.ai/api/v1` with `X-API-Key: era_…`; Swagger at `/api/v1/docs`.

Start every session with `list_brands` (or `whoami`) to get a `brand_id`. Read tools work with any key; write tools need a write-scoped key. Tools flagged **destructive** should be confirmed with the user first.

## read tools

### `get_answer`
- scope: read · params: `answer_id`*, `brand_id`*
- The full verbatim AI answer for one monitoring run, plus the sources it cited and the sub-queries it ran. ``answer_id`` comes from ``list_answers``. Use this to read exactly what an engine said about the brand.

### `get_article`
- scope: read · params: `article_id`*, `connection_id`, `include_html`
- Get one article with its full Markdown body. ``is_editable`` says whether it can still be changed (and ``not_editable_reason`` why not). The body may contain ``<IMAGE_INFOGRAPHICS_N>caption</IMAGE_INFOGRAPHICS_N>`` markers — these are where Era splices in generated figures, so keep every one of them intact when rewriting or the image is silently dropped. ``sub_product`` (``{id, name, url}`` or ``null``) is the product the article is written for; its closing call to action links to that ``url``. Also returns ``excerpt`` (the title when the article has no prose paragraph), ``featured_image`` and ``social_image`` (``{url, alt}``) and ``publications`` — where the article already went out, with each destination's ``status`` and public ``url``. Set ``include_html=True`` when you are about to publish the article on the user's own site: ``html`` is then the publish-ready body fragment (infographics inlined as ``<figure>``, links to the brand's other articles resolved to their live URLs; the title is not part of it). It is the same body a webhook would carry, except that outbound links which 404 are not unlinked here. It roughly doubles the response, so leave it off for reading and editing. ``connection_id`` (from ``list_publishing_destinations``) picks whose live URLs the links resolve to. With ``include_html=True`` it is required when the brand has several custom sites: without it the call fails with ``CONNECTION_ID_REQUIRED`` — pick the right ``custom_site`` and call again. An id that is not a connection of this brand fails with ``CONNECTION_NOT_FOUND``.

### `get_article_context`
- scope: read · params: `article_id`*, `sections`
- Get the data Era used to write the article, so a rewrite stays on-brief. ``sections`` is a comma-separated subset of: ``keywords`` (target keywords with AI/Google search volume, difficulty and intent), ``brand`` (positioning, ICP, point of view, tone-of-voice prompt, confirmed competitors), ``cluster`` (the topic cluster the article was assigned and the real AI-search queries behind it), ``quality`` (readability panel scores and the humanization pass result). Every section is size-capped. Request only what you need — asking for all four on a large brand fills a lot of context.

### `get_brand_analytics`
- scope: read · params: `brand_id`*, `days`
- Full AEO analytics for a brand: visibility, share of voice, sentiment and citation stats plus per-provider and daily timeseries. The broad 'show me everything about this brand' tool. ``days`` limits the window.

### `get_brand_dashboard`
- scope: read · params: `brand_id`*, `days`
- Get an at-a-glance AEO dashboard for one brand. Summarizes how the brand appears across the AI answer engines it is monitored on: visibility, share of voice, sentiment, average position and citation counts. ``brand_id`` comes from ``list_brands``; ``days`` limits the time window (omit for the default window).

### `get_brand_kit`
- scope: read · params: `brand_id`*
- Get the brand kit: what every article is written with. ``brand_id`` comes from ``list_brands``. Returns ``about_brand``, ``ideal_customer_profile`` and ``brand_point_of_view`` (each ``null`` until set). Brand assets such as logos are not included. Change them with ``update_brand_kit``.

### `get_brand_visibility`
- scope: read · params: `brand_id`*, `days`
- How visible the brand is in AI answers: overall visibility %, average position, and the per-provider + daily visibility timeseries (is it trending up on ChatGPT vs Perplexity?).

### `get_competitor_analytics`
- scope: read · params: `brand_id`*, `competitor_id`*, `days`
- Visibility, share of voice and citations for ONE tracked competitor over the window: visibility %, current/average SoV, avg_rank (order-of-mention position proxy), citation count and per-domain citation sources. ``competitor_id`` comes from list_competitors. Note: sentiment is not tracked per-competitor.

### `get_content_plan`
- scope: read · params: `brand_id`*
- Get the brand's content plan: the season in progress and the next one. ``brand_id`` comes from ``list_brands``. Content-plan brands only. Returns ``active`` (the season in progress) and ``scheduled`` (the next season, built ahead; ``null`` until then) — each ``null`` when there is none. A season has its ``id`` (the ``plan_id`` that ``list_plan_topics`` / ``approve_topics`` take), ``status``, ``plan_size``, ``segment_quotas`` (how it splits between the hub and the sub-products) and ``counts`` of its blog articles (``topics``: awaiting approval, ``approved``, ``generated``, ``published``). No article rows — list them with ``list_plan_topics``. Both ``null`` means no season exists yet: ``start_content_workflow`` creates the first. Topics can be approved only in the season under ``active`` (see ``approve_topics``); the ``scheduled`` one's can be read and renamed, not approved. Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `get_content_settings`
- scope: read · params: `brand_id`*
- Get a brand's content settings: season shape, pipeline steps, tone, schedule. ``brand_id`` comes from ``list_brands``. Content-plan brands only. Returns ``is_running`` (the workflow is armed: articles are generated and published on schedule), ``categories_confirmed`` (a plan cannot be generated before the mix is confirmed), ``plan_size`` (articles per 30-day season; set by Era) and ``category_mix`` (``keyword``, ``glossary``, ``versus``, ``top5``, ``howto`` — summing to ``plan_size``), ``steps`` (each optional pipeline step on or off), ``tone_of_voice_id`` (``null`` = the default blog tone; ids come from ``list_tones``), ``publish_hour_utc`` and ``publish_destination_ids`` (ids from ``list_publishing_destinations``), ``blog_publish_enabled``, ``publish_lanes`` (other lanes that publish at that hour: ``youtube``, ``medium``, ``substack``), ``plan_status`` and ``upgrade_available``. Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan; tell the user to upgrade it in the Era dashboard.

### `get_glossary`
- scope: read · params: none
- Definitions of the AEO metrics Era reports (visibility, share of voice, sentiment, position, citation) so the terms are interpreted consistently.

### `get_keyword_suggestion_run`
- scope: read · params: `brand_id`*, `run_id`*
- Check a keyword Suggest run: whether it has finished and what it added. ``brand_id`` comes from ``list_brands``; ``run_id`` from ``suggest_keywords``. ``status`` is ``pending`` or ``running`` (poll again in a minute or two — runs take several minutes), ``completed`` (``keywords_added`` is the number of new keywords; read them with ``list_keywords``) or ``failed`` (``error`` is a short generic reason, not a diagnosis). A failed run does not count against the monthly runs: start another with ``suggest_keywords`` if the user still wants one. Fix and retry — ``KEYWORD_SUGGESTION_NOT_FOUND``: no run with that id on this brand; use the ``run_id`` that ``suggest_keywords`` returned.

### `get_keyword_usage`
- scope: read · params: `brand_id`*
- Get the brand's monthly allowance of paid keyword actions and what is left. ``brand_id`` comes from ``list_brands``. Returns ``chat_used`` / ``chat_limit`` (volume checks: each ``check_keyword_volumes`` call and each ``add_keywords`` call with ``check_volumes`` on is one, however many keywords it carries), ``suggest_used`` / ``suggest_limit`` (``suggest_keywords`` runs) and ``resets_at`` (the subscription's monthly billing date). Read it before spending either quota and tell the user what remains.

### `get_sentiment`
- scope: read · params: `brand_id`*, `days`
- Sentiment of AI mentions of the brand: aggregate score, positive/neutral/ negative counts, and the daily sentiment timeseries.

### `get_share_of_voice`
- scope: read · params: `brand_id`*, `days`
- Share of voice for the brand vs competitors: current/average SoV, the daily SoV timeseries, and the per-competitor SoV breakdown.

### `get_sub_product_analytics`
- scope: read · params: `brand_id`*, `date_from`, `date_to`, `days`
- Compare AI visibility by sub-product: one row for the hub, one per sub-product. ``brand_id`` comes from ``list_brands``. Each row has the segment's active prompts, measured unbranded answers (``response_count``), ``mention_count``, ``visibility`` (% of those answers mentioning the brand) and ``avg_position`` over the window; the rows add up to the brand-wide numbers. The hub row is ``segment: "hub"`` (prompts outside every sub-product). The window is ``days`` (anchored at now) or an explicit ``date_from`` + ``date_to`` (``YYYY-MM-DD``, inclusive, UTC; both required together, ``date_to`` not in the future). Omit all three for the default window. Fix and retry — a 422 "date_from and date_to must be provided together" (or a reversed / future range): correct the dates.

### `get_top_citations`
- scope: read · params: `brand_id`*, `days`
- Which sources AI engines cite about the brand: citation stats (totals, unique sources, how often the brand's own site is cited) and the top cited links.

### `list_answers`
- scope: read · params: `brand_id`*, `date_from`, `date_to`, `limit`, `offset`, `prompt_id`, `provider`
- List the AI answers behind the brand's metrics: for each monitoring run, the engine, model, prompt, date, whether the brand was mentioned and at what position, and a text preview. Filter by ``provider`` (e.g. 'openai'), ``prompt_id`` or an ISO date range (``date_from``/``date_to``). Take an ``answer_id`` from here and pass it to ``get_answer`` for the full text.

### `list_articles`
- scope: read · params: `brand_id`*, `connection_id`, `due_before`, `editable_only`, `limit`, `offset`, `platform`, `ready_to_publish`, `sub_product_id`
- List a brand's generated articles. Call this to find an ``article_id``. Defaults to articles that can still be changed — ready (or already edited) and not yet published anywhere. Pass ``editable_only=False`` to also see published and not-yet-written ones. ``brand_id`` comes from ``list_brands``. ``total`` is the number of items in this page; ``total_count`` is the number of matching articles across all pages (page with ``offset`` until ``offset + total >= total_count``). To find what the user's own site should publish next, call ``list_articles(brand_id, ready_to_publish=True, due_before=<today>)`` — ``due_before`` is today's date (``YYYY-MM-DD``; articles with no scheduled date count as due). ``ready_to_publish=True`` returns only blog articles whose text and images are done and that are not yet published or publishing on the user's custom site; having gone out to WordPress or another destination does not hide them. It overrides ``editable_only`` and already implies ``platform="blog"``. ``connection_id`` (from ``list_publishing_destinations``) picks the custom site that is judged; by default it is all of the brand's custom sites. Each item's own ``ready_to_publish`` flag is judged the same way. Each item's ``sub_product`` is the product the article is written for (``{id, name, url}``; its call to action links to ``url``) when the brand has sub-products, else ``null``. ``sub_product_id`` lists one product's articles only (an ``id`` seen in ``sub_product``); ``sub_product_id="hub"`` lists the ones about the brand as a whole. ``updated_at`` moves only when the article itself changes (for example its images are replaced), not when links to newer articles get resolved. To pick those links up, re-fetch posts you already published every now and then with ``get_article(include_html=True)`` and update them in place.

### `list_brands`
- scope: read · params: `limit`, `offset`
- List the brands your Era workspace tracks. Call this FIRST to discover a ``brand_id`` for the other tools. Returns id, name and website domain per brand, plus pagination info.

### `list_cited_domains`
- scope: read · params: `brand_id`*, `days`, `limit`
- The brand's citation sources aggregated by domain — each domain with its citation count and share of all external citations — plus own_brand_cited_count (citations pointing at the brand's own site). The 'which sites does AI cite about us' view. For individual URLs instead of domains, see get_top_citations.

### `list_competitors`
- scope: read · params: `brand_id`*
- List the brand's tracked competitors (id, name, website, confirmed status). Use the ids with get_competitor_analytics (per-competitor visibility/SoV) or delete_competitor. For the brand-vs-competitors SoV split, see get_share_of_voice.

### `list_keyword_clusters`
- scope: read · params: `brand_id`*, `sub_product_id`
- List the topic clusters the content plan draws from, highest priority first. ``brand_id`` comes from ``list_brands``. Each cluster has a name, its priority (``priority_rank`` 1 = first), volume totals, ``member_count`` and its top 20 keywords. The clusters are rebuilt automatically after a Suggest run or a segment change, so a brand that has just been set up may have none yet — an empty list is not an error. ``sub_product_id`` (from ``list_sub_products``, or ``"hub"``) narrows to one segment. Fix and retry — ``INVALID_SUB_PRODUCT_ID``: ``sub_product_id`` is neither a sub-product id nor ``hub``.

### `list_keywords`
- scope: read · params: `brand_id`*, `include_hidden`, `limit`, `offset`, `order`, `search`, `sort`, `sub_product_id`
- List a brand's keywords — what its content plan is written from. ``brand_id`` comes from ``list_brands``. Each item has an ``id`` (for ``assign_keywords`` / ``archive_keyword``), the ``keyword``, its ``status`` (``active``: used for content; ``hidden``: stored but below the volume/relevance gate, or never checked), ``ai_search_volume`` (monthly searches in AI assistants; ``null`` = never checked), Google volume, difficulty, intent and the ``sub_product_id`` segment it sits in (``null`` = the brand itself). ``limit`` is 1-100 per page; page with ``offset`` until ``offset + len(items)`` reaches ``total`` (all rows matching the filters). ``counts`` (active / hidden) stay brand-wide whatever the filters. ``sort`` is one of ``ai_search_volume`` (default), ``relevance``, ``search_volume``, ``cpc``, ``keyword_difficulty``, ``keyword``, ``created_at``, ``gsc_clicks``, ``gsc_impressions``, ``gsc_position``; ``order`` is ``asc`` or ``desc``. ``search`` is a substring match. Archived keywords are never listed; ``include_hidden=True`` also lists the hidden ones. ``sub_product_id`` narrows to one segment: a sub-product's ``id`` (from ``list_sub_products``) or ``"hub"`` for the keywords about the brand as a whole. Fix and retry — ``INVALID_SUB_PRODUCT_ID``: ``sub_product_id`` is neither a sub-product id nor ``hub``.

### `list_plan_topics`
- scope: read · params: `limit`, `offset`, `plan_id`*, `status`, `sub_product_id`
- List a season's topics and articles in calendar order. ``plan_id`` is the ``id`` of ``active`` / ``scheduled`` from ``get_content_plan``. Each item has an ``id`` (the ``article_id`` for ``update_plan_topic`` / ``approve_topics``; once written, also for ``get_article``), ``title``, ``status``, ``scheduled_publish_date``, ``platform`` (``blog`` or a Medium / Substack lane), ``content_intent`` (the category it was planned as) and its ``sub_product``. ``status`` narrows to one stage — ``topic`` lists what still awaits approval; others are ``approved``, ``draft``, ``generating``, ``generated``, ``edited``, ``failed``. ``sub_product_id`` (from ``list_sub_products``, or ``"hub"``) narrows to one segment. ``limit`` is 1-100; page with ``offset`` until it reaches ``total``. The ``scheduled`` season's topics can be read here (and renamed with ``update_plan_topic``) but not approved — ``approve_topics`` takes the ``active`` season only. Fix and retry — ``PLAN_NOT_FOUND``: no such plan in this workspace; take the id from ``get_content_plan``. ``INVALID_SUB_PRODUCT_ID``: neither a sub-product id nor ``hub``. Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `list_prompts`
- scope: read · params: `active_only`, `brand_id`*
- List the brand's monitoring prompts plus the capacity (used/cap/remaining) against the brand's active-prompt limit. Use the ids with update_prompt / delete_prompt / swap_prompts.

### `list_providers`
- scope: read · params: `brand_id`*
- The AI answer engines this brand is monitored on, plus every provider selectable on the platform. Use the values to scope ``list_answers`` by provider, or to read per-engine metrics.

### `list_publishing_destinations`
- scope: read · params: `brand_id`*
- List where a brand's articles can be published: its connected destinations. Each item has ``id`` (the ``connection_id``), ``platform`` (``custom_site``, ``wordpress``, …), ``name``, ``status`` and ``site_base_url``. For a Custom site, ``delivery`` is ``webhook`` (Era pushes signed articles to the user's endpoint — nothing for you to do) or ``api`` (the user's site, or you on its behalf, pulls articles and reports the URL). No credentials are included. Call this before publishing on the user's own site: it shows whether a Custom site is connected, and which ``connection_id`` to pass to ``list_articles`` / ``get_article`` / ``report_article_published`` when the brand has several. Content-plan brands only. ``brand_id`` comes from ``list_brands``. If publishing is switched off for the account the call fails with ``PUBLISHING_DISABLED``.

### `list_search_queries`
- scope: read · params: `brand_id`*, `limit`, `offset`, `order`, `search`, `sort_by`, `sub_product_id`
- The search sub-queries AI engines actually ran about the brand, enriched with topic cluster paths, the providers that generated them, share of voice and competitor counts. ``sort_by`` is count|created_at|query; ``order`` is asc|desc. ``sub_product_id`` narrows to one product's queries (an ``id`` from ``list_sub_products``) or, as ``"hub"``, to the brand-level ones. A query belongs to the segment of the prompts that produced it (most prompts wins, a tie goes to the hub). An unknown sub-product id just returns no rows. Fix and retry — ``INVALID_SUB_PRODUCT_ID``: the value is neither a sub-product id nor ``hub``.

### `list_sub_products`
- scope: read · params: `brand_id`*, `include_inactive`
- List the brand's sub-products (its products/tools), in display order. ``brand_id`` comes from ``list_brands``. Each item has an ``id`` (the ``sub_product_id`` the keyword, article and search-query tools take), ``name``, ``url``, ``is_active``, its monitoring ``topic_id`` and ``prompt_count`` (monitored prompts; ``0`` right after creation while they are generated). ``include_inactive=True`` also lists deactivated ones. Also returns ``sub_products_enabled`` (whether the feature is switched on for the brand — if ``false`` every write except ``deactivate_sub_product`` is refused with ``SUB_PRODUCTS_DISABLED`` and only Era can turn it on), ``active_count`` and ``max_sub_products`` (the per-brand cap, deactivated ones included).

### `list_tones`
- scope: read · params: `brand_id`*
- List the brand's tones of voice, default tones first. ``brand_id`` comes from ``list_brands``. Each tone has an ``id`` (pass it as ``tone_of_voice_id`` to ``update_content_settings``, or to ``update_tone`` / ``delete_tone``), ``name``, ``platform`` (``null`` = any), the ``master_prompt`` its articles are written to, ``is_default`` (the brand's default for that platform) and ``is_system`` (created by Era: editable, not deletable).

### `list_topics`
- scope: read · params: `brand_id`*, `selected_only`
- The topics organising the brand's monitoring prompts (id, name, type, whether actively monitored). ``selected_only`` limits to monitored topics.

### `whoami`
- scope: read · params: none
- Identify the workspace and permissions behind your API key. Returns the team/workspace id, the API key's name, and its scopes (``read`` and optionally ``write``). Use this to confirm a key works and to check whether write tools are available before calling them.

## chart tools

### `chart_brand_dashboard`
- scope: read · params: `brand_id`*, `days`
- Render an interactive AEO dashboard for a brand: KPI cards (visibility, share of voice, sentiment, citations) plus visibility-by-engine, sentiment-over-time and competitor share-of-voice charts. The visual 'how is my brand doing' view.

### `chart_brand_visibility`
- scope: read · params: `brand_id`*, `days`
- Render a line chart of the brand's visibility over time, one line per AI engine (ChatGPT, Perplexity, Gemini, …).

### `chart_sentiment`
- scope: read · params: `brand_id`*, `days`
- Render an area chart of the brand's sentiment score over time.

### `chart_share_of_voice`
- scope: read · params: `brand_id`*, `days`
- Render a horizontal bar chart of share of voice for the brand vs its top competitors (highest first).

## write tools

### `activate_sub_product`
- scope: write · params: `brand_id`*, `sub_product_id`*
- Reactivate a deactivated sub-product: monitoring and content planning resume. ``brand_id`` comes from ``list_brands``; ``sub_product_id`` from ``list_sub_products(include_inactive=True)``. Monitoring restarts with a fresh batch of prompts and the sub-product rejoins the content plan. On a sub-product that is already active but has no prompts it retries prompt generation (at most once an hour). Returns the sub-product. Fix and retry — ``SUB_PRODUCT_NOT_FOUND``: use an id from ``list_sub_products``. Do not retry — ``SUB_PRODUCTS_DISABLED``: sub-products are not switched on for this brand.

### `add_competitor`
- scope: write · params: `aliases`, `brand_id`*, `description`, `name`*, `website_url`
- Add a tracked competitor to the brand.

### `add_keywords`
- scope: write · params: `brand_id`*, `check_volumes`, `keywords`*, `sub_product_id`
- Add keywords to the brand's Keywords Database; Era measures their volumes. **Spends one of the brand's monthly volume checks** (one per call, however many keywords) while ``check_volumes`` is on, so confirm with the user before calling and look at ``get_keyword_usage`` for what is left. ``brand_id`` comes from ``list_brands``. ``keywords`` is 1-1000 phrases, normalized (lowercase, trimmed) and deduplicated; blanks, junk and phrases over 250 characters are dropped and counted in ``dropped``. You cannot supply volumes — Era measures each keyword's AI search volume itself and keywords with demand become ``active``. Repeating a keyword the brand already has is harmless (``created: false``); an archived one comes back. ``sub_product_id`` (from ``list_sub_products``) adds them into that sub-product's segment — keywords the brand already has are moved into it too. Omitted: new keywords land in the hub (the brand as a whole) and existing ones stay put. ``check_volumes=False`` skips the measurement and spends nothing, but new keywords are stored ``hidden`` until checked. If the monthly checks are already used up the keywords are still stored without volumes (new ones hidden) and the response carries a ``notice`` saying when the allowance resets — relay it to the user rather than retrying. ``volumes_checked`` tells whether a measurement ran. **If the call times out or the connection drops, do NOT blindly retry** — the keywords may already be stored and the check spent. Look at ``list_keywords`` (``search`` for one of them) and ``get_keyword_usage`` (did ``chat_used`` rise?) first. Fix and retry — ``NO_VALID_KEYWORDS``: every input was blank, a duplicate, too long or not a keyword. ``SUB_PRODUCT_NOT_FOUND``: use an id from ``list_sub_products``. ``SUB_PRODUCT_INACTIVE``: the sub-product is deactivated; call ``activate_sub_product`` first. Transient — ``VOLUME_LOOKUP_FAILED`` (503): the volume provider did not answer. Nothing was stored and no check was spent; retry in a few minutes. Do not retry — ``VOLUME_LOOKUP_UNAVAILABLE`` (503): volume lookups are not configured on this Era server, so waiting will not help; tell the user to contact Era support. ``SUB_PRODUCTS_DISABLED``: sub-products are not switched on for this brand (Era enables them); stop and tell the user.

### `add_prompts`
- scope: write · params: `brand_id`*, `contents`*, `prompt_type`
- Add one or more monitoring prompts to a brand. Fails (with capacity info) if it would exceed the brand's active-prompt cap — use swap_prompts to add-by-removing. Returns the created prompts and the new capacity.

### `add_sub_products`
- scope: write · params: `brand_id`*, `items`*
- Add 1-50 sub-products (products/tools with their own page) to a brand. ``brand_id`` comes from ``list_brands``. ``items`` is a list of objects with a ``name``, a ``url`` (the product's absolute http(s) page) and an optional ``description``. Each new sub-product starts its own monitoring prompts, gets day-one keywords and takes a share of the content plan, so add only the products the user named. Returns the brand's full sub-product list (deactivated ones included); the new ones' ``id`` is what the keyword and article tools take as ``sub_product_id``. **Slow:** Era fetches each product page before answering, which can take tens of seconds. If the call times out or the connection drops, do NOT blindly retry — the sub-products may already be saved. Call ``list_sub_products`` first; retrying a saved URL fails with ``DUPLICATE_URL``. Fix and retry — ``DUPLICATE_URL``: the brand already has a sub-product with that URL (or the list repeats one); the message names it — drop it or use ``update_sub_product``. A 422 "Invalid arguments" means a bad ``url`` or a blank ``name``. Do not retry — ``SUB_PRODUCT_CAP``: the brand is at its sub-product cap, and deactivated ones count; tell the user. ``SUB_PRODUCTS_DISABLED``: sub-products are not switched on for this brand (Era enables them); tell the user.

### `apply_article_edit` **destructive**
- scope: write · params: `article_id`*, `proposal_id`*
- Commit a proposed rewrite. Only call this once the user has approved the diff. Replaces the article body, marks it as edited, and keeps the previous version as a revision the user can restore from the Era dashboard. Fails if the proposal expired, was already applied, was superseded by a newer one, or the article changed after it was proposed.

### `approve_topics`
- scope: write · params: `article_ids`*, `generate_images`, `plan_id`*
- Approve 1-10 topics for writing now. **Each approved topic is one full paid generation** (research, text and, with ``generate_images``, images) — confirm with the user which topics and how many before calling. ``plan_id`` comes from ``get_content_plan``; ``article_ids`` are topic ``id`` values from ``list_plan_topics(status="topic")``, at most 10 per call (there is no approve-all). All or nothing: if any id is not a topic of this plan nothing is approved. The running workflow already approves topics on its own a few days ahead of their dates — approve here only to get specific ones written sooner. Only the season in progress can have topics approved (its ``status`` is ``active`` or ``publishing``): take ``plan_id`` from ``active`` in ``get_content_plan``, never from ``scheduled``. Returns ``approved`` ids and ``articles_enqueued``; the articles appear in ``list_articles`` when written. Fix and retry — ``PLAN_NOT_FOUND``: take ``plan_id`` from ``get_content_plan``. ``PLAN_NOT_IN_PROGRESS``: this plan is not in progress (for example the next season, built ahead, or a finished one); call ``get_content_plan`` and approve the topics of its ``active`` plan instead. ``ARTICLE_NOT_FOUND``: an id is not in this plan. ``NOT_A_TOPIC``: one of them was already approved; re-list with ``list_plan_topics(status="topic")`` and approve only the ones still awaiting. Do not retry — ``GENERATION_BLOCKED``: the brand's subscription is not live, so nothing can be generated; the user must renew it. ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `archive_keyword` **destructive**
- scope: write · params: `brand_id`*, `keyword_id`*
- Archive a keyword: it stops feeding the content plan and Suggest won't re-add it. ``brand_id`` comes from ``list_brands``; ``keyword_id`` from ``list_keywords``. Reversible with ``restore_keyword`` (use the ``id`` in this response). Returns the archived keyword. Fix and retry — ``KEYWORD_NOT_FOUND``: no keyword with that id on this brand.

### `assign_keywords`
- scope: write · params: `brand_id`*, `keyword_ids`*, `sub_product_id`*
- Move keywords into a sub-product's segment, or back to the hub. ``brand_id`` comes from ``list_brands``; ``keyword_ids`` (1-1000) from ``list_keywords``. ``sub_product_id`` is required: an active sub-product's ``id`` (from ``list_sub_products``), or ``null`` to move the keywords back to the hub (the brand as a whole). The affected segments are re-clustered in the background. ``updated`` counts keywords actually moved — unknown ids and keywords already in the target segment are ignored, not rejected. Fix and retry — ``SUB_PRODUCT_NOT_FOUND``: use an id from ``list_sub_products``. ``SUB_PRODUCT_INACTIVE``: call ``activate_sub_product`` first. Do not retry — ``SUB_PRODUCTS_DISABLED``: sub-products are not switched on for this brand.

### `check_keyword_volumes`
- scope: write · params: `brand_id`*, `keywords`*
- Measure the AI search volume of up to 1000 keywords without adding them. **Spends one of the brand's monthly volume checks** (one per call, billed only when the lookup succeeds; ``get_keyword_usage`` shows what is left), so confirm with the user first. ``brand_id`` comes from ``list_brands``. To add keywords there is no need to check first — ``add_keywords`` measures them itself — so use this only to preview or compare. Returns ``items`` (highest AI volume first; ``ai_search_volume``, Google ``search_volume`` best effort, and ``in_database``: the brand already has it), ``checked`` and ``dropped`` (inputs that were blank, duplicate, junk or too long). **If the call times out or the connection drops, do NOT blindly retry** — the check may already have been spent: compare ``get_keyword_usage`` (``chat_used``) before calling again. Fix and retry — ``NO_VALID_KEYWORDS``: nothing usable in ``keywords``. Transient — ``VOLUME_LOOKUP_FAILED`` (503): the volume provider did not answer; nothing was billed. Retry in a few minutes. Do not retry — ``QUOTA_EXHAUSTED``: the monthly checks are used up; the message says when they reset. Tell the user. ``VOLUME_LOOKUP_UNAVAILABLE`` (503): volume lookups are not configured on this Era server; tell the user to contact Era support.

### `create_publishing_destination`
- scope: write · params: `brand_id`*, `delivery`*, `name`*, `site_base_url`, `webhook_url`
- Connect the user's own site as a Custom site publishing destination. ``brand_id`` comes from ``list_brands``. ``name`` is a label shown in the dashboard (up to 255 characters). ``delivery`` is ``webhook`` (Era POSTs each article to ``webhook_url`` as signed JSON; ``webhook_url`` is required and must be an absolute https URL) or ``api`` (the user's site pulls ready articles over the API and reports the URL back, as in ``list_publishing_destinations``; ``webhook_url`` must be left out). ``site_base_url`` is the blog's public address, used for links between articles. Only a Custom site can be created here; other platforms are connected by the user in the dashboard (Settings → Integrations). **The response carries the webhook's ``signing_secret`` exactly once.** Era never shows it again and cannot recover it. Give it to the user right away — it must be stored on their site, where it verifies the ``X-Era-Signature`` header — and do not paste it into logs, files in the repository or later messages. ``api`` delivery has no secret (``signing_secret`` is ``null``). A new ``webhook`` connection is ``error`` ("Awaiting verification") and receives nothing until the site is deployed with the secret and ``test_publishing_destination`` passes; an ``api`` connection is ``active`` at once. Use the returned ``connection.id`` as the destination id in ``update_content_settings``. Fix and retry — ``INVALID_WEBHOOK_URL``: ``webhook_url`` is not an absolute https URL with a host (and no credentials in it). A 422 "Invalid arguments" otherwise means ``webhook_url`` is missing for ``webhook`` delivery or present for ``api``. Do not retry — ``PUBLISHING_DISABLED``: publishing is switched off for this account; stop and tell the user. ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `create_tone`
- scope: write · params: `brand_id`*, `description`, `is_default`, `master_prompt`*, `name`*, `platform`
- Create a tone of voice for the brand's articles. ``brand_id`` comes from ``list_brands``. ``master_prompt`` (up to 8000 characters) is the writing instruction every article in this tone gets — describe voice, register, sentence length, what to avoid, with a short example if helpful. ``name`` is up to 120 characters, ``description`` up to 2000. ``platform`` limits it to a platform (``blog``, ``medium``, ``substack``, ``reddit``, ``x``, ``linkedin``); omitted = any. ``is_default=True`` makes it the brand's default for its platform. Pick it for the brand's articles with ``update_content_settings(tone_of_voice_id=<id>)``. Content-plan brands only. Returns the tone. Fix and retry — a 422 "Invalid arguments" means a field is empty or over its length limit. Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `deactivate_sub_product`
- scope: write · params: `brand_id`*, `sub_product_id`*
- Deactivate a sub-product — the way to remove one; nothing is deleted. ``brand_id`` comes from ``list_brands``; ``sub_product_id`` from ``list_sub_products``. It leaves the content plan and its prompts stop being monitored; history stays and ``activate_sub_product`` brings it back. It still counts against the brand's sub-product cap. Always allowed, even when sub-products are switched off. Returns the sub-product. Fix and retry — ``SUB_PRODUCT_NOT_FOUND``: use an id from ``list_sub_products``.

### `delete_competitor` **destructive**
- scope: write · params: `brand_id`*, `competitor_id`*
- Remove a tracked competitor from the brand.

### `delete_prompt` **destructive**
- scope: write · params: `brand_id`*, `prompt_id`*
- Deactivate (stop monitoring) a prompt, freeing a slot against the cap. Returns the brand's new capacity.

### `delete_tone` **destructive**
- scope: write · params: `tone_id`*
- Delete a tone the brand created. ``tone_id`` comes from ``list_tones``. Content settings that pointed at it fall back to the default tone; articles already written are untouched. Era's own (system) tones cannot be deleted. Returns an empty object on success. Fix and retry — ``TONE_NOT_FOUND``: use an id from ``list_tones``. Do not retry — ``SYSTEM_TONE``: Era's default tones can be edited with ``update_tone`` but not deleted. ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `propose_article_edit`
- scope: write · params: `article_id`*, `content`*, `note`, `title`
- Stage a rewrite and get back a diff. **This does not change the article.** Pass the complete new body in ``content`` (Markdown, keeping every ``<IMAGE_INFOGRAPHICS_N>`` marker) — not a patch or a fragment. You MUST show the returned ``diff`` to the user and get their explicit approval before calling ``apply_article_edit``. Do not chain the two calls on your own initiative. The proposal expires after an hour, supersedes any earlier pending one for the same article, and is rejected at apply time if the article changed in the meantime — in which case re-read it with ``get_article`` and propose again rather than retrying the same body.

### `report_article_published`
- scope: write · params: `article_id`*, `connection_id`, `external_id`, `published_at`, `url`*
- Tell Era that YOU published an article on the user's own site, and where. Call this only after the post is live at ``url`` (an absolute http(s) URL on a public host) — never for a draft or a post you have only written. **This publishes nothing**: Era just records what the site already did. The article then shows as posted in the content calendar, "Visit page" links to ``url``, and newer articles link to it. Idempotent: reporting the same URL again changes nothing, and a different ``url`` replaces the earlier one (use that if the post moved). Optional: ``external_id`` — your own id for the post (defaults to the id already on record, else the article id); ``published_at`` — ISO 8601 time it went live (defaults to now); ``connection_id`` — which Custom site, only when the brand has several. Needs a Custom site connection on the brand. Errors carry a code: Fix and retry — ``NO_CUSTOM_SITE_CONNECTION``: there is none (or none enabled); ask the user to connect one in Era (Settings → Integrations → Custom site, delivery "API"), then retry. ``CONNECTION_ID_REQUIRED``: the brand has several; call ``list_publishing_destinations``, pick the right ``custom_site`` and pass its ``id`` as ``connection_id``. ``CONNECTION_NOT_FOUND``: that id is not a Custom site of this brand. ``CONNECTION_DISABLED``: that site is disabled; a passing Test connection in Settings → Integrations re-activates it. ``URL_NOT_PUBLIC``: the URL's host is private/internal or does not resolve — report the post's real public URL (plain ``http`` is fine for a public host). Transient — ``ARTICLE_NOT_READY``: the article is not ready yet (for example still being written). Skip it for now; it becomes ready later and then shows up in ``list_articles(ready_to_publish=True)``. Not an error to surface to the user. Do not retry — ``NOT_A_BLOG_ARTICLE`` / ``TEST_ARTICLE``: Era publishes that article itself, or it is a test run; it is not one your site publishes. ``ARTICLE_HAS_NO_BRAND``: only brand articles can be reported. ``PUBLISHING_DISABLED``: publishing is switched off for this account — stop and tell the user.

### `restore_keyword`
- scope: write · params: `brand_id`*, `keyword_id`*
- Bring an archived keyword back into the brand's Keywords Database. ``brand_id`` comes from ``list_brands``. ``keyword_id`` is the ``id`` that ``archive_keyword`` returned — ``list_keywords`` never lists archived keywords. The keyword comes back ``active`` or ``hidden`` by the same volume/relevance rule as any other. Idempotent. Fix and retry — ``KEYWORD_NOT_FOUND``: no keyword with that id on this brand.

### `run_test_article`
- scope: write · params: `brand_id`*
- Write one test article from a random topic, to check the voice before a season. **Spends a full generation** (text and images) — confirm with the user first. ``brand_id`` comes from ``list_brands``. Needs a season in progress (see ``get_content_plan``). The article stays off the calendar and is never published. One at a time and at most three a day per brand. Returns ``test_article_id`` straight away (``202``); the article takes a few minutes — read it with ``get_article``. Fix and retry — ``NO_ACTIVE_PLAN``: no season exists yet; call ``start_content_workflow`` first. Transient — ``NO_TOPICS``: the season's topics are still being generated; wait a few minutes. ``TEST_ARTICLE_RUNNING``: the previous test article is still being written; wait for it. Do not retry — ``TEST_ARTICLE_DAILY_CAP``: today's limit is used up; it resets at 00:00 UTC. ``GENERATION_BLOCKED``: the brand's subscription is not live, so nothing can be generated; the user must renew it. ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `start_content_workflow`
- scope: write · params: `brand_id`*
- Start the content workflow: articles begin to be generated and published. **Spends generation budget** — confirm with the user first. ``brand_id`` comes from ``list_brands``; set the mix, steps, tone and schedule with ``update_content_settings`` before starting. With no season in progress it generates the plan's topics first (``status: started``, ``phase: generating_topics``); with one it queues the next articles (``topping_up``), or does nothing when enough are queued (``ok``). From then on the workflow approves topics a few days ahead of their dates and publishes on schedule. Idempotent — also resumes after ``stop_content_workflow``. ``status: blocked`` (not an error) means the content subscription is not active: approving topics and the test article are refused for the same reason (``GENERATION_BLOCKED``). Fix and retry — ``MIX_NOT_CONFIRMED``: starting would create a new season and the category mix is not confirmed yet; confirm it with ``update_content_settings(confirm_categories=True)`` or by sending ``category_mix``. (Not raised while a season is in progress or one built ahead is waiting: starting then resumes or promotes it.) ``TONE_NOT_IN_BRAND``: the chosen tone no longer belongs to the brand; pick another with ``update_content_settings``. Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `stop_content_workflow`
- scope: write · params: `brand_id`*
- Pause the content workflow for a brand; ``start_content_workflow`` resumes it. ``brand_id`` comes from ``list_brands``. Generation and publishing stop from the next scheduled run; articles already generating finish. Nothing is deleted. Stopping is also what lets ``update_content_settings`` switch steps. Returns the settings (``is_running`` is now ``false``). Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `suggest_keywords`
- scope: write · params: `brand_id`*, `sub_product_id`
- Start a Suggest run: Era discovers keywords from the brand's site and adds them. **Spends one of the brand's monthly Suggest runs** and runs for several minutes, so confirm with the user before calling and look at ``get_keyword_usage`` for what is left. ``brand_id`` comes from ``list_brands``. The run discovers keywords from the brand's site, competitors and topics (or, with ``sub_product_id`` from ``list_sub_products``, from that product alone), measures them and adds the relevant ones. Returns at once with a ``run_id`` and ``status: pending``; poll ``get_keyword_suggestion_run`` until it is ``completed`` or ``failed``. A start never answers ``failed``: a run that cannot be queued is a ``SUGGEST_QUEUE_FAILED`` error instead. Fix and retry — ``SUB_PRODUCT_NOT_FOUND``: use an id from ``list_sub_products``. ``SUB_PRODUCT_INACTIVE``: call ``activate_sub_product`` first. Transient — ``SUGGEST_IN_PROGRESS``: a run is already going for this brand; the message names its run id — poll it with ``get_keyword_suggestion_run``, then start another only if the user still wants it. ``SUGGEST_QUEUE_FAILED`` (503): the run could not be queued; it is marked failed and does not count against the monthly runs. Retry in a few minutes. Do not retry — ``QUOTA_EXHAUSTED``: the monthly runs are used up; the message says when they reset. ``NOTHING_TO_SUGGEST_FROM``: the brand has no website, competitors or topics to start from — tell the user. ``SUB_PRODUCTS_DISABLED``: sub-products are not switched on for this brand.

### `swap_prompts`
- scope: write · params: `add_contents`*, `brand_id`*, `prompt_type`, `remove_prompt_ids`*
- Atomically deactivate some prompts and add new ones in one transaction — the supported way to add prompts when the brand is already at its cap. All-or-nothing: every id in remove_prompt_ids must be an active prompt of this brand, otherwise the swap is rejected (422) and nothing changes.

### `test_publishing_destination`
- scope: write · params: `connection_id`*
- Test a publishing destination: ping it, and activate it if it answers. ``connection_id`` is the ``id`` from ``list_publishing_destinations`` (or ``create_publishing_destination``). A Custom site gets a signed ``ping`` event and must answer 2xx. On success the connection becomes ``active`` — this is how a new webhook goes live and how a disabled connection comes back. A failed ping is NOT an HTTP error: the call returns ``ok: false`` with the reason in ``error`` and the connection stays ``error``. Fix the site (is it deployed, does it hold the secret?) or the URL with ``update_publishing_destination``, then test again. Fix and retry — ``CONNECTION_NOT_FOUND``: use an id from ``list_publishing_destinations``. Do not retry — ``PUBLISHING_DISABLED``: publishing is switched off for this account. ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `update_brand_kit`
- scope: write · params: `about_brand`, `brand_id`*, `brand_point_of_view`, `ideal_customer_profile`
- Update the brand kit. Partial: only the fields you pass change. ``brand_id`` comes from ``list_brands``; read the current kit with ``get_brand_kit`` first. Content-plan brands only. ``about_brand`` and ``ideal_customer_profile`` take up to 2048 characters, ``brand_point_of_view`` up to 4096; an empty string clears a field. These go into every article's generation prompt, so write them as the brand would describe itself, not as instructions. Applies to articles written from now on. Returns the kit. Fix and retry — a 422 "Invalid arguments" means a field is over its length limit. Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `update_content_settings`
- scope: write · params: `brand_id`*, `category_mix`, `confirm_categories`, `publish_destination_ids`, `publish_hour_utc`, `steps`, `tone_of_voice_id`, `use_default_tone`
- Change a brand's content settings. Partial: only what you pass changes. ``brand_id`` comes from ``list_brands``; read the current state with ``get_content_settings`` first. Content-plan brands only. ``category_mix`` is all five counts (``keyword``, ``glossary``, ``versus``, ``top5``, ``howto``) and must sum to ``plan_size``; sending it also confirms it. ``confirm_categories=True`` confirms the current mix as it is — a plan cannot be generated before the mix is confirmed. ``steps`` switches pipeline steps on or off by name (``brand_kit``, ``keywords``, ``tone_of_voice``, ``humanize``, ``images``, ``videos``, ``video_metadata``, ``video_thumbnail``, ``publish_blog``, ``publish_youtube``, ``publish_medium``, ``publish_substack``); steps you leave out keep their state. ``tone_of_voice_id`` (from ``list_tones``) picks the tone articles are written in; ``use_default_tone=True`` reverts to the brand's default blog tone (do not pass both). ``publish_hour_utc`` (0-23) and ``publish_destination_ids`` (active destinations from ``list_publishing_destinations``; replaces the saved list) are the publishing schedule. ``publish_destination_ids=[]`` clears the list, but only while a YouTube, Medium or Substack lane is armed to publish at that hour — otherwise there would be nowhere to publish and it is refused with ``INVALID_DESTINATION``. **Saving the schedule can start publishing right away:** it turns blog publishing on exactly when destinations remain, and if the workflow is running the season in progress switches to publishing (``auto_publishing_started: true``) — confirm with the user before saving one. A destination must be ``active``: connect and test it first (``create_publishing_destination``, ``test_publishing_destination``). **A changed mix may regenerate the plan:** the un-started rest of the season in progress is re-planned (``regenerating_plan_id`` is set) and the next season built ahead is dropped and rebuilt (``scheduled_successor_reset``). That happens at most 3 times a day per brand; beyond that the mix applies from the next season and ``regeneration_skipped`` says why (``in_flight``: a generation is already running, ``daily_cap``, or ``not_in_progress``: the season exists but is neither active nor publishing, e.g. finished or failed) — it is not an error. With no season at all there is nothing to re-plan and ``regeneration_skipped`` is ``null``. Returns the settings after the update. Fix and retry — ``MIX_INVALID``: the mix does not sum to ``plan_size``. ``STEP_REQUIRED``: a required step cannot be switched off. ``TONE_NOT_IN_BRAND``: that tone is not this brand's; use an id from ``list_tones``. ``INVALID_DESTINATION``: an id is unknown, not this brand's, not active, or a pull-mode (API) site; or ``[]`` was sent while no YouTube, Medium or Substack lane is armed to publish; use ``list_publishing_destinations``. ``PUBLISH_HOUR_REQUIRED``: destinations were sent but no hour is saved; send ``publish_hour_utc`` too. ``PUBLISH_STEP_CONFLICT``: ``steps.publish_blog`` contradicts the destinations; leave it out. ``WORKFLOW_RUNNING``: steps can only be switched while the workflow is stopped; call ``stop_content_workflow``, change them, then ``start_content_workflow`` again (the mix, tone and schedule can change while it runs). Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `update_plan_topic`
- scope: write · params: `article_id`*, `plan_id`*, `title`*
- Rename a topic before it is written. ``plan_id`` comes from ``get_content_plan``; ``article_id`` is a topic's ``id`` from ``list_plan_topics(status="topic")``. Changes only the ``title`` (1-500 characters) of a topic still awaiting approval. A written article is edited with ``propose_article_edit`` instead. Fix and retry — ``PLAN_NOT_FOUND`` / ``ARTICLE_NOT_FOUND``: use the ids from ``get_content_plan`` / ``list_plan_topics``. Do not retry — ``NOT_A_TOPIC``: the article was already approved; use ``propose_article_edit`` once it is written. ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `update_prompt`
- scope: write · params: `brand_id`*, `content`, `is_active`, `prompt_id`*
- Edit a prompt's text and/or activate/deactivate it. Re-activating counts against the brand's active-prompt cap.

### `update_publishing_destination`
- scope: write · params: `connection_id`*, `name`, `site_base_url`, `status`, `webhook_url`
- Edit a publishing destination: rename it, change its URLs, or disable it. ``connection_id`` is the ``id`` from ``list_publishing_destinations``. Partial: only the fields you pass change. ``name`` renames it; ``webhook_url`` (Custom site, webhook delivery) and ``site_base_url`` (Custom site) are edited here; ``site_base_url=""`` clears it. ``status="disabled"`` stops publishing to it. **Nothing here pings or activates:** a new ``webhook_url`` leaves the connection ``error`` ("Awaiting verification") until ``test_publishing_destination`` passes, and that test is also how a disabled connection is re-enabled. Secrets are not editable and the delivery mode is fixed at creation. Returns the connection. Fix and retry — ``INVALID_WEBHOOK_URL``: not an absolute https URL. ``CONNECTION_NOT_FOUND``: use an id from ``list_publishing_destinations``. Do not retry — ``DELIVERY_IMMUTABLE``: an ``api`` site has no webhook and a connection's delivery cannot change; create a new destination. ``NOT_A_CUSTOM_SITE``: only a Custom site has these URLs (renaming and disabling work for any destination). ``PUBLISHING_DISABLED``: publishing is switched off for this account. ``PLAN_REQUIRED``: the brand is not on a Content plan.

### `update_sub_product`
- scope: write · params: `brand_id`*, `description`, `display_order`, `name`, `sub_product_id`*, `url`
- Edit a sub-product: rename it, change its page or description, or reorder it. ``brand_id`` comes from ``list_brands``; ``sub_product_id`` from ``list_sub_products``. Partial: only the fields you pass change (send at least one). Changing the ``name`` or ``description`` replaces the sub-product's monitoring prompts with a fresh batch (the old prompts' history stays); a new ``url`` re-fetches the page; a ``url`` or ``display_order`` change alone leaves the prompts alone. ``description=""`` clears the description. Returns the updated sub-product. Fix and retry — ``DUPLICATE_URL``: another sub-product of the brand already has that URL. ``SUB_PRODUCT_NOT_FOUND``: use an id from ``list_sub_products``. Transient — ``PROMPT_REGEN_QUEUE_FAILED`` (503): the edit IS saved, but the fresh prompts were not queued. Do not repeat the request straight away — within the hour it does nothing. Era queues the missing prompts itself (its nightly check; the same request repeated after an hour does it too); look at ``prompt_count`` in ``list_sub_products`` later. Do not retry — ``SUB_PRODUCTS_DISABLED``: sub-products are not switched on for this brand.

### `update_tone`
- scope: write · params: `description`, `is_default`, `master_prompt`, `name`, `platform`, `tone_id`*
- Edit a tone of voice. Partial: only the fields you pass change. ``tone_id`` comes from ``list_tones``. Era's own (system) tones can be edited too. ``name``, ``description``, ``platform`` (``blog``, ``medium``, ``substack``, ``reddit``, ``x``, ``linkedin``) and ``master_prompt`` (up to 8000 characters) are as in ``create_tone``; ``description=""`` clears the description and ``platform=""`` makes the tone apply to any platform; ``is_default=True`` makes it the default for its platform. Articles already written keep the voice they were written in; the change applies to new ones. Returns the tone. Fix and retry — ``TONE_NOT_FOUND``: use an id from ``list_tones``. Do not retry — ``PLAN_REQUIRED``: the brand is not on a Content plan.


## Prompts shipped by the server

- `era_competitor_radar` — Highlight competitors whose share of voice moved by more than a threshold (percentage points) — the biggest gainers and losers.
- `era_content_setup` — Walk through setting up a brand's content engine: brand kit, tone, category mix, publishing destination, then starting the workflow and approving topics.
- `era_engine_scorecard` — Per-engine breakdown of how the brand performs across each AI answer engine (ChatGPT, Perplexity, Gemini, ...).
- `era_onboard_sub_product` — Add a product page to a brand as a sub-product, load its keywords and check it is wired up (prompts, keywords, content plan).
- `era_source_authority` — Audit which sources AI engines cite about the brand and where the gaps are versus competitors.
- `era_weekly_pulse` — A week-over-week AEO digest for a brand: visibility, share of voice and sentiment changes, competitor moves and notable new cited sources.
