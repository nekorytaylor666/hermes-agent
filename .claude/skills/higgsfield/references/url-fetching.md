# URL Fetching

## Tool Cascade

Use `fetchcli fetch` as the default. Fall back to `searchcli` for JS-heavy pages, then `WebFetch` as last resort.

### fetchcli fetch (default)

```bash
fetchcli fetch --url "<URL>"
```

For structured data extraction (product info, prices, images):
```bash
fetchcli fetch --url "<URL>" --formats json --prompt "extract product name, price, images"
```
Runs LLM extraction server-side, returns clean JSON (~2-3KB).

Pass `--schema '{...}'` for strict typed output.

**CRITICAL: Do NOT add `markdown` to formats when fetching marketplace/product pages** — Amazon, AliExpress, Shopify pages produce 100-200KB of markdown that truncates the output including the extracted JSON. Use `--formats json` alone for product pages.

Use `--formats markdown` only for articles/blogs where you need the full text.

Filtering: `--include-tags "img,h1,p"` (whitelist) or `--exclude-tags "nav,footer,script"` (blacklist).

### searchcli read (JS fallback)

If `fetchcli` returns empty/incomplete (JS-heavy SPAs):
```bash
searchcli read --url "<URL>" --with-alt
```
Renders JS, supports `--wait-for-selector "CSS_SELECTOR"`, captions images.

### WebFetch (last resort)

Only after both `fetchcli` and `searchcli` fail.

## Fetch Once Per URL

Save the full response to a local file (e.g. `/tmp/<slug>-fetch.json`) and reference it for every follow-up extraction. Never re-fetch the same URL for a different slice. One URL, one fetch, multiple local reads.

Exception: user explicitly asks to re-fetch, or initial fetch was incomplete and you're escalating renderer.
