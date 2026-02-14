---
name: ai-web-searcher
description: AI-powered web content extraction tool with multi-threaded concurrent support. Extract structured content from web pages using browser rendering and AI analysis. Use when users need to: (1) Scrape multiple websites concurrently, (2) Extract key information from dynamic JavaScript pages, (3) Filter out ads and irrelevant content, (4) Get structured JSON/Markdown output from web pages, (5) Monitor multiple sources simultaneously.
---

# AI Web Searcher

Lightweight AI-driven web content extraction tool with concurrent multi-threading support. Uses browser automation to render pages and AI to extract meaningful content - not traditional crawling.

## Quick Start

### Single URL Extraction

```bash
# Extract content from a single page
python3 scripts/extract.py --url "https://example.com" --format json
```

### Concurrent Multi-URL Extraction

```bash
# Extract from multiple URLs concurrently
python3 scripts/extract.py --urls urls.txt --format json --concurrency 5
```

## Core Features

### 1. Multi-Threaded Concurrent Processing

Control concurrency with the `--concurrency` flag:

- **Default**: 3 concurrent browser instances
- **Recommended**: 5-10 for most use cases
- **Maximum**: Depends on your system resources

```bash
python3 scripts/extract.py --urls urls.txt --concurrency 10
```

### 2. Content Extraction Modes

Choose extraction strategy based on page type:

| Mode | Description | Use Case |
|------|-------------|----------|
| `light` | web_fetch only (fast, static HTML) | Simple blogs, news sites |
| `browser` | Full browser rendering (JS/SPA support) | React/Vue apps, dynamic content |
| `deep` | Crawlee-based deep scraping | Complex sites like YouTube |

```bash
# Light mode (fastest)
python3 scripts/extract.py --urls urls.txt --mode light

# Browser mode (default)
python3 scripts/extract.py --urls urls.txt --mode browser

# Deep mode (most thorough)
python3 scripts/extract.py --urls urls.txt --mode deep
```

### 3. AI Content Analysis

AI automatically:
- Identifies key content (titles, paragraphs, lists)
- Filters out ads, navigation, footers
- Extracts structured data (prices, dates, metadata)
- Summarizes content when requested

```bash
# Enable AI summarization
python3 scripts/extract.py --urls urls.txt --summarize --summary-length 200
```

### 4. Output Formats

Multiple output options:

```bash
# JSON output (default)
python3 scripts/extract.py --urls urls.txt --output results.json

# Markdown output
python3 scripts/extract.py --urls urls.txt --format markdown --output results.md

# CSV output (tabular data)
python3 scripts/extract.py --urls urls.txt --format csv --output results.csv
```

## Advanced Features

### Custom Selectors

For specific content extraction, define custom selectors:

```json
{
  "title": "h1, .title, [role='heading']",
  "content": "article p, .content, main",
  "price": ".price, [data-price]",
  "date": "[data-date], .date"
}
```

```bash
python3 scripts/extract.py --urls urls.txt --selectors custom_selectors.json
```

### Rate Limiting

Avoid getting blocked with rate limiting:

```bash
# Add delay between requests (in seconds)
python3 scripts/extract.py --urls urls.txt --delay 2

# Random delay between 1-3 seconds
python3 scripts/extract.py --urls urls.txt --delay 1-3
```

### Retry Mechanism

Automatic retry on failures:

```bash
# Retry failed URLs up to 3 times
python3 scripts/extract.py --urls urls.txt --retries 3
```

### Authentication

Support for authenticated pages:

```bash
# Basic auth
python3 scripts/extract.py --urls urls.txt --auth user:pass

# Cookie-based auth
python3 scripts/extract.py --urls urls.txt --cookies cookies.txt
```

## Input Formats

### URLs from File

Create `urls.txt` (one URL per line):

```
https://example.com/page1
https://example.com/page2
https://another-site.com
```

```bash
python3 scripts/extract.py --urls urls.txt
```

### URLs from JSON

Create `urls.json`:

```json
{
  "urls": [
    {"url": "https://example.com", "tags": ["news", "tech"]},
    {"url": "https://another-site.com", "tags": ["blog"]},
    {"url": "https://dynamic-site.com", "mode": "browser"}
  ]
}
```

```bash
python3 scripts/extract.py --urls urls.json
```

### URLs from CLI

```bash
python3 scripts/extract.py --url "https://example.com" --url "https://another.com"
```

## Output Structure

### JSON Output

```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "content": "Main content...",
  "summary": "AI-generated summary",
  "metadata": {
    "author": "John Doe",
    "date": "2026-02-14",
    "tags": ["tech", "news"]
  },
  "extraction_time": "2026-02-14T10:00:00Z",
  "word_count": 1234,
  "status": "success"
}
```

### Markdown Output

```markdown
# Page Title

**URL**: https://example.com
**Author**: John Doe
**Date**: 2026-02-14

## Summary

AI-generated summary here...

## Content

Main content extracted from the page...

---

*Extracted at: 2026-02-14T10:00:00Z | Words: 1234*
```

## Best Practices

### Choosing the Right Mode

- **Static pages (news, blogs)**: Use `--mode light` for speed
- **Dynamic apps (SPA, React/Vue)**: Use `--mode browser`
- **Complex sites (YouTube, social media)**: Use `--mode deep`

### Concurrency Settings

```bash
# Conservative (low bandwidth)
python3 scripts/extract.py --urls urls.txt --concurrency 3

# Balanced (default)
python3 scripts/extract.py --urls urls.txt --concurrency 5

# Aggressive (high bandwidth, powerful machine)
python3 scripts/extract.py --urls urls.txt --concurrency 10
```

### Rate Limiting

Always add delays when extracting from:
- The same domain multiple times
- Sites with anti-bot protection
- Unknown or untrusted sources

```bash
# Safe default for most sites
python3 scripts/extract.py --urls urls.txt --delay 1-3
```

### Error Handling

```bash
# Continue on errors, log failures
python3 scripts/extract.py --urls urls.txt --continue-on-error --log errors.log
```

## Troubleshooting

### Common Issues

**Issue**: Browser not rendering correctly
```
Solution: Use --mode deep for complex sites
```

**Issue**: Getting rate-limited or blocked
```
Solution: Add --delay 2-5 and --retries 3
```

**Issue**: Missing content (ads filtered incorrectly)
```
Solution: Use custom selectors to target specific elements
```

**Issue**: Slow performance
```
Solution: Reduce --concurrency or use --mode light for static pages
```

## Integration with OpenClaw

This skill works seamlessly with OpenClaw's built-in tools:

- **browser tool**: Use for interactive page navigation
- **web_fetch**: Used internally in light mode
- **AI models**: Content analysis and summarization

Example workflow:

1. Use `agent-browser` for initial exploration
2. Use `ai-web-searcher` for batch extraction
3. Use AI to analyze and synthesize results

## References

For advanced configurations and patterns, see:

- [CONCURRENCY.md](references/CONCURRENCY.md) - Detailed concurrency patterns
- [SELECTORS.md](references/SELECTORS.md) - CSS selector examples
- [OUTPUT_FORMATS.md](references/OUTPUT_FORMATS.md) - Custom output templates
