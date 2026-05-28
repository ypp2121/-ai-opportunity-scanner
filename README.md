# AI Opportunity Scanner

A [Kimi Code CLI](https://github.com/MoonshotAI/kimi-cli) skill for discovering hidden business opportunities unlocked by AI-driven cost reduction.

## Core Idea

AI doesn't just make existing tasks faster — it changes which tasks are **economically viable** in the first place.

> **Before AI**: Expert labor cost > value of the task → skipped  
> **After AI**: Marginal cost drops 10-100x → the same task becomes a profitable market

This skill systematically scans any industry for these "cost inversion" opportunities.

## What It Does

When triggered, the skill walks through a structured analysis:

1. **Framework analysis** — applies 6 lenses (information asymmetry, expert bottleneck, data deluge, etc.)
2. **Pattern matching** — checks 12 reusable AI cost-inversion archetypes
3. **Cross-industry comparison** — transferable patterns from energy, legal, agriculture, healthcare, and more
4. **Opportunity matrix** — produces a standardized deliverable with prioritized next steps

## Installation

### Option 1: Copy to your local skills directory
```bash
cp -r ai-opportunity-scanner ~/.codex/skills/
```

### Option 2: Install from GitHub (using skill-installer)
```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <your-username>/<your-repo> \
  --path ai-opportunity-scanner
```

## Usage Examples

Once installed, simply ask Kimi Code CLI:

> *"Analyze the legal services industry for AI cost-inversion opportunities"*

> *"What becomes viable in agriculture now that AI can process images and documents cheaply?"*

> *"Compare储能, healthcare, and construction using the AI opportunity scanner"*

## Skill Structure

```
ai-opportunity-scanner/
├── SKILL.md                              # Core skill instructions
├── agents/openai.yaml                    # UI metadata
├── references/
│   ├── framework.md                      # Analytical lenses & value-chain scanning
│   ├── patterns.md                       # 12 cost-inversion archetypes
│   └── examples.md                       # Worked examples across industries
└── assets/
    └── opportunity-matrix-template.md    # Standardized output template
```

## Daily Market Scanner (每日海外市场扫描)

自动化每日扫描北美和欧洲市场中与储能/太阳能相关的采购需求和招标信息。

### 扫描范围

| 产品类别 | 关键词示例 |
|----------|-----------|
| 储能电芯 | LFP battery cells, BESS cells, energy storage cells |
| PCS (储能变流器) | Power conversion system, bidirectional inverter |
| 储能柜 | Battery cabinet, containerized storage system |
| 太阳能板 | Solar modules, PV panels |

| 市场区域 | 覆盖国家 |
|----------|---------|
| 北美 | 美国、加拿大 |
| 欧洲 | 德国、英国、法国、西班牙、意大利、荷兰、波兰、瑞典 |

### 工作原理

1. GitHub Actions 定时任务每天 UTC 8:00 (北京时间 16:00) 执行
2. Python 脚本通过搜索 API 抓取最新的采购/招标/需求信息
3. 按产品类别和地区整理，生成结构化 Markdown 日报
4. 日报自动提交到 `reports/` 目录，同时作为 GitHub Actions Artifact 保存

### 配置搜索 API

至少需要配置以下 **一组** API 密钥 (在仓库 Settings → Secrets and variables → Actions 中添加):

| 方案 | 所需 Secrets | 获取方式 |
|------|-------------|---------|
| Google Custom Search | `GOOGLE_API_KEY` + `GOOGLE_CSE_ID` | [Google Cloud Console](https://console.cloud.google.com/) |
| SerpApi | `SERPAPI_KEY` | [serpapi.com](https://serpapi.com/) |
| NewsAPI (新闻补充) | `NEWSAPI_KEY` | [newsapi.org](https://newsapi.org/) |

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 生成示例报告 (无需 API key)
python3 scripts/generate_sample_report.py

# 实际扫描 (需要至少一个 API key)
export SERPAPI_KEY="your-key"
python3 scripts/market_scanner.py
```

### 手动触发

在 GitHub → Actions → "Daily Energy Storage Market Scanner" 页面点击 **Run workflow** 即可手动执行。

### 自定义配置

编辑 `config/market_scan_config.yaml` 可以:
- 添加/修改搜索关键词
- 增加新的目标国家和地区
- 调整报告保留天数

### 文件结构

```
scripts/
├── market_scanner.py           # 主扫描脚本
└── generate_sample_report.py   # 示例报告生成
config/
└── market_scan_config.yaml     # 搜索关键词和区域配置
reports/
└── market-report-YYYY-MM-DD.md # 每日生成的市场报告
.github/workflows/
└── daily-market-scan.yml       # GitHub Actions 定时任务
```

## License

MIT
