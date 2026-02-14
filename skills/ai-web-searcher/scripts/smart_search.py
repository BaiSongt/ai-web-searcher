#!/usr/bin/env python3
"""
Smart Search - Search AI news from known sources first
"""

import argparse
import json
import os
import sys
import subprocess
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add workspace to path
workspace = os.path.expanduser('~/.openclaw/workspace')
if workspace not in sys.path:
    sys.path.insert(0, workspace)


class SmartSearcher:
    """Smart search that prioritizes known sources"""

    def __init__(self, sources_file: str):
        self.sources_file = sources_file
        self.sources = self.load_sources()

    def load_sources(self) -> Dict[str, Any]:
        """Load search sources configuration"""

        if not os.path.exists(self.sources_file):
            raise FileNotFoundError(f"Sources file not found: {self.sources_file}")

        with open(self.sources_file, 'r') as f:
            return json.load(f)

    def search(
        self,
        query: str,
        max_results: int = 10,
        category: Optional[str] = None,
        mode: str = "browser"
    ) -> List[Dict[str, Any]]:
        """Search from known sources"""

        query_lower = query.lower()
        results = []

        # If category specified, use category-specific sources
        if category and category in self.sources['search_categories']:
            category_config = self.sources['search_categories'][category]
            sources = self.filter_sources_by_keywords(
                category_config['keywords'],
                category_config.get('sources', [])
            )
        else:
            # Search all sources, prioritize by keyword matches
            sources = self.score_sources(query_lower)

        # Extract content from top sources
        for source in sources[:max_results]:
            result = self.extract_from_source(source, query, mode)
            if result:
                results.append(result)

        return results

    def filter_sources_by_keywords(
        self,
        keywords: List[str],
        source_names: List[str]
    ) -> List[Dict[str, Any]]:
        """Filter sources by keywords and names"""

        filtered = []
        for source in self.sources['ai_news_sources']:
            if source['name'].lower() in [s.lower() for s in source_names]:
                filtered.append(source)
        return filtered

    def score_sources(self, query: str) -> List[Dict[str, Any]]:
        """Score sources based on keyword relevance"""

        scored = []

        for source in self.sources['ai_news_sources']:
            score = 0

            # Score by direct keyword matches
            query_words = query.split()
            for word in query_words:
                for keyword in source['keywords']:
                    if word.lower() in keyword.lower():
                        score += 1

            # Score by keyword mappings
            for key, synonyms in self.sources['keyword_mappings'].items():
                if any(word in query.lower() for word in synonyms):
                    for keyword in source['keywords']:
                        if any(syn in keyword.lower() for syn in synonyms):
                            score += 2

            # Apply priority factor
            score = score * (11 - source['priority'])  # Higher priority = higher score

            if score > 0:
                scored.append({
                    'source': source,
                    'score': score
                })

        # Sort by score
        scored.sort(key=lambda x: x['score'], reverse=True)

        return [item['source'] for item in scored]

    def extract_from_source(
        self,
        source: Dict[str, Any],
        query: str,
        mode: str
    ) -> Optional[Dict[str, Any]]:
        """Extract content from a single source"""

        url = source['url']
        name = source['name']

        print(f"🔍 Searching {name}...")

        # Use the main extract.py script
        try:
            result = subprocess.run(
                [
                    'python3',
                    os.path.join(os.path.dirname(__file__), 'extract.py'),
                    '--url', url,
                    '--mode', mode,
                    '--format', 'json',
                    '--output', f'/tmp/{name.replace(" ", "_")}_result.json'
                ],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                with open(f'/tmp/{name.replace(" ", "_")}_result.json', 'r') as f:
                    data = json.load(f)

                if data and len(data) > 0 and data[0].get('status') == 'success':
                    extracted = data[0]
                    extracted['source_name'] = name
                    extracted['source_priority'] = source['priority']
                    extracted['relevance_score'] = self.calculate_relevance(
                        extracted.get('content', ''),
                        query
                    )
                    return extracted

        except Exception as e:
            print(f"❌ Failed to extract from {name}: {str(e)}")

        return None

    def calculate_relevance(self, content: str, query: str) -> float:
        """Calculate relevance score between content and query"""

        content_lower = content.lower()
        query_lower = query.lower()

        # Count keyword matches
        matches = 0
        for word in query.split():
            if word in content_lower:
                matches += 1

        # Calculate score (0-1)
        if len(query.split()) == 0:
            return 0.0

        return matches / len(query.split())

    def search_by_category(
        self,
        category: str,
        mode: str = "browser"
    ) -> List[Dict[str, Any]]:
        """Search all sources for a specific category"""

        if category not in self.sources['search_categories']:
            raise ValueError(f"Unknown category: {category}")

        category_config = self.sources['search_categories'][category]

        results = []
        for keyword in category_config['keywords'][:5]:  # Limit keywords
            print(f"\n📂 Searching for: {keyword}")

            category_results = self.search(
                query=keyword,
                max_results=3,
                category=category,
                mode=mode
            )
            results.extend(category_results)

        # Deduplicate and sort by relevance
        seen = set()
        unique_results = []
        for result in results:
            key = result.get('url', '')
            if key not in seen:
                seen.add(key)
                unique_results.append(result)

        unique_results.sort(
            key=lambda x: x.get('relevance_score', 0),
            reverse=True
        )

        return unique_results

    def list_sources(self) -> None:
        """List all configured sources"""

        print("\n📚 Available AI News Sources:\n")

        for source in self.sources['ai_news_sources']:
            print(f"  • {source['name']}")
            print(f"    URL: {source['url']}")
            print(f"    Priority: {source['priority']}")
            print(f"    Keywords: {', '.join(source['keywords'][:3])}...")
            print()

    def list_categories(self) -> None:
        """List all search categories"""

        print("\n📂 Available Search Categories:\n")

        for category, config in self.sources['search_categories'].items():
            print(f"  • {category}")
            print(f"    Keywords: {', '.join(config['keywords'][:5])}...")
            print()


def main():
    parser = argparse.ArgumentParser(
        description='Smart Search - AI news from known sources'
    )

    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--category', help='Search by category')
    parser.add_argument('--max-results', type=int, default=10,
                       help='Maximum results (default: 10)')
    parser.add_argument('--mode', choices=['light', 'browser', 'deep'],
                       default='browser', help='Extraction mode')
    parser.add_argument('--list-sources', action='store_true',
                       help='List all configured sources')
    parser.add_argument('--list-categories', action='store_true',
                       help='List all search categories')
    parser.add_argument('--sources', default='references/search_sources.json',
                       help='Path to sources config file')

    args = parser.parse_args()

    # Change to skill directory
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(skill_dir)

    sources_file = args.sources
    if not os.path.isabs(sources_file):
        sources_file = os.path.join(skill_dir, sources_file)

    try:
        searcher = SmartSearcher(sources_file)

        if args.list_sources:
            searcher.list_sources()
        elif args.list_categories:
            searcher.list_categories()
        elif args.category:
            results = searcher.search_by_category(args.category, args.mode)
            print_results(results, args.max_results)
        elif args.query:
            results = searcher.search(
                args.query,
                args.max_results,
                mode=args.mode
            )
            print_results(results, args.max_results)
        else:
            parser.print_help()

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def print_results(results: List[Dict[str, Any]], max_results: int) -> None:
    """Print search results"""

    print(f"\n{'='*60}")
    print(f"📰 Found {len(results)} results")
    print(f"{'='*60}\n")

    results = results[:max_results]

    for i, result in enumerate(results, 1):
        print(f"{'─'*60}")
        print(f"#{i} {result.get('title', 'Untitled')}")
        print(f"{'─'*60}")

        source = result.get('source_name', 'Unknown')
        relevance = result.get('relevance_score', 0) * 100

        print(f"📂 Source: {source}")
        print(f"📊 Relevance: {relevance:.1f}%")
        print(f"🔗 URL: {result.get('url', '')}")

        if 'summary' in result and result['summary']:
            print(f"\n📝 Summary:\n{result['summary']}\n")

        content = result.get('content', '')
        if content:
            # Show first 500 characters
            preview = content[:500] + '...' if len(content) > 500 else content
            print(f"📄 Content Preview:\n{preview}\n")

        print(f"📅 Extracted: {result.get('extraction_time', 'N/A')}")
        print(f"📏 Words: {result.get('word_count', 0)}")
        print()

    print(f"{'='*60}")
    print(f"Showing {min(len(results), max_results)} of {len(results)} results")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
