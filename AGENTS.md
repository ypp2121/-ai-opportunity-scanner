# AGENTS.md

## Cursor Cloud specific instructions

### 仓库概览

本仓库包含两个能力，均**无本地 HTTP 服务或监听端口**：

1. **AI Opportunity Scanner** — Kimi/Codex CLI 技能（`SKILL.md`、`references/`、`assets/`），通过宿主 CLI + LLM 使用，无 in-repo 服务器。
2. **Daily Energy Storage Market Scanner** — Python 批处理 CLI（`scripts/market_scanner.py`），生成 `reports/market-report-YYYY-MM-DD.md`。

### 依赖安装

标准命令见 [README.md](README.md)。VM 启动时由 update script 执行：

```bash
python3 -m pip install -r requirements.txt
```

仅需 **Python 3** 与 `requests`、`pyyaml`（无 Node.js、Docker Compose）。

### 开发与验证

| 目标 | 命令 | 说明 |
|------|------|------|
| 离线 E2E（推荐） | `python3 scripts/generate_sample_report.py` | 无需 API key，验证报告格式与 `config/market_scan_config.yaml` |
| 实网扫描 | `export BRAVE_API_KEY=...` 后 `python3 scripts/market_scanner.py` | 至少配置 Brave、Google+CSE、SerpApi 之一；仅 `NEWSAPI_KEY` 不足以作为唯一主后端 |
| 语法检查 | `python3 -m py_compile scripts/*.py` | 仓库未配置 pytest/ruff/flake8 |

### 实网扫描注意事项

- 无搜索 API 时，`market_scanner.py` 会以 exit code 1 结束，但仍可能写入**空线索**日报并覆盖同日已有报告；做格式演示请优先用 `generate_sample_report.py`。
- 去重状态：`reports/.seen_urls.json`（gitignore，勿提交）。
- GitHub Actions 工作流：`.github/workflows/daily-market-scan.yml`（cron UTC 08:00 或手动 `workflow_dispatch`）。

### AI 技能 E2E

安装示例（见 README）：`cp -r . ~/.codex/skills/ai-opportunity-scanner`（或按仓库实际技能目录名调整）。在 Kimi/Codex CLI 中触发行业分析即可；输出应遵循 `assets/opportunity-matrix-template.md`。

### 密钥

搜索 API 密钥通过环境变量注入（`BRAVE_API_KEY`、`GOOGLE_API_KEY`+`GOOGLE_CSE_ID`、`SERPAPI_KEY`、`NEWSAPI_KEY`）。本地与 Cloud Agent 需用户/Secrets 配置；未配置时只能用示例报告流程验证环境。
