# AGENTS.md

## Cursor Cloud specific instructions

### 仓库概览

本仓库包含两个独立产物，**均无长期运行的 Web 服务或监听端口**：

1. **AI Opportunity Scanner** — Kimi Code CLI / Codex 技能（`SKILL.md`、`references/`、`assets/`）。在宿主 CLI 中安装后通过自然语言触发，本仓库内无独立进程可启动。
2. **Daily Energy Storage Market Scanner** — Python 批处理脚本（`scripts/market_scanner.py`），通过外部搜索 API 生成 `reports/market-report-YYYY-MM-DD.md`。

### 依赖与更新

- **运行时**：Python 3.12+、`pip install -r requirements.txt`（`requests`、`pyyaml`）。
- **无** npm、Docker Compose、数据库、Redis，也**无**项目级 lint/test 配置（无 pytest、ruff、pre-commit）。

### 常用命令（从仓库根目录执行）

| 目的 | 命令 |
|------|------|
| 离线验证报告流水线（无需 API key） | `python3 scripts/generate_sample_report.py` |
| 实时市场扫描 | 设置至少一组搜索 API 环境变量后运行 `python3 scripts/market_scanner.py` |
| Python 语法检查（可选） | `python3 -m py_compile scripts/*.py` |

### 搜索 API 环境变量（实时扫描必需至少一组）

- 推荐：`BRAVE_API_KEY`
- 或：`GOOGLE_API_KEY` + `GOOGLE_CSE_ID`
- 或：`SERPAPI_KEY`
- 可选补充：`NEWSAPI_KEY`

未配置任何密钥时，`market_scanner.py` 会记录错误并生成 0 条线索的报告（退出码可能为 1）；**不代表 Python 环境未就绪**。

### 非显而易见的行为

- `scripts/generate_sample_report.py` 通过 `sys.path` 导入同目录的 `market_scanner` 模块，必须在仓库根目录或 `scripts/` 下以 `python3 scripts/...` 方式运行。
- 去重缓存写在 `reports/.seen_urls.json`（已 gitignore），重复运行 live 扫描会跳过已见 URL。
- GitHub Actions 工作流见 `.github/workflows/daily-market-scan.yml`；本地开发无需启动 Actions，只需能出站 HTTPS（live 扫描时）。
- 技能安装路径见 `README.md`（例如复制到 `~/.codex/skills/`），Cloud Agent VM 上通常只验证 Markdown 技能文件存在即可，不必安装 Kimi/Codex 才能完成扫描器相关任务。

### 标准文档

更完整的安装说明、API 注册链接与配置项见根目录 `README.md`。
