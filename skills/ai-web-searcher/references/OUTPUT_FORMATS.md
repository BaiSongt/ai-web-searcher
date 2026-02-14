# Output Formats Guide

## Overview

AI Web Searcher supports multiple output formats for different use cases:

- **JSON** - Structured data for programmatic use
- **Markdown** - Human-readable documents
- **CSV** - Tabular data for spreadsheets

## JSON Output

### Structure

```json
{
  "url": "https://example.com/page",
  "title": "Page Title",
  "content": "Extracted content...",
  "summary": "AI-generated summary...",
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

### Use Cases

- **API Integration**: Feed results into other systems
- **Data Analysis**: Process with Python, R, or other tools
- **Database Storage**: Import directly into databases
- **Machine Learning**: Use as training data

### Example Usage

```bash
python3 scripts/extract.py --urls urls.txt --format json --output results.json
```

### Processing with Python

```python
import json

with open('results.json', 'r') as f:
    results = json.load(f)

for result in results:
    if result['status'] == 'success':
        print(f"{result['title']}: {result['word_count']} words")
```

### Processing with jq

```bash
# Extract all titles
jq '.[].title' results.json

# Count successful extractions
jq '[.[] | select(.status == "success")] | length' results.json

# Extract URLs with word counts
jq '.[] | {url, word_count}' results.json
```

## Markdown Output

### Structure

```markdown
# Page Title

**URL**: https://example.com/page
**Author**: John Doe
**Date**: 2026-02-14

## Summary

AI-generated summary here...

## Content

Main content extracted from the page...

---

*Extracted at: 2026-02-14T10:00:00Z | Words: 1234*
```

### Use Cases

- **Documentation**: Create human-readable reports
- **Blogging**: Convert web content to blog posts
- **Knowledge Base**: Build searchable documentation
- **Review**: Quick review of extracted content

### Example Usage

```bash
python3 scripts/extract.py --urls urls.txt --format markdown --output results.md
```

### Customizing Output

The Markdown output can be customized by modifying the script:

```python
# In save_results() function
f.write(f"## Custom Field\n{result.get('custom_field', '')}\n\n")
```

### Generating Tables

For tabular data, use Markdown tables:

```markdown
| URL | Title | Words | Date |
|-----|-------|-------|------|
| https://example.com/page1 | Page 1 | 1234 | 2026-02-14 |
| https://example.com/page2 | Page 2 | 567 | 2026-02-14 |
```

## CSV Output

### Structure

```csv
url,title,summary,word_count,extraction_time,extraction_mode,status
https://example.com/page1,Page 1,Summary text...,1234,2026-02-14T10:00:00Z,browser,success
https://example.com/page2,Page 2,Another summary...,567,2026-02-14T10:00:00Z,browser,success
```

### Use Cases

- **Spreadsheet Analysis**: Open in Excel, Google Sheets
- **Data Visualization**: Import into Tableau, Power BI
- **Database Import**: Use COPY command for PostgreSQL
- **Quick Review**: Human-readable tabular format

### Example Usage

```bash
python3 scripts/extract.py --urls urls.txt --format csv --output results.csv
```

### Processing with Python

```python
import csv

with open('results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['title']}: {row['word_count']} words")
```

### Processing with awk

```bash
# Extract titles
awk -F',' 'NR>1 {print $2}' results.csv

# Count words
awk -F',' 'NR>1 {sum += $4} END {print "Total words:", sum}' results.csv
```

## Custom Output Formats

### Adding a New Format

To add a custom output format, modify the `save_results()` function in `scripts/extract.py`:

```python
elif format == 'custom':
    with open(output_path, 'w', encoding='utf-8') as f:
        for result in results:
            # Your custom formatting logic here
            f.write(f"Custom: {result.get('title', '')}\n")
```

### Template-Based Output

Use Jinja2 templates for complex formats:

```python
from jinja2 import Template

template_str = """
# {{ result.title }}

URL: {{ result.url }}
Words: {{ result.word_count }}

{{ result.content }}
"""

template = Template(template_str)

# In save_results()
for result in results:
    output = template.render(result=result)
    f.write(output)
```

## Output Filtering

### Filter by Status

```python
# Only successful results
successful = [r for r in results if r.get('status') == 'success']
save_results(successful, 'success_only.json', 'json')
```

### Filter by Word Count

```python
# Only long articles
long_articles = [r for r in results if r.get('word_count', 0) > 1000]
save_results(long_articles, 'long_articles.json', 'json')
```

### Filter by URL Pattern

```python
import re

# Only specific domain
pattern = re.compile(r'https://example\.com/.*')
filtered = [r for r in results if pattern.match(r.get('url', ''))]
save_results(filtered, 'example_com.json', 'json')
```

## Output Aggregation

### Summarize Across Results

```python
# Calculate statistics
total_words = sum(r.get('word_count', 0) for r in results)
successful = sum(1 for r in results if r.get('status') == 'success')
average_words = total_words / successful if successful > 0 else 0

summary = {
    "total_urls": len(results),
    "successful": successful,
    "failed": len(results) - successful,
    "total_words": total_words,
    "average_words": round(average_words, 2)
}

with open('summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
```

### Merge Content

```python
# Merge all content into single file
all_content = "\n\n".join(
    r.get('content', '') for r in results
    if r.get('status') == 'success'
)

with open('merged_content.txt', 'w', encoding='utf-8') as f:
    f.write(all_content)
```

### Create Index

```python
# Create index of all extracted pages
index = []
for result in results:
    if result.get('status') == 'success':
        index.append({
            "title": result.get('title', ''),
            "url": result.get('url', ''),
            "word_count": result.get('word_count', 0),
            "summary": result.get('summary', '')[:200]
        })

with open('index.json', 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=2, ensure_ascii=False)
```

## Output Compression

### Compress JSON Output

```bash
# Gzip compress
gzip results.json
# Creates results.json.gz

# Extract
gunzip results.json.gz
```

```python
# Python compression
import gzip
import json

with open('results.json.gz', 'wb') as f:
    f.write(json.dumps(results).encode('utf-8'))
```

### Compress CSV Output

```bash
# Gzip compress
gzip results.csv

# Extract
gunzip results.csv.gz
```

## Output Streaming

### Stream to File

For large datasets, stream output instead of loading everything into memory:

```python
import json

def stream_results(results, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('[\n')
        for i, result in enumerate(results):
            if i > 0:
                f.write(',\n')
            json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n]')
```

### Stream Multiple Files

Split results into multiple files:

```python
import json
from math import ceil

chunk_size = 100
total_chunks = ceil(len(results) / chunk_size)

for chunk in range(total_chunks):
    start = chunk * chunk_size
    end = start + chunk_size
    chunk_results = results[start:end]

    with open(f'results_chunk_{chunk}.json', 'w') as f:
        json.dump(chunk_results, f, indent=2, ensure_ascii=False)
```

## Output Validation

### Validate JSON Schema

```python
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "word_count": {"type": "number"},
        "status": {"type": "string"}
    },
    "required": ["url", "status"]
}

for result in results:
    validate(instance=result, schema=schema)
```

### Check Data Quality

```python
# Check for missing fields
missing = []
for i, result in enumerate(results):
    if not result.get('title'):
        missing.append(f"Result {i}: Missing title")

if missing:
    print("Data quality issues:")
    for issue in missing:
        print(f"  - {issue}")
```

## Output Transformation

### Convert JSON to Markdown

```python
import json
import markdownify

with open('results.json', 'r') as f:
    results = json.load(f)

with open('results.md', 'w') as f:
    for result in results:
        if result.get('status') == 'success':
            f.write(f"# {result['title']}\n\n")
            f.write(f"**URL**: {result['url']}\n\n")
            f.write(result['content'])
            f.write("\n\n---\n\n")
```

### Convert JSON to CSV

```python
import json
import csv

with open('results.json', 'r') as f:
    results = json.load(f)

with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['url', 'title', 'word_count'])
    writer.writeheader()

    for result in results:
        if result.get('status') == 'success':
            writer.writerow({
                'url': result['url'],
                'title': result['title'],
                'word_count': result['word_count']
            })
```

## Best Practices

### Choose the Right Format

| Use Case | Recommended Format |
|----------|-------------------|
| API integration | JSON |
| Human review | Markdown |
| Spreadsheet analysis | CSV |
| Database import | JSON or CSV |
| Machine learning | JSON |

### Include Metadata

Always include extraction metadata:
- `extraction_time` - When data was extracted
- `extraction_mode` - How it was extracted
- `word_count` - Size of content
- `status` - Success or failure

### Validate Output

Validate output before using:
```python
assert len(results) > 0, "No results extracted"
assert all('url' in r for r in results), "Missing URLs"
```

### Backup Original Data

Keep original HTML for reference:
```python
# Store original HTML for debugging
result['raw_html'] = html_content
```

## Resources

- [JSON Specification](https://www.json.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [CSV RFC 4180](https://tools.ietf.org/html/rfc4180)
- [jsonschema Validation](https://python-jsonschema.readthedocs.io/)
