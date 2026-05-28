#!/usr/bin/env python3
"""
生成示例报告 —— 无需 API key，用于验证报告格式和流程。
运行: python scripts/generate_sample_report.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_scanner import (
    MarketLead,
    generate_report,
    load_config,
    save_report,
)

SAMPLE_LEADS = [
    MarketLead(
        title="US DOE Issues RFQ for 200MWh Grid-Scale Battery Storage Cells",
        url="https://example.com/doe-rfq-battery",
        snippet="The U.S. Department of Energy seeks proposals for LFP battery cells for grid-scale BESS projects across 5 states.",
        source="sam.gov",
        product_category="energy_storage_cells",
        product_label="储能电芯",
        region="north_america",
        region_label="北美市场",
        country="United States",
        country_label="美国",
        relevance_score=0.65,
    ),
    MarketLead(
        title="European Commission Tender: PCS for Cross-Border Energy Storage",
        url="https://example.com/eu-pcs-tender",
        snippet="Tender notice for 50MW power conversion systems for the EU-funded BESS interconnection pilot.",
        source="ted.europa.eu",
        product_category="pcs",
        product_label="PCS (储能变流器)",
        region="europe",
        region_label="欧洲市场",
        country="Germany",
        country_label="德国",
        relevance_score=0.55,
    ),
    MarketLead(
        title="UK National Grid: Battery Cabinet System Procurement",
        url="https://example.com/uk-cabinet",
        snippet="National Grid ESO looking for containerized battery storage cabinet suppliers for frequency response projects.",
        source="nationalgrid.com",
        product_category="energy_storage_cabinet",
        product_label="储能柜",
        region="europe",
        region_label="欧洲市场",
        country="United Kingdom",
        country_label="英国",
        relevance_score=0.50,
    ),
    MarketLead(
        title="Canada Alberta Solar Panel Bulk Purchase for Community Solar Program",
        url="https://example.com/canada-solar",
        snippet="Alberta government seeking solar module suppliers for 150MW community solar program procurement.",
        source="merx.com",
        product_category="solar_panels",
        product_label="太阳能板",
        region="north_america",
        region_label="北美市场",
        country="Canada",
        country_label="加拿大",
        relevance_score=0.45,
    ),
    MarketLead(
        title="Spain Issues Tender for Utility-Scale Solar PV Modules",
        url="https://example.com/spain-solar",
        snippet="Spanish Ministry of Energy procurement for 500MW PV module supply for national renewable targets.",
        source="boe.es",
        product_category="solar_panels",
        product_label="太阳能板",
        region="europe",
        region_label="欧洲市场",
        country="Spain",
        country_label="西班牙",
        relevance_score=0.40,
    ),
    MarketLead(
        title="German BESS Developer Seeks LFP Cell Manufacturer",
        url="https://example.com/de-lfp",
        snippet="Leading German energy storage developer seeking long-term supply agreement for 280Ah LFP cells.",
        source="energy-storage.news",
        product_category="energy_storage_cells",
        product_label="储能电芯",
        region="europe",
        region_label="欧洲市场",
        country="Germany",
        country_label="德国",
        relevance_score=0.60,
    ),
    MarketLead(
        title="Netherlands C&I Storage Cabinet RFP",
        url="https://example.com/nl-cabinet",
        snippet="Dutch commercial energy storage integrator issues RFP for indoor battery cabinet systems with integrated BMS.",
        source="tendersonline.nl",
        product_category="energy_storage_cabinet",
        product_label="储能柜",
        region="europe",
        region_label="欧洲市场",
        country="Netherlands",
        country_label="荷兰",
        relevance_score=0.35,
    ),
    MarketLead(
        title="US Utility Issues PCS Procurement for Solar+Storage Projects",
        url="https://example.com/us-pcs",
        snippet="Major US utility seeking bidirectional PCS inverter solutions for 12 co-located solar-plus-storage sites.",
        source="utilitydive.com",
        product_category="pcs",
        product_label="PCS (储能变流器)",
        region="north_america",
        region_label="北美市场",
        country="United States",
        country_label="美国",
        relevance_score=0.50,
    ),
]


def main():
    config = load_config()
    report = generate_report(SAMPLE_LEADS, config)
    path = save_report(report)
    print(f"示例报告已生成: {path}")
    print("\n" + "=" * 40 + " 预览 " + "=" * 40)
    print(report[:2000])
    print("...\n(报告已截断，完整内容请查看文件)")


if __name__ == "__main__":
    main()
