# Concurrency Patterns

## Understanding Concurrency in AI Web Searcher

The tool uses **ThreadPoolExecutor** to manage concurrent extractions. Each extraction runs in its own thread, allowing multiple web pages to be processed simultaneously.

## Thread Safety Considerations

### Thread-Safe Operations
- ✅ File I/O (each thread writes to separate result objects)
- ✅ HTTP requests (each thread has its own session)
- ✅ Memory operations (local variables in each thread)

### Not Thread-Safe
- ❌ Shared file writes (use separate log files or proper locking)
- ❌ Shared state without synchronization (avoid global variables)

## Concurrency Patterns

### Pattern 1: Bounded Concurrency

Limit concurrent operations to avoid overwhelming the target server or your system:

```bash
python3 scripts/extract.py --urls urls.txt --concurrency 5
```

**When to use**:
- Extracting from multiple domains
- Limited system resources
- Unknown target server capacity

**Recommended settings**:
- **Conservative**: 2-3 threads
- **Balanced**: 5-10 threads (default)
- **Aggressive**: 10-20 threads (powerful machine + high bandwidth)

### Pattern 2: Adaptive Concurrency

Start with conservative settings and increase based on success rate:

```bash
# First pass - low concurrency
python3 scripts/extract.py --urls urls.txt --concurrency 3 --delay 2

# If successful, increase for second pass
python3 scripts/extract.py --urls urls.txt --concurrency 8 --delay 1
```

### Pattern 3: Domain-Specific Concurrency

Group URLs by domain and use different concurrency per domain:

```json
{
  "groups": [
    {
      "domain": "example.com",
      "urls": ["https://example.com/page1", "https://example.com/page2"],
      "concurrency": 3,
      "delay": "2"
    },
    {
      "domain": "another-site.com",
      "urls": ["https://another-site.com/page1"],
      "concurrency": 1,
      "delay": "0"
    }
  ]
}
```

## Resource Management

### Memory Usage

Each thread uses approximately:
- **Light mode**: ~10-20 MB
- **Browser mode**: ~100-200 MB
- **Deep mode**: ~200-500 MB

**Formula**: `Expected Memory = Threads × Memory per Thread`

Example:
```
5 threads × 150 MB (browser mode) = 750 MB
```

### CPU Usage

Browser and deep modes are CPU-intensive:
- **Rendering**: 1-2 cores per thread
- **AI analysis**: Additional CPU usage

**Rule of thumb**: Set concurrency ≤ (Available CPU Cores / 2)

### Network Bandwidth

Estimate bandwidth requirements:
- **Average page size**: ~500 KB - 2 MB
- **Concurrent requests**: Concurrency × Page size

Example:
```
5 threads × 1 MB = 5 MB/s peak bandwidth
```

## Rate Limiting Strategies

### Fixed Delay

```bash
# Consistent delay between all requests
python3 scripts/extract.py --urls urls.txt --delay 2
```

### Random Delay Range

```bash
# Random delay between 1-3 seconds
python3 scripts/extract.py --urls urls.txt --delay 1-3
```

**Advantage**: Less detectable as automated traffic

### Exponential Backoff

Not directly supported, but can be simulated:
1. First attempt: `--delay 1`
2. Retry attempts: `--retries 3` (built-in exponential backoff)

## Error Recovery Patterns

### Pattern 1: Fail Fast

Stop on first error:

```bash
# Default behavior
python3 scripts/extract.py --urls urls.txt
```

**Use when**:
- Early errors indicate a problem
- Data consistency is critical
- You want to debug issues immediately

### Pattern 2: Continue on Error

Continue processing even if some URLs fail:

```bash
python3 scripts/extract.py --urls urls.txt --continue-on-error --log errors.log
```

**Use when**:
- Some failures are acceptable
- You want maximum data collected
- Failed URLs can be retried later

### Pattern 3: Retry Pattern

Built-in retry mechanism:

```bash
# Retry failed URLs up to 3 times
python3 scripts/extract.py --urls urls.txt --retries 3 --delay 1-2
```

**Best practice**:
- Combine retries with delays to avoid rate limiting
- Start with `--retries 3` and increase if needed
- Use `--delay 1-3` for retry scenarios

## Performance Tuning

### Scenario 1: High Volume, Simple Pages

**Goal**: Extract thousands of simple blog posts

**Configuration**:
```bash
python3 scripts/extract.py --urls urls.txt --mode light --concurrency 20 --delay 0
```

**Expected throughput**: ~100-200 pages/minute

### Scenario 2: Medium Volume, Dynamic Pages

**Goal**: Extract hundreds of React/Vue apps

**Configuration**:
```bash
python3 scripts/extract.py --urls urls.txt --mode browser --concurrency 5 --delay 1
```

**Expected throughput**: ~20-50 pages/minute

### Scenario 3: Low Volume, Complex Sites

**Goal**: Extract from YouTube, social media

**Configuration**:
```bash
python3 scripts/extract.py --urls urls.txt --mode deep --concurrency 2 --delay 2-5
```

**Expected throughput**: ~5-10 pages/minute

## Monitoring Concurrency

### Log Output

The tool provides real-time feedback:
```
✅ Success: https://example.com (1234 words)
✅ Success: https://another.com (567 words)
❌ Failed: https://blocked.com - Rate limit exceeded
```

### Error Logging

Enable error logging for analysis:
```bash
python3 scripts/extract.py --urls urls.txt --continue-on-error --log errors.json
```

Analyze failures to adjust concurrency:
```json
[
  {
    "url": "https://blocked.com",
    "status": "failed",
    "error": "Rate limit exceeded"
  }
]
```

**Adjustment**: Increase delay or reduce concurrency

## Advanced Patterns

### Chunked Processing

For very large URL lists, process in chunks:

```bash
# Split urls.txt into chunks of 100
split -l 100 urls.txt chunk_

# Process each chunk
for chunk in chunk_*; do
  python3 scripts/extract.py --urls $chunk --output results_$chunk.json --concurrency 5
done
```

### Distributed Extraction

Run multiple instances on different machines:

```bash
# Machine 1
python3 scripts/extract.py --urls urls_part1.txt --concurrency 5

# Machine 2 (simultaneously)
python3 scripts/extract.py --urls urls_part2.txt --concurrency 5
```

Combine results later:
```bash
cat results_part*.json > combined_results.json
```

## Best Practices Summary

| Scenario | Concurrency | Delay | Mode |
|----------|-------------|-------|------|
| High volume, simple pages | 10-20 | 0 | light |
| Medium volume, dynamic pages | 5-10 | 1-2 | browser |
| Low volume, complex sites | 2-5 | 2-5 | deep |
| Unknown server | 3-5 | 2-3 | browser |
| Same domain, many URLs | 2-3 | 2-5 | any |

**Golden rule**: Start conservative, increase gradually, monitor for errors.
