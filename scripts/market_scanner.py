#!/usr/bin/env python3
"""
海外储能/太阳能市场需求每日扫描工具

扫描北美和欧洲市场中与储能电芯、PCS、储能柜、太阳能板相关的
采购需求、招标信息和市场动态，生成结构化的中文市场报告。
"""

import json
import os
import re
import sys
import logging
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote_plus, urlencode
from dataclasses import dataclass, field, asdict
from typing import Optional

import requests
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "market_scan_config.yaml"
REPORT_DIR = ROOT_DIR / "reports"
DEDUP_PATH = REPORT_DIR / ".seen_urls.json"


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class MarketLead:
    title: str
    url: str
    snippet: str
    source: str
    product_category: str
    product_label: str
    region: str
    region_label: str
    country: str
    country_label: str
    published_date: str = ""
    relevance_score: float = 0.0

    @property
    def uid(self) -> str:
        return hashlib.md5(self.url.encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Search backends
# ---------------------------------------------------------------------------

COUNTRY_CODES = {
    "United States": "US",
    "Canada": "CA",
    "Germany": "DE",
    "United Kingdom": "GB",
    "France": "FR",
    "Spain": "ES",
    "Italy": "IT",
    "Netherlands": "NL",
    "Poland": "PL",
    "Sweden": "SE",
}


class BraveSearchBackend:
    """Brave Search API — recommended default (free tier: 2000 queries/month).

    Requires BRAVE_API_KEY. Supports both web search and news search endpoints.
    Docs: https://api-dashboard.search.brave.com/app/documentation/web-search
    """

    BASE_WEB = "https://api.search.brave.com/res/v1/web/search"
    BASE_NEWS = "https://api.search.brave.com/res/v1/news/search"

    def __init__(self):
        self.api_key = os.environ.get("BRAVE_API_KEY", "")
        if not self.api_key:
            log.warning("BRAVE_API_KEY not set – Brave Search backend disabled")

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key,
        }

    def search_web(self, query: str, country: str = "", count: int = 10) -> list[dict]:
        if not self.available:
            return []
        params = {
            "q": query,
            "count": min(count, 20),
            "freshness": "pw",
            "text_decorations": False,
            "search_lang": "en",
        }
        cc = COUNTRY_CODES.get(country, "")
        if cc:
            params["country"] = cc
        try:
            resp = requests.get(
                self.BASE_WEB,
                headers=self._headers(),
                params=params,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("url", ""),
                    "snippet": item.get("description", ""),
                    "publishedAt": item.get("page_age", ""),
                })
            return results
        except Exception as exc:
            log.error("Brave web search failed for '%s': %s", query, exc)
            return []

    def search_news(self, query: str, country: str = "", count: int = 10) -> list[dict]:
        if not self.available:
            return []
        params = {
            "q": query,
            "count": min(count, 20),
            "freshness": "pw",
            "search_lang": "en",
        }
        cc = COUNTRY_CODES.get(country, "")
        if cc:
            params["country"] = cc
        try:
            resp = requests.get(
                self.BASE_NEWS,
                headers=self._headers(),
                params=params,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in data.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("url", ""),
                    "snippet": item.get("description", ""),
                    "publishedAt": item.get("age", ""),
                })
            return results
        except Exception as exc:
            log.error("Brave news search failed for '%s': %s", query, exc)
            return []


class GoogleSearchBackend:
    """Google Custom Search JSON API (requires GOOGLE_API_KEY + GOOGLE_CSE_ID)."""

    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY", "")
        self.cse_id = os.environ.get("GOOGLE_CSE_ID", "")
        if not self.api_key or not self.cse_id:
            log.warning("GOOGLE_API_KEY / GOOGLE_CSE_ID not set – Google backend disabled")

    @property
    def available(self) -> bool:
        return bool(self.api_key and self.cse_id)

    def search(self, query: str, num: int = 10, date_restrict: str = "d7") -> list[dict]:
        if not self.available:
            return []
        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": query,
            "num": min(num, 10),
            "dateRestrict": date_restrict,
            "safe": "active",
        }
        try:
            resp = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params=params,
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json().get("items", [])
        except Exception as exc:
            log.error("Google search failed for '%s': %s", query, exc)
            return []


class SerpApiBackend:
    """SerpApi (requires SERPAPI_KEY)."""

    def __init__(self):
        self.api_key = os.environ.get("SERPAPI_KEY", "")
        if not self.api_key:
            log.warning("SERPAPI_KEY not set – SerpApi backend disabled")

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, num: int = 10) -> list[dict]:
        if not self.available:
            return []
        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": query,
            "num": num,
            "tbs": "qdr:w",
        }
        try:
            resp = requests.get(
                "https://serpapi.com/search",
                params=params,
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("organic_results", [])
        except Exception as exc:
            log.error("SerpApi search failed for '%s': %s", query, exc)
            return []


class NewsApiBackend:
    """NewsAPI.org (requires NEWSAPI_KEY)."""

    def __init__(self):
        self.api_key = os.environ.get("NEWSAPI_KEY", "")
        if not self.api_key:
            log.warning("NEWSAPI_KEY not set – NewsAPI backend disabled")

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, num: int = 10) -> list[dict]:
        if not self.available:
            return []
        from_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
        params = {
            "apiKey": self.api_key,
            "q": query,
            "from": from_date,
            "sortBy": "relevancy",
            "pageSize": num,
            "language": "en",
        }
        try:
            resp = requests.get(
                "https://newsapi.org/v2/everything",
                params=params,
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json().get("articles", [])
        except Exception as exc:
            log.error("NewsAPI search failed for '%s': %s", query, exc)
            return []


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def load_seen_urls() -> set[str]:
    if DEDUP_PATH.exists():
        try:
            data = json.loads(DEDUP_PATH.read_text(encoding="utf-8"))
            return set(data.get("urls", []))
        except Exception:
            pass
    return set()


def save_seen_urls(urls: set[str]):
    DEDUP_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEDUP_PATH.write_text(
        json.dumps({"urls": list(urls)[-5000:]}, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Relevance scoring
# ---------------------------------------------------------------------------

HIGH_SIGNAL_TERMS = [
    "tender", "rfq", "rfp", "procurement", "bid", "purchase order",
    "sourcing", "supplier wanted", "bulk order", "import",
    "looking for", "seeking", "needed", "required",
    "energy storage", "battery", "solar", "pv module",
    "pcs", "inverter", "bess", "ess",
    "lfp", "lithium", "photovoltaic",
]


def score_relevance(title: str, snippet: str) -> float:
    text = f"{title} {snippet}".lower()
    hits = sum(1 for term in HIGH_SIGNAL_TERMS if term in text)
    return min(hits / len(HIGH_SIGNAL_TERMS), 1.0)


# ---------------------------------------------------------------------------
# Core scanning logic
# ---------------------------------------------------------------------------

def run_scan(config: dict) -> list[MarketLead]:
    brave = BraveSearchBackend()
    google = GoogleSearchBackend()
    serpapi = SerpApiBackend()
    newsapi = NewsApiBackend()

    backends_available = sum([
        brave.available, google.available, serpapi.available, newsapi.available,
    ])
    if backends_available == 0:
        log.error(
            "No search backend is configured. "
            "Set at least one of: BRAVE_API_KEY (recommended), "
            "GOOGLE_API_KEY+GOOGLE_CSE_ID, SERPAPI_KEY, NEWSAPI_KEY"
        )
        return []

    seen = load_seen_urls()
    leads: list[MarketLead] = []
    products = config["products"]
    regions = config["regions"]

    for prod_key, prod_info in products.items():
        for region_key, region_info in regions.items():
            for country in region_info["countries"]:
                for term in prod_info["search_terms"][:4]:
                    query = f"{term} {country['name']}"
                    raw_results: list[dict] = []

                    if brave.available:
                        raw_results.extend(brave.search_web(query, country=country["name"], count=5))
                        raw_results.extend(brave.search_news(query, country=country["name"], count=3))
                    elif google.available:
                        raw_results.extend(google.search(query, num=5))
                    elif serpapi.available:
                        for r in serpapi.search(query, num=5):
                            raw_results.append({
                                "title": r.get("title", ""),
                                "link": r.get("link", ""),
                                "snippet": r.get("snippet", ""),
                            })

                    if newsapi.available:
                        for art in newsapi.search(query, num=3):
                            raw_results.append({
                                "title": art.get("title", ""),
                                "link": art.get("url", ""),
                                "snippet": art.get("description", ""),
                            })

                    for item in raw_results:
                        url = item.get("link", item.get("url", ""))
                        if not url or url in seen:
                            continue
                        title = item.get("title", "")
                        snippet = item.get("snippet", item.get("description", ""))
                        score = score_relevance(title, snippet)
                        if score < 0.05:
                            continue
                        seen.add(url)
                        leads.append(MarketLead(
                            title=title,
                            url=url,
                            snippet=snippet or "",
                            source=_extract_domain(url),
                            product_category=prod_key,
                            product_label=prod_info["label"],
                            region=region_key,
                            region_label=region_info["label"],
                            country=country["name"],
                            country_label=country["label"],
                            published_date=item.get("publishedAt", ""),
                            relevance_score=score,
                        ))

    save_seen_urls(seen)
    leads.sort(key=lambda x: x.relevance_score, reverse=True)
    log.info("Scan complete – found %d leads", len(leads))
    return leads


def _extract_domain(url: str) -> str:
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc
    except Exception:
        return url[:60]


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(leads: list[MarketLead], config: dict) -> str:
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y-%m-%d %H:%M UTC")

    products = config["products"]
    regions = config["regions"]

    lines = [
        f"# 海外储能/太阳能市场需求日报",
        f"",
        f"> 扫描时间: {time_str}",
        f"> 本次共发现 **{len(leads)}** 条相关线索",
        f"",
        f"---",
        f"",
    ]

    lines.append("## 概览统计\n")
    lines.append("| 产品类别 | 线索数 | 高相关度 (>0.3) |")
    lines.append("|----------|--------|-----------------|")
    for pk, pv in products.items():
        cat_leads = [l for l in leads if l.product_category == pk]
        high = len([l for l in cat_leads if l.relevance_score > 0.3])
        lines.append(f"| {pv['label']} | {len(cat_leads)} | {high} |")
    lines.append("")

    lines.append("| 市场区域 | 线索数 |")
    lines.append("|----------|--------|")
    for rk, rv in regions.items():
        region_leads = [l for l in leads if l.region == rk]
        lines.append(f"| {rv['label']} | {len(region_leads)} |")
    lines.append("")

    for pk, pv in products.items():
        cat_leads = [l for l in leads if l.product_category == pk]
        lines.append(f"---\n")
        lines.append(f"## {pv['label']}\n")
        if not cat_leads:
            lines.append("暂无新线索。\n")
            continue

        for region_key, region_info in regions.items():
            region_leads = [l for l in cat_leads if l.region == region_key]
            if not region_leads:
                continue
            lines.append(f"### {region_info['label']}\n")

            for country in region_info["countries"]:
                country_leads = [l for l in region_leads if l.country == country["name"]]
                if not country_leads:
                    continue
                lines.append(f"#### {country['label']} ({country['name']})\n")
                for i, lead in enumerate(country_leads[:10], 1):
                    score_bar = "🔴" if lead.relevance_score > 0.3 else "🟡" if lead.relevance_score > 0.15 else "⚪"
                    lines.append(f"{i}. {score_bar} **[{lead.title}]({lead.url})**")
                    lines.append(f"   - 来源: `{lead.source}`")
                    if lead.snippet:
                        lines.append(f"   - 摘要: {lead.snippet[:200]}")
                    if lead.published_date:
                        lines.append(f"   - 日期: {lead.published_date}")
                    lines.append("")

    lines.append("---\n")
    lines.append("## 建议操作\n")

    high_leads = [l for l in leads if l.relevance_score > 0.3]
    if high_leads:
        lines.append(f"- ✅ 共 **{len(high_leads)}** 条高相关度线索，建议优先跟进")
        by_product = {}
        for l in high_leads:
            by_product.setdefault(l.product_label, []).append(l)
        for pname, pleads in by_product.items():
            countries = set(l.country_label for l in pleads)
            lines.append(f"  - **{pname}**: {len(pleads)} 条 (涉及: {', '.join(countries)})")
    else:
        lines.append("- 本次扫描未发现高相关度线索，建议关注趋势变化")
    lines.append("")

    lines.append("---\n")
    lines.append(f"*本报告由 AI Opportunity Scanner 自动生成，数据仅供参考。*\n")

    return "\n".join(lines)


def save_report(content: str) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = REPORT_DIR / f"market-report-{date_str}.md"
    path.write_text(content, encoding="utf-8")
    log.info("Report saved to %s", path)
    return path


# ---------------------------------------------------------------------------
# Cleanup old reports
# ---------------------------------------------------------------------------

def cleanup_old_reports(keep_days: int = 90):
    cutoff = datetime.now(timezone.utc) - timedelta(days=keep_days)
    for p in REPORT_DIR.glob("market-report-*.md"):
        match = re.search(r"market-report-(\d{4}-\d{2}-\d{2})\.md", p.name)
        if match:
            try:
                report_date = datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if report_date < cutoff:
                    p.unlink()
                    log.info("Removed old report: %s", p.name)
            except ValueError:
                pass


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    log.info("=== 海外储能/太阳能市场需求扫描开始 ===")
    config = load_config()

    leads = run_scan(config)
    report = generate_report(leads, config)
    report_path = save_report(report)

    keep_days = config.get("report", {}).get("keep_days", 90)
    cleanup_old_reports(keep_days)

    print(f"\n{'='*60}")
    print(f"扫描完成! 共发现 {len(leads)} 条线索")
    print(f"报告已保存: {report_path}")
    print(f"{'='*60}\n")

    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(report)

    return 0 if leads else 1


if __name__ == "__main__":
    sys.exit(main())
