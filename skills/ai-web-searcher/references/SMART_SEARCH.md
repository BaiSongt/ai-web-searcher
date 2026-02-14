# Smart Search - 智能搜索功能

## 概述

Smart Search 是 AI Web Searcher 的扩展功能，优先从预配置的 AI 新闻源搜索内容，提高相关性和准确性。

## 工作原理

### 1. 知识源优先
- 维护 10+ 个权威 AI 新闻源
- 包括 OpenAI、Google、DeepMind、Anthropic 官方博客
- 涵盖 TechCrunch、The Verge、MIT Tech Review 等媒体

### 2. 关键词匹配
- 根据搜索查询匹配关键词
- 使用同义词映射提高匹配率
- 评分系统排序相关性

### 3. 分类搜索
- 按类别快速定位内容
- 6 大类：模型发布、研究、产品、行业、安全、应用

---

## 配置文件

### 位置
`references/search_sources.json`

### 结构

```json
{
  "ai_news_sources": [
    {
      "name": "Source Name",
      "url": "https://example.com",
      "keywords": ["keyword1", "keyword2"],
      "update_frequency": "daily",
      "priority": 1
    }
  ],
  "search_categories": {
    "category_name": {
      "keywords": ["keyword1", "keyword2"],
      "sources": ["source1", "source2"]
    }
  },
  "keyword_mappings": {
    "term": ["synonym1", "synonym2"]
  }
}
```

---

## 使用方法

### 查看所有源

```bash
python3 scripts/smart_search.py --list-sources
```

### 查看所有分类

```bash
python3 scripts/smart_search.py --list-categories
```

### 关键词搜索

```bash
# 基本搜索
python3 scripts/smart_search.py "GPT OpenAI model"

# 限制结果数
python3 scripts/smart_search.py "AI safety" --max-results 5

# 指定提取模式
python3 scripts/smart_search.py "machine learning" --mode browser
```

### 分类搜索

```bash
# 搜索模型发布
python3 scripts/smart_search.py --category model_releases

# 搜索研究论文
python3 scripts/smart_search.py --category research

# 搜索行业新闻
python3 scripts/smart_search.py --category industry
```

---

## 搜索类别

### 1. model_releases（模型发布）
**关键词**：GPT, Claude, Gemini, Llama, Mistral, release, launch, model
**主要源**：OpenAI, Google, DeepMind, Anthropic

### 2. research（研究）
**关键词**：paper, arXiv, breakthrough, research, study, experiment
**主要源**：arXiv, MIT, DeepMind

### 3. products（产品）
**关键词**：product, feature, update, launch, app, tool
**主要源**：OpenAI, Google, TechCrunch, Verge

### 4. industry（行业）
**关键词**：funding, acquisition, IPO, startup, company, business
**主要源**：VentureBeat, TechCrunch

### 5. safety（安全）
**关键词**：safety, alignment, regulation, policy, ethics, governance
**主要源**：OpenAI, Anthropic, DeepMind, MIT

### 6. applications（应用）
**关键词**：application, deployment, use case, integration, enterprise
**主要源**：AI News, TechCrunch, Verge

---

## 关键词映射

### 模型相关
- `gpt` → GPT, GPT-4, GPT-4o, GPT-4.5
- `claude` → Claude, Claude 3, Claude 4, Anthropic Claude
- `gemini` → Gemini, Google Gemini, Gemini Pro, Gemini Ultra

### 技术术语
- `llm` → LLM, Large Language Model, language model, text model
- `generative_ai` → generative AI, GenAI, generative, text-to-image, text-to-video
- `agents` → AI agent, autonomous agent, AI assistant, copilot

### 多模态
- `multimodal` → multimodal, multi-modal, vision, audio, video model

---

## 工作流程

### 搜索流程

```
用户查询
    ↓
关键词分析
    ↓
源评分（基于关键词匹配 + 优先级）
    ↓
按分数排序
    ↓
并发提取（使用 extract.py）
    ↓
相关性计算
    ↓
结果排序和去重
    ↓
返回结果
```

### 评分算法

```
Score = (直接关键词匹配数) × (11 - 优先级)

示例：
- 关键词匹配 3 次，优先级 1
  Score = 3 × 10 = 30

- 关键词匹配 2 次，优先级 5
  Score = 2 × 6 = 12
```

---

## 相关性计算

### 算法
```
Relevance = 匹配词数 / 查询总词数
```

### 示例
- 查询："GPT model release"（3 词）
- 内容："GPT-4o is the latest model release from OpenAI"
- 匹配：GPT, model, release（3 词）
- 相关性：3/3 = 100%

---

## 局限性

### 当前限制

1. **需要浏览器渲染**
   - 大多数现代新闻网站使用 JavaScript
   - `--mode light` 无法获取动态内容
   - 需要 `--mode browser` 或 `--mode deep`

2. **实时性**
   - 每次搜索都重新提取
   - 没有缓存机制
   - 适合偶尔使用，不适合高频搜索

3. **源依赖**
   - 仅限预配置的 10 个源
   - 无法搜索整个互联网
   - 需要定期更新源配置

---

## 未来增强

### 计划功能

1. **缓存机制**
   - 缓存已提取内容
   - 减少 API 调用
   - 提高响应速度

2. **增量更新**
   - 只提取新内容
   - 基于时间戳过滤
   - 减少带宽使用

3. **智能摘要**
   - 使用 AI 模型生成摘要
   - 提取关键信息
   - 生成要点列表

4. **用户自定义源**
   - 允许添加个人源
   - 支持本地文件
   - 灵活配置

5. **搜索历史**
   - 记录搜索查询
   - 保存结果
   - 便于回顾

---

## 最佳实践

### 选择正确的模式

| 场景 | 模式 | 原因 |
|--------|------|--------|
| 静态博客 | light | 速度快，资源少 |
| 动态新闻网站 | browser | 完整渲染 |
| 复杂网站 | deep | 最彻底提取 |

### 优化搜索查询

- **具体关键词**：`"GPT-4o model"` 比 `"model"` 更好
- **使用同义词**：`"LLM language model"` 匹配更多内容
- **组合查询**：`"AI safety regulation"` 交叉匹配

### 利用分类

- **快速浏览**：使用 `--category` 快速获取某一类新闻
- **深入挖掘**：多次搜索不同类别
- **综合分析**：对比不同来源的同一主题

---

## 故障排除

### 问题：没有结果

**可能原因**：
1. 模式不匹配（静态 vs 动态）
2. 网站结构变化
3. 网络连接问题

**解决方案**：
```bash
# 尝试不同的模式
python3 scripts/smart_search.py "query" --mode browser

# 检查单个源
python3 scripts/extract.py --url "https://example.com" --mode browser
```

### 问题：结果不相关

**可能原因**：
1. 关键词匹配度低
2. 源优先级配置不当

**解决方案**：
- 使用更具体的关键词
- 调整源配置中的关键词
- 修改源优先级

### 问题：速度慢

**可能原因**：
1. 浏览器模式开销大
2. 并发数过低

**解决方案**：
```bash
# 使用 light 模式（如果可能）
python3 scripts/smart_search.py "query" --mode light

# 增加并发
# 修改 extract.py 中的默认并发数
```

---

## 示例用例

### 用例 1：追踪模型发布

```bash
# 每天运行一次
python3 scripts/smart_search.py --category model_releases --max-results 5

# 输出到文件
python3 scripts/smart_search.py --category model_releases > model_news.log
```

### 用例 2：行业研究

```bash
# 搜索多个类别
for cat in model_releases research industry; do
    echo "=== $cat ===" >> industry_report.md
    python3 scripts/smart_search.py --category $cat >> industry_report.md
done
```

### 用例 3：监控特定关键词

```bash
# 创建定时任务，每小时搜索
0 * * * * cd ~/.openclaw/workspace/skills/ai-web-searcher && \
    python3 scripts/smart_search.py "AI safety regulation" >> safety_watch.log
```

---

## 集成指南

### 与 extract.py 集成

Smart Search 调用 extract.py 进行内容提取：
```python
result = subprocess.run([
    'python3', 'extract.py',
    '--url', url,
    '--mode', mode,
    '--format', 'json'
])
```

### 与 OpenClaw 集成

可以作为 OpenClaw Skill 使用：
```markdown
当用户搜索 AI 新闻时，使用 smart_search.py 从预配置源提取内容。
优先使用分类搜索，然后是关键词搜索。
```

---

## 性能指标

| 指标 | 值 |
|--------|-----|
| 源数量 | 10+ |
| 搜索类别 | 6 |
| 关键词映射 | 20+ |
| 平均响应时间 | 10-30 秒（browser 模式） |
| 准确率 | ~80%（基于关键词匹配） |

---

## 贡献

### 添加新源

编辑 `references/search_sources.json`：

```json
{
  "name": "New Source",
  "url": "https://example.com",
  "keywords": ["keyword1", "keyword2"],
  "update_frequency": "daily",
  "priority": 3
}
```

### 添加新类别

```json
{
  "new_category": {
    "keywords": ["keyword1", "keyword2"],
    "sources": ["source1", "source2"]
  }
}
```

---

## 总结

Smart Search 通过预配置的权威源和智能关键词匹配，为 AI 领域提供更准确、更相关的搜索结果。

**优势**：
- ✅ 高相关性（源 + 关键词双匹配）
- ✅ 分类浏览（快速定位）
- ✅ 可配置（灵活扩展）
- ⏳ 实时性（每次搜索都提取）

**限制**：
- ❌ 需要浏览器渲染（慢）
- ❌ 源数量有限
- ⏳ 无缓存机制

**适用场景**：
- 定期 AI 新闻追踪
- 特定主题研究
- 行业动态监控

不适合：
- 实时全网搜索
- 超高频查询
- 非AI领域搜索
