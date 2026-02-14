# CSS Selectors Guide

## Overview

Custom CSS selectors allow you to precisely target specific content on web pages. Use the `--selectors` flag to provide a JSON file with your selector definitions.

## Selector Configuration

### Basic Structure

```json
{
  "title": "h1, .title, [role='heading']",
  "content": "article p, .content, main",
  "price": ".price, [data-price]",
  "date": "[data-date], .date",
  "author": ".author, .byline",
  "image": "img.hero, .featured-image",
  "metadata": ".meta, .article-info"
}
```

### Using Custom Selectors

```bash
python3 scripts/extract.py --urls urls.txt --selectors custom.json
```

## Common Patterns

### Article Content

```json
{
  "title": "h1.article-title, .entry-title, .post-title",
  "content": "article .entry-content, .post-content, .article-body",
  "author": ".author-name, .byline, .post-author",
  "date": ".post-date, .entry-date, time[datetime]",
  "tags": ".tags a, .categories a, .post-tags"
}
```

### E-commerce Products

```json
{
  "title": ".product-title, h1.product-name",
  "price": ".price, [data-price], .product-price",
  "description": ".product-description, .product-details",
  "image": ".product-image img, .gallery img:first-of-type",
  "rating": ".rating, .stars, [data-rating]",
  "availability": ".stock-status, .availability"
}
```

### News Articles

```json
{
  "title": "h1.headline, .article-headline",
  "content": ".article-body, .story-content, .news-text",
  "author": ".author, .reporter",
  "date": "time.published, .publish-date",
  "category": ".category, .section"
}
```

### Blog Posts

```json
{
  "title": ".post-title, h1.entry-title",
  "content": ".post-content, .entry-content",
  "author": ".vcard, .post-author",
  "date": ".post-date, time[datetime]",
  "comments": ".comments-count, .comment-count"
}
```

## Advanced Selectors

### Attribute Selectors

Target elements with specific attributes:

```json
{
  "title": "[data-testid='article-title']",
  "content": "[data-component='article-body']",
  "price": "[data-currency='USD']"
}
```

### Pseudo-classes

Select specific elements:

```json
{
  "first_paragraph": "article p:first-child",
  "last_paragraph": "article p:last-child",
  "even_rows": "table tr:nth-child(even)",
  "featured_image": ".gallery img:nth-of-type(1)"
}
```

### Structural Selectors

Based on DOM structure:

```json
{
  "main_content": "main > article",
  "sidebar": "aside",
  "header": "header, .header",
  "footer": "footer, .footer"
}
```

### Text Content Matching

Match by text content:

```json
{
  "buy_button": "button:contains('Buy Now'), .btn-purchase",
  "read_more": "a:contains('Read More')"
}
```

## Framework-Specific Selectors

### React Applications

```json
{
  "title": "[data-reactid] h1, [data-testid*='title']",
  "content": "[data-component*='article'], [data-testid*='content']"
}
```

### Vue Applications

```json
{
  "title": "[v-cloak] h1, [data-v-*] h1",
  "content": "[data-component='content']"
}
```

### Angular Applications

```json
{
  "title": "app-root h1, [ng-reflect-router-link]",
  "content": "article, [ng-content]"
}
```

## Testing Selectors

### Method 1: Browser DevTools

1. Open the target page in Chrome/Firefox
2. Press F12 to open DevTools
3. Use the Elements tab to inspect
4. Test selectors in the Console:

```javascript
document.querySelectorAll('.article-content')
document.querySelector('h1.article-title')
```

### Method 2: Python Script

Create a test script:

```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Test your selectors
title = soup.select_one('h1.article-title')
content = soup.select('article p')

print(f"Title: {title.text if title else 'Not found'}")
print(f"Paragraphs: {len(content)}")
```

### Method 3: Online Tools

- [CSS Selector Tester](https://css-selector-tester.com/)
- [SelectorGadget](https://selectorgadget.com/) - Chrome extension

## Fallback Patterns

### Hierarchical Fallbacks

Define multiple selectors in priority order:

```json
{
  "title": [
    "h1.article-title",
    ".entry-title",
    "h1",
    "[role='heading']"
  ]
}
```

The tool will try each selector until it finds a match.

### Domain-Specific Selectors

Different selectors for different domains:

```json
{
  "example.com": {
    "title": ".custom-title",
    "content": ".custom-content"
  },
  "another-site.com": {
    "title": "h1",
    "content": "article"
  },
  "default": {
    "title": "h1, .title",
    "content": "article, .content"
  }
}
```

## Common Pitfalls

### Dynamic Classes

Avoid selecting by auto-generated classes:

```json
// ❌ Bad
{
  "content": ".css-1a2b3c4d"
}

// ✅ Good
{
  "content": ".content, [data-component='content']"
}
```

### Overly Specific

Too specific selectors break easily:

```json
// ❌ Bad
{
  "title": "div.container > div.main > div.article > h1"
}

// ✅ Good
{
  "title": ".article h1, [data-component='article'] h1"
}
```

### Missing Fallbacks

Always provide alternatives:

```json
// ❌ Bad
{
  "title": ".specific-title-only"
}

// ✅ Good
{
  "title": ".specific-title-only, h1, [role='heading']"
}
```

## Best Practices

### 1. Use Semantic Selectors

Prefer semantic attributes:

```json
{
  "title": "h1, [role='heading'], [aria-label*='title']"
}
```

### 2. Target Data Attributes

Data attributes are stable:

```json
{
  "title": "[data-testid='article-title']",
  "price": "[data-currency] [data-price]"
}
```

### 3. Combine Selectors

Use comma-separated alternatives:

```json
{
  "content": "article p, .entry-content p, .post-content p"
}
```

### 4. Keep Selectors Simple

Complex selectors are brittle:

```json
// ❌ Too complex
{
  "content": "div:nth-child(2) > div:nth-child(1) > article > div > p"
}

// ✅ Simple
{
  "content": "article p"
}
```

## Examples by Use Case

### Extracting Social Media Posts

```json
{
  "post": "div[data-testid='tweet'], .post",
  "author": ".author, [data-author]",
  "content": ".tweet-text, .post-content",
  "timestamp": "time, [data-time]",
  "likes": ".likes, [data-likes]",
  "shares": ".shares, [data-shares]"
}
```

### Extracting Documentation

```json
{
  "title": "h1, .docs-title",
  "content": ".markdown-body, .documentation, article",
  "code_blocks": "pre code, .code-block",
  "headings": "h2, h3, h4",
  "links": ".markdown-body a"
}
```

### Extracting Job Listings

```json
{
  "title": ".job-title, h2.job-title",
  "company": ".company-name, .employer",
  "location": ".location, .job-location",
  "description": ".job-description, .description",
  "salary": ".salary, [data-salary]",
  "requirements": ".requirements, ul.requirements"
}
```

## Performance Tips

### Efficient Selectors

- Use ID selectors where available: `#article-title`
- Use class selectors: `.article-content`
- Avoid complex pseudo-selectors
- Minimize descendant combinator depth

### Selector Caching

The tool caches selector results, so define reusable selectors:

```json
{
  "article": "article, [data-component='article']",
  "title": "h1, .title",
  "content": ".article-content, .post-content p"
}
```

## Troubleshooting

### Selector Not Matching

1. Verify page has loaded (use `--mode browser`)
2. Check for dynamic content loading
3. Test selector in browser DevTools
4. Provide fallback selectors

### Too Much/Too Little Content

1. Make selector more specific if too much
2. Make selector more general if too little
3. Use attribute selectors for precision

### Selectors Break on Updates

1. Use semantic/attribute selectors
2. Provide multiple fallbacks
3. Avoid auto-generated classes

## Resources

- [MDN CSS Selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [CSS Tricks Selector Reference](https://css-tricks.com/almanac/selectors/)
- [W3C CSS Selectors Level 3](https://www.w3.org/TR/selectors-3/)
