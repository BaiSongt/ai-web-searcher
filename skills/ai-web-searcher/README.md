# AI Web Searcher

Multi-threaded AI-powered web content extraction tool with smart search capabilities.

## Features

- ✅ Multi-threaded concurrent processing
- ✅ AI-driven content analysis
- ✅ Support for dynamic websites (JS/SPA)
- ✅ Multiple output formats (JSON/Markdown/CSV)
- ✅ Rate limiting and retry mechanisms
- ✅ Custom CSS selectors
- ✅ **Smart Search** - Pre-configured AI news sources with keyword matching
- ✅ **Categorized Search** - 6 search categories for quick navigation
- ✅ **Relevance Scoring** - Intelligent ranking of results

## Quick Start

### Extract Content

#### Single URL
```bash
python3 scripts/extract.py --url "https://example.com" --format json
```

#### Multiple URLs
```bash
python3 scripts/extract.py --urls urls.txt --concurrency 5 --format json
```

### Smart Search

#### List Available Sources
```bash
python3 scripts/smart_search.py --list-sources
```

#### Search by Keywords
```bash
python3 scripts/smart_search.py "GPT model release" --max-results 5
```

#### Search by Category
```bash
# Model releases
python3 scripts/smart_search.py --category model_releases

# Research papers
python3 scripts/smart_search.py --category research

# Industry news
python3 scripts/smart_search.py --category industry
```

## Documentation

- [SKILL.md](SKILL.md) - Main documentation
- [references/CONCURRENCY.md](references/CONCURRENCY.md) - Concurrency patterns
- [references/SELECTORS.md](references/SELECTORS.md) - CSS selector guide
- [references/OUTPUT_FORMATS.md](references/OUTPUT_FORMATS.md) - Output formats
- [references/SMART_SEARCH.md](references/SMART_SEARCH.md) - Smart search guide
- [TEST_REPORT.md](TEST_REPORT.md) - Test results and validation

## Pre-configured Sources

Smart Search includes 10+ AI news sources:
- OpenAI News
- Google AI Blog
- DeepMind Blog
- Anthropic News
- TechCrunch AI
- The Verge AI
- MIT Technology Review
- VentureBeat AI
- arXiv CS.AI
- Artificial Intelligence News

## Search Categories

- `model_releases` - New model launches and updates
- `research` - Academic papers and breakthroughs
- `products` - Product updates and features
- `industry` - Funding, acquisitions, startups
- `safety` - AI safety and regulation
- `applications` - Enterprise and use cases

## Requirements

- Python 3.7+
- OpenClaw CLI (for browser integration)

## License

MIT
