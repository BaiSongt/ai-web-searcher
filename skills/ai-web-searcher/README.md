# AI Web Searcher

Multi-threaded AI-powered web content extraction tool.

## Features

- ✅ Multi-threaded concurrent processing
- ✅ AI-driven content analysis
- ✅ Support for dynamic websites (JS/SPA)
- ✅ Multiple output formats (JSON/Markdown/CSV)
- ✅ Rate limiting and retry mechanisms
- ✅ Custom CSS selectors

## Quick Start

### Single URL
```bash
python3 scripts/extract.py --url "https://example.com" --format json
```

### Multiple URLs
```bash
python3 scripts/extract.py --urls urls.txt --concurrency 5 --format json
```

## Documentation

- [SKILL.md](SKILL.md) - Main documentation
- [references/CONCURRENCY.md](references/CONCURRENCY.md) - Concurrency patterns
- [references/SELECTORS.md](references/SELECTORS.md) - CSS selector guide
- [references/OUTPUT_FORMATS.md](references/OUTPUT_FORMATS.md) - Output formats

## Requirements

- Python 3.7+
- OpenClaw CLI (for browser integration)

## License

MIT
