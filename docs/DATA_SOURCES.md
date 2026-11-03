# Data source registry

Status means research/entrypoint verification, not completed automated ingestion. An adapter must be tested for licensing, schema stability, coverage, update cadence and reproducibility before it is treated as production-ready.

## India — priority sources

| Source | What it provides | Business use | Integration approach | Priority |
|---|---|---|---|---|
| [OGD Platform India](https://data.gov.in/) | Government datasets and catalogued APIs | Common discovery layer for agriculture, economy, environment, infrastructure, MSMEs | Search catalog; use documented API/resource downloads and API keys where required | P0 |
| [AGMARKNET / OGD daily mandi prices](https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi) | Daily commodity, market, variety, arrivals and min/modal/max price fields | Find regional price gaps, sourcing markets, destination markets and seasonality | OGD resource API/CSV; validate schema and commodity/unit mapping | P0 |
| [Department of Commerce Trade Intelligence & Analytics](https://trade-analytics.commerce.gov.in/public/indiaTrade) | India exports/imports by HS commodity and partner, sourced from DGCI&S | Identify import dependence, export growth, destination markets and partner concentration | Portal exports / documented data extraction; preserve HS code version | P0 |
| [TradeStat — monthly trade](https://tradestat.commerce.gov.in/ftspcc/ttrade_country_wise) | Monthly country/region and commodity foreign-trade statistics | Product-country screening and trend analysis | Portal tables/downloads; automate only via supported public interface | P0 |
| [TradeStat — export commodity view](https://tradestat.commerce.gov.in/eidb/commodity_wise_export) | Annual commodity-wise trade statistics | HS code ranking, value/quantity trend | Portal tables/downloads | P0 |
| [IMD API Management](https://api.imd.gov.in/public/) | Weather observations, forecasts, warnings and specialized bulletins | Crop/output disruptions, heat/rain risk, demand changes, logistics disruption | Register for access; use documented APIs; store issue time and validity window | P0 |
| [Central Public Procurement Portal](https://eprocure.gov.in/) | Government tenders, awards and procurement notices | Detect institutional demand and buyer leads | Prefer published tender feeds/downloads; capture closing date, buyer, item, quantity and eligibility | P0 |
| [GeM bids](https://bidplus.gem.gov.in/all-bids) | Government e-marketplace bid notices | Find government demand, product specifications and procurement buyers | Public bid pages; check terms and access restrictions before ingestion | P0 |
| [MoSPI eSankhyiki](https://esankhyiki.mospi.gov.in/catalogue-main/catalogue) | Official statistics including IIP and national accounts datasets | Industrial demand proxies, manufacturing activity and sector expansion | Catalog downloads / available machine-readable formats | P1 |
| [RBI DBIE](https://dbie.rbi.org.in/) | Banking, financial and macroeconomic time series | FX, rates, credit and macro risk context | Download/API where available; document series and frequency | P1 |
| [APEDA](https://apeda.gov.in/) | Agricultural and processed food export information, market and product guidance | Export readiness, product-country opportunity discovery | Reports, dashboard and available datasets; verify reuse rights | P1 |
| [Spices Board India](https://www.indianspices.com/) | Spices trade, export and market information | Spices sourcing/export opportunities | Official reports and data downloads | P1 |
| [DPIIT Startup India — procurement](https://www.startupindia.gov.in/content/sih/en/public_procurement.html) | Procurement guidance and startup participation rules | Understand tender eligibility and startup relaxations | Reference/guidance, not primary transaction data | P2 |

## Global sources

| Source | What it provides | Business use | Integration approach | Priority |
|---|---|---|---|---|
| [UN Comtrade](https://comtrade.un.org/) | Annual/monthly merchandise trade by reporter, partner and product; API | Discover importing countries, export suppliers, trade growth and concentration | Use official API; respect free-tier limits and subscription terms | P0 |
| [World Bank Commodity Markets / Pink Sheet](https://www.worldbank.org/en/research/commodity-markets) | Historical and outlook commodity prices | Benchmark costs, price cycles and commodity risk | Download official XLSX/CSV/PDF; store revision date | P0 |
| [FAOSTAT](https://www.fao.org/faostat/en/#data) | Agriculture, production, trade, food balances and prices | Crop supply/demand fundamentals and food commodity markets | FAOSTAT bulk/API services; document release vintage | P1 |
| [Eurostat API](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access) | EU trade and economic datasets via REST API | EU importer demand and market entry screening | REST API, dataset metadata and filters | P1 |
| [World Bank Climate Change Knowledge Portal](https://climateknowledgeportal.worldbank.org/) | Historical and projected climate information | Long-horizon climate/production risk | Download/API where supported; never mix projections with weather forecasts | P1 |
| [NOAA Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) | Global historical climate observations and API | Historical weather anomalies and seasonality | API token; archive station/coverage metadata | P2 |

## News and trend intelligence

News is a leading indicator, not proof of demand. Start with official ministry/department press releases, regulator notices, company filings and reputable news metadata. Store headline, publisher, publication time, canonical URL, named entities, geography, product/HS-code tags and extracted claims. Deduplicate syndicated stories and keep the original link.

Potential official discovery points:
- [PIB](https://pib.gov.in/) — Government of India announcements.
- [Ministry of Commerce](https://www.commerce.gov.in/) — trade policy, export/import and schemes.
- [DGFT](https://www.dgft.gov.in/) — foreign-trade policy, notifications and trade facilitation.
- [FSSAI](https://www.fssai.gov.in/) — food compliance and regulatory changes.
- [BIS](https://www.bis.gov.in/) — standards and mandatory certification information.
- [CPCB](https://cpcb.nic.in/) — environmental regulation and pollution data.

## Data governance requirements

Every record should carry:
- source_id, source_url, retrieved_at_utc, published_at, valid_from, valid_to (when applicable)
- source_record_id / original identifier
- geography codes and original geographic label
- product_id, HS code and HS nomenclature/version where applicable
- value, currency, unit and conversion method
- raw payload reference or archived file checksum
- data quality status, revision/vintage and transformation version

Never compare prices until grade, quality, packaging, currency, quantity unit, market level (farmgate/mandi/wholesale/retail), tax treatment and date basis are compatible.

## Verified research notes (3 Nov 2026)

- OGD lists the daily mandi prices resource as updated on 28 Oct 2026 when checked. The underlying dataset is sourced through the Directorate of Marketing & Inspection and AGMARKNET.
- Department of Commerce TIA reports HS8 and trading-partner coverage, with source attribution to DGCI&S; the portal displayed coverage through Aug 2026 at the time of review.
- TradeStat's monthly foreign-trade view showed data through Sep 2026 and an update date of 28 Oct 2026.
- IMD provides an official API Management Platform for real-time observations, forecasts, warnings and specialized bulletins.
- NIC describes CPPP as a procurement platform with active tenders, global tenders and award details.
- UN Comtrade provides product/partner trade data and API access, subject to access limits.
- World Bank publishes commodity price series and outlooks; distinguish observed historical prices from forecast scenarios.
- MoSPI's eSankhyiki catalogue exposes monthly IIP information; IIP is an industrial production indicator, not a direct sales measure.

Use source publications for final claims and cite the original source in the product UI.
