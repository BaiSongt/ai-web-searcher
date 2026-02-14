# Smart Search 使用示例

## 基础用法

### 1. 查看所有可用的新闻源

```bash
cd ~/.openclaw/workspace/skills/ai-web-searcher
python3 scripts/smart_search.py --list-sources
```

输出：
```
📚 Available AI News Sources:

  • OpenAI News
    URL: https://openai.com/news
    Priority: 1
    Keywords: GPT, OpenAI, model...

  • Google AI Blog
    URL: https://blog.google/technology/ai/
    Priority: 1
    Keywords: Google, Gemini, Bard...
```

### 2. 查看所有搜索分类

```bash
python3 scripts/smart_search.py --list-categories
```

输出：
```
📂 Available Search Categories:

  • model_releases
    Keywords: GPT, Claude, Gemini...

  • research
    Keywords: paper, arXiv, breakthrough...

  • industry
    Keywords: funding, acquisition, IPO...
```

## 关键词搜索

### 搜索 OpenAI 模型发布

```bash
python3 scripts/smart_search.py "GPT model release" --max-results 5 --mode browser
```

### 搜索 AI 安全相关内容

```bash
python3 scripts/smart_search.py "AI safety regulation policy" --max-results 3
```

### 搜索多模态 AI

```bash
python3 scripts/smart_search.py "multimodal vision text-to-video" --mode browser
```

## 分类搜索

### 获取最新的模型发布新闻

```bash
python3 scripts/smart_search.py --category model_releases --max-results 10
```

这将搜索所有高优先级的源（OpenAI、Google、Anthropic 等）

### 查看最新的研究论文

```bash
python3 scripts/smart_search.py --category research --max-results 5 --mode browser
```

这将搜索 arXiv、MIT、DeepMind 等研究源

### 获取行业动态（融资、收购）

```bash
python3 scripts/smart_search.py --category industry --max-results 8
```

这将搜索 VentureBeat、TechCrunch 等行业源

## 实际应用场景

### 场景 1：每日 AI 新闻摘要

创建定时任务，每天早上获取 AI 新闻：

```bash
# 添加到 crontab 或使用 OpenClaw cron
0 8 * * * cd ~/.openclaw/workspace/skills/ai-web-searcher && \
    python3 scripts/smart_search.py --category model_releases --max-results 5 > /tmp/ai_news_$(date +\%Y\%m\%d).md
```

### 场景 2：监控特定关键词

持续监控 AI 安全相关内容：

```bash
# 创建脚本 monitor_safety.sh
#!/bin/bash
while true; do
    python3 scripts/smart_search.py "AI safety alignment" --max-results 3 >> safety_monitor.log
    echo "---" >> safety_monitor.log
    sleep 3600  # 每小时
done
```

### 场景 3：综合报告

生成每周 AI 行业报告：

```bash
#!/bin/bash
# weekly_ai_report.sh

REPORT="ai_weekly_$(date +\%Y\%m\%d).md"

echo "# AI Weekly Report" > $REPORT
echo "Date: $(date)" >> $REPORT
echo "" >> $REPORT

echo "## Model Releases" >> $REPORT
python3 scripts/smart_search.py --category model_releases --max-results 3 >> $REPORT

echo "" >> $REPORT
echo "## Research Breakthroughs" >> $REPORT
python3 scripts/smart_search.py --category research --max-results 3 >> $REPORT

echo "" >> $REPORT
echo "## Industry News" >> $REPORT
python3 scripts/smart_search.py --category industry --max-results 3 >> $REPORT

echo "" >> $REPORT
echo "## AI Safety" >> $REPORT
python3 scripts/smart_search.py --category safety --max-results 3 >> $REPORT
```

### 场景 4：对比搜索结果

搜索同一主题的不同表述：

```bash
# 搜索 LLM 相关内容
echo "=== Searching 'LLM' ===" >> llm_search.txt
python3 scripts/smart_search.py "LLM language model" >> llm_search.txt

# 搜索 generative AI 相关内容
echo "=== Searching 'generative AI' ===" >> genai_search.txt
python3 scripts/smart_search.py "generative AI GenAI" >> genai_search.txt

# 搜索 agents 相关内容
echo "=== Searching 'AI agents' ===" >> agents_search.txt
python3 scripts/smart_search.py "AI agents autonomous" >> agents_search.txt
```

### 场景 5：源优先级测试

测试不同关键词如何影响源选择：

```bash
# 搜索 "OpenAI" - 应该优先匹配 OpenAI News
python3 scripts/smart_search.py "OpenAI" --max-results 1

# 搜索 "Google" - 应该优先匹配 Google AI Blog
python3 scripts/smart_search.py "Google" --max-results 1

# 搜索 "DeepMind" - 应该优先匹配 DeepMind Blog
python3 scripts/smart_search.py "DeepMind" --max-results 1

# 搜索 "startup" - 应该优先匹配 VentureBeat
python3 scripts/smart_search.py "startup funding" --max-results 1
```

## 高级用法

### 1. 组合多个搜索

```bash
# 创建综合报告
for category in model_releases research industry; do
    echo "=== $category ===" >> comprehensive_report.md
    python3 scripts/smart_search.py --category $category --max-results 2 >> comprehensive_report.md
    echo "" >> comprehensive_report.md
done
```

### 2. 定制源配置

编辑 `references/search_sources.json` 添加自定义源：

```json
{
  "name": "My Company Blog",
  "url": "https://mycompany.com/blog",
  "keywords": ["mycompany", "product", "feature"],
  "update_frequency": "daily",
  "priority": 1
}
```

### 3. 输出到不同格式

```bash
# JSON 格式（默认）
python3 scripts/smart_search.py "AI news" > results.json

# 纯文本格式（可读）
python3 scripts/smart_search.py "AI news" | tee results.txt

# Markdown 格式（适合文档）
python3 scripts/smart_search.py "AI news" > results.md
```

## 性能优化

### 1. 使用 light 模式（静态网站）

```bash
# 快速但不完整
python3 scripts/smart_search.py "query" --mode light
```

### 2. 调整并发数

修改 `scripts/extract.py` 中的默认并发数：

```python
parser.add_argument('--concurrency', type=int, default=5)  # 改为 10
```

### 3. 限制结果数量

```bash
# 只获取前 3 个结果
python3 scripts/smart_search.py "AI news" --max-results 3
```

## 故障排除

### 问题：所有网站都无法提取

**原因**：网站需要浏览器渲染

**解决**：
```bash
# 使用 browser 模式
python3 scripts/smart_search.py "query" --mode browser
```

### 问题：结果不相关

**原因**：关键词不匹配

**解决**：
```bash
# 使用更具体的关键词
python3 scripts/smart_search.py "GPT-4o specific model" --max-results 5
```

### 问题：速度太慢

**原因**：浏览器模式开销大

**解决**：
```bash
# 减少并发数或使用 light 模式
python3 scripts/smart_search.py "query" --mode light
```

## 与其他工具集成

### 与 extract.py 结合

```bash
# 先用智能搜索找到相关源
python3 scripts/smart_search.py --list-sources > sources.txt

# 提取特定源
python3 scripts/extract.py --url "https://openai.com/news" --mode browser
```

### 与 OpenClaw cron 结合

```bash
# 每天早上 9 点搜索 AI 新闻
openclaw cron add \
  --name "每日AI新闻" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "cd ~/.openclaw/workspace/skills/ai-web-searcher && python3 scripts/smart_search.py --category model_releases --max-results 5" \
  --deliver
```

## 最佳实践

1. **定期更新源**：每月检查并更新 `search_sources.json`
2. **使用分类搜索**：比关键词搜索更快、更准确
3. **保存结果**：定期备份搜索结果到文件
4. **调整关键词**：根据需要更新源的关键词列表
5. **监控性能**：记录搜索时间，优化配置

## 扩展建议

1. **添加更多源**：扩展到 20+ 个源
2. **增加分类**：添加更多细分类别
3. **实现缓存**：缓存已提取内容，减少重复请求
4. **AI 摘要**：集成 AI 模型生成智能摘要
5. **多语言支持**：添加中文、日文等源
