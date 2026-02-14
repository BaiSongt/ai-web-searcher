#!/usr/bin/env python3
"""
AI Web Searcher - Multi-threaded web content extraction tool
"""

import argparse
import asyncio
import json
import os
import sys
import time
import random
from datetime import datetime
from typing import List, Dict, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add OpenClaw workspace to path
workspace = os.path.expanduser('~/.openclaw/workspace')
if workspace not in sys.path:
    sys.path.insert(0, workspace)

try:
    import subprocess
except ImportError:
    pass


class WebExtractor:
    """Extract content from web pages with AI analysis"""

    def __init__(
        self,
        mode: str = "browser",
        concurrency: int = 3,
        delay: str = "0",
        retries: int = 3,
        summarize: bool = False,
        summary_length: int = 200,
        selectors: Optional[Dict] = None,
        auth: Optional[str] = None,
        cookies: Optional[str] = None
    ):
        self.mode = mode
        self.concurrency = concurrency
        self.delay = delay
        self.retries = retries
        self.summarize = summarize
        self.summary_length = summary_length
        self.selectors = selectors or {}
        self.auth = auth
        self.cookies = cookies

    def parse_delay(self) -> tuple:
        """Parse delay string (e.g., "2", "1-3")"""
        if '-' in self.delay:
            min_delay, max_delay = map(float, self.delay.split('-'))
            return min_delay, max_delay
        return float(self.delay), float(self.delay)

    def get_delay(self) -> float:
        """Get delay for this request"""
        min_delay, max_delay = self.parse_delay()
        if min_delay == max_delay:
            return min_delay
        return random.uniform(min_delay, max_delay)

    async def extract_single_url(
        self,
        url: str,
        url_config: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Extract content from a single URL with retry logic"""

        url_config = url_config or {}
        mode = url_config.get('mode', self.mode)

        for attempt in range(self.retries):
            try:
                # Add delay if configured
                if self.delay != "0" and attempt > 0:
                    delay_time = self.get_delay()
                    time.sleep(delay_time)

                # Choose extraction method based on mode
                if mode == "light":
                    result = await self.extract_light(url)
                elif mode == "browser":
                    result = await self.extract_browser(url)
                elif mode == "deep":
                    result = await self.extract_deep(url)
                else:
                    raise ValueError(f"Unknown mode: {mode}")

                result['extraction_mode'] = mode
                result['attempt'] = attempt + 1

                # Add AI summary if requested
                if self.summarize:
                    result['summary'] = await self.generate_summary(result)

                return result

            except Exception as e:
                print(f"Attempt {attempt + 1}/{self.retries} failed for {url}: {str(e)}")
                if attempt == self.retries - 1:
                    return {
                        "url": url,
                        "status": "failed",
                        "error": str(e),
                        "attempts": attempt + 1
                    }

    async def extract_light(self, url: str) -> Dict[str, Any]:
        """Light extraction using web_fetch (static HTML)"""

        # Use OpenClaw's web_fetch via CLI
        cmd = ['curl', '-s', '-L', url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            raise Exception(f"Failed to fetch URL: {result.stderr}")

        html_content = result.stdout

        # Basic content extraction (can be enhanced)
        title = self._extract_title(html_content)
        content = self._extract_content(html_content)

        return {
            "url": url,
            "title": title,
            "content": content,
            "status": "success",
            "extraction_time": datetime.utcnow().isoformat() + "Z",
            "word_count": len(content.split())
        }

    async def extract_browser(self, url: str) -> Dict[str, Any]:
        """Browser-based extraction (full rendering)"""

        # Use OpenClaw's browser tool
        try:
            # Try using browser tool via exec
            cmd = ['openclaw', 'browser', 'open', '--url', url, '--timeout', '30']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            # For now, fallback to fetch + basic parsing
            # In production, this would use the browser API properly
            return await self.extract_light(url)

        except Exception as e:
            print(f"Browser extraction failed, falling back to light mode: {e}")
            return await self.extract_light(url)

    async def extract_deep(self, url: str) -> Dict[str, Any]:
        """Deep extraction using Crawlee (for complex sites)"""

        # Placeholder for deep scraper integration
        # Would integrate with deep-scraper skill
        print(f"Deep extraction not fully implemented, using browser mode for {url}")
        return await self.extract_browser(url)

    def _extract_title(self, html: str) -> str:
        """Extract title from HTML"""
        import re
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            return title_match.group(1).strip()
        return "Untitled"

    def _extract_content(self, html: str) -> str:
        """Extract main content from HTML"""

        # Remove script and style tags
        import re
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.IGNORECASE | re.DOTALL)

        # Extract paragraphs
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.IGNORECASE | re.DOTALL)

        # Clean HTML tags
        content = []
        for p in paragraphs:
            # Remove HTML tags
            clean_p = re.sub(r'<[^>]+>', '', p)
            clean_p = clean_p.strip()
            if len(clean_p) > 50:  # Filter very short paragraphs
                content.append(clean_p)

        return '\n\n'.join(content[:20])  # Limit to first 20 paragraphs

    async def generate_summary(self, result: Dict[str, Any]) -> str:
        """Generate AI summary of content"""

        # Placeholder for AI summarization
        # In production, this would call the AI model
        content = result.get('content', '')[:2000]
        words = content.split()

        if len(words) <= self.summary_length:
            return content

        return ' '.join(words[:self.summary_length]) + '...'


async def extract_urls(
    urls: List[str],
    extractor: WebExtractor,
    continue_on_error: bool = False,
    log_file: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Extract content from multiple URLs concurrently"""

    results = []
    errors = []

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=extractor.concurrency) as executor:
        # Submit all tasks
        future_to_url = {}
        for url_config in urls:
            if isinstance(url_config, str):
                url = url_config
                config = {}
            else:
                url = url_config.get('url')
                config = url_config

            future = executor.submit(
                asyncio.run,
                extractor.extract_single_url(url, config)
            )
            future_to_url[future] = url

        # Collect results as they complete
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)

                if result.get('status') == 'failed':
                    errors.append(result)
                    print(f"❌ Failed: {url} - {result.get('error', 'Unknown error')}")
                else:
                    print(f"✅ Success: {url} ({result.get('word_count', 0)} words)")

            except Exception as e:
                error_result = {
                    "url": url,
                    "status": "failed",
                    "error": str(e)
                }
                errors.append(error_result)
                if continue_on_error:
                    results.append(error_result)
                print(f"❌ Exception for {url}: {str(e)}")

                if not continue_on_error:
                    break

    # Log errors if requested
    if log_file and errors:
        with open(log_file, 'w') as f:
            json.dump(errors, f, indent=2)
        print(f"\nLogged {len(errors)} errors to {log_file}")

    return results


def load_urls(input_path: str) -> List[Dict[str, Any]]:
    """Load URLs from file (txt or json)"""

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Check file extension
    if input_path.endswith('.json'):
        with open(input_path, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'urls' in data:
                return data['urls']
            else:
                raise ValueError("Invalid JSON format")
    else:
        # Assume text file (one URL per line)
        with open(input_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        return [{"url": url} for url in urls]


def save_results(
    results: List[Dict[str, Any]],
    output_path: str,
    format: str
) -> None:
    """Save results to file"""

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    elif format == 'markdown':
        with open(output_path, 'w', encoding='utf-8') as f:
            for result in results:
                if result.get('status') == 'failed':
                    f.write(f"# ❌ Failed\n\n")
                    f.write(f"**URL**: {result['url']}\n")
                    f.write(f"**Error**: {result.get('error', 'Unknown')}\n\n")
                    f.write("---\n\n")
                    continue

                f.write(f"# {result.get('title', 'Untitled')}\n\n")
                f.write(f"**URL**: {result['url']}\n")
                f.write(f"**Extracted**: {result.get('extraction_time', 'N/A')}\n")
                f.write(f"**Words**: {result.get('word_count', 0)}\n")

                if 'summary' in result:
                    f.write(f"\n## Summary\n\n{result['summary']}\n\n")

                f.write(f"## Content\n\n{result.get('content', '')}\n\n")
                f.write("---\n\n")

    elif format == 'csv':
        import csv
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'url', 'title', 'summary', 'word_count',
                'extraction_time', 'extraction_mode', 'status'
            ])
            writer.writeheader()
            for result in results:
                writer.writerow({
                    'url': result.get('url', ''),
                    'title': result.get('title', ''),
                    'summary': result.get('summary', ''),
                    'word_count': result.get('word_count', 0),
                    'extraction_time': result.get('extraction_time', ''),
                    'extraction_mode': result.get('extraction_mode', ''),
                    'status': result.get('status', 'failed')
                })

    else:
        raise ValueError(f"Unsupported format: {format}")


def main():
    parser = argparse.ArgumentParser(
        description='AI Web Searcher - Multi-threaded web content extraction'
    )

    # Input options
    parser.add_argument('--url', action='append', help='Single URL to extract (can be used multiple times)')
    parser.add_argument('--urls', help='File containing URLs (txt or json)')

    # Extraction options
    parser.add_argument('--mode', choices=['light', 'browser', 'deep'], default='browser',
                       help='Extraction mode (default: browser)')
    parser.add_argument('--concurrency', type=int, default=3,
                       help='Number of concurrent extractions (default: 3)')
    parser.add_argument('--delay', default='0',
                       help='Delay between requests (e.g., "2" or "1-3" seconds, default: 0)')
    parser.add_argument('--retries', type=int, default=3,
                       help='Number of retries for failed extractions (default: 3)')

    # AI options
    parser.add_argument('--summarize', action='store_true',
                       help='Enable AI summarization')
    parser.add_argument('--summary-length', type=int, default=200,
                       help='Summary length in words (default: 200)')

    # Custom selectors
    parser.add_argument('--selectors',
                       help='JSON file with custom CSS selectors')

    # Authentication
    parser.add_argument('--auth', help='Authentication (user:pass)')
    parser.add_argument('--cookies', help='Cookie file')

    # Output options
    parser.add_argument('--format', choices=['json', 'markdown', 'csv'], default='json',
                       help='Output format (default: json)')
    parser.add_argument('--output', default='results.json',
                       help='Output file (default: results.json)')

    # Error handling
    parser.add_argument('--continue-on-error', action='store_true',
                       help='Continue on errors instead of stopping')
    parser.add_argument('--log', help='Log file for errors')

    args = parser.parse_args()

    # Load URLs
    url_configs = []

    if args.urls:
        url_configs = load_urls(args.urls)
    elif args.url:
        url_configs = [{"url": url} for url in args.url]
    else:
        parser.error("Must provide --urls or --url")

    # Load custom selectors if provided
    selectors = None
    if args.selectors:
        with open(args.selectors, 'r') as f:
            selectors = json.load(f)

    # Create extractor
    extractor = WebExtractor(
        mode=args.mode,
        concurrency=args.concurrency,
        delay=args.delay,
        retries=args.retries,
        summarize=args.summarize,
        summary_length=args.summary_length,
        selectors=selectors,
        auth=args.auth,
        cookies=args.cookies
    )

    # Extract content
    print(f"🚀 Starting extraction of {len(url_configs)} URLs...")
    print(f"   Mode: {args.mode}")
    print(f"   Concurrency: {args.concurrency}")
    print(f"   Delay: {args.delay}s\n")

    results = asyncio.run(extract_urls(
        urls=url_configs,
        extractor=extractor,
        continue_on_error=args.continue_on_error,
        log_file=args.log
    ))

    # Save results
    save_results(results, args.output, args.format)

    # Print summary
    successful = sum(1 for r in results if r.get('status') == 'success')
    failed = len(results) - successful

    print(f"\n✨ Extraction complete!")
    print(f"   Total: {len(results)}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Output: {args.output}")


if __name__ == '__main__':
    main()
