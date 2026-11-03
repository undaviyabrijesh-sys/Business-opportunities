# Data source registry

Status: entrypoint and official documentation researched. No adapter is production-ready until access rules, schema, cadence, licensing and historical reproducibility are tested.

## India — priority sources

| Source | Data | Opportunity use | Integration |
|---|---|---|---|
| [OGD Platform India](https://data.gov.in/) | Central/state datasets and catalogue APIs | Government-data discovery | Catalogue search; documented API/resource downloads |
| [AGMARKNET daily mandi prices via OGD](https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi) | Daily commodity/market/variety prices, arrivals, min/modal/max | Geographic price spreads, sourcing and seasonality | OGD API/CSV; normalize grade, unit and market identifiers |
| [Department of Commerce Trade Intelligence & Analytics](https://trade-analytics.commerce.gov.in/public/indiaTrade) | India trade by HS code and partner, sourced from DGCI&S | Import dependence, export growth and destination selection | Portal exports/data extraction; version HS classification |
| [TradeStat monthly statistics](https://tradestat.commerce.gov.in/ftspcc/ttrade_country_wise) | Monthly commodity/country/region trade | Product-country screening | Official portal tables/downloads |
| [IMD API portal](https://api.imd.gov.in/public/) and [reference](https://api.imd.gov.in/public/api_reference.html) | Forecasts, current observations, warnings, rainfall, port/highway warnings, agromet advisories | Weather/crop/logistics disruption | Official API; check account/access requirements |
| [Central Public Procurement Portal](https://eprocure.gov.in/eprocure/app) | Active tenders, corrigenda, awards | Institutional buyer demand | Public tender pages/downloads; no CAPTCHA bypass |
| [GeM bids](https://bidplus.gem.gov.in/all-bids) | Government marketplace bids | Public-sector procurement | Public bid pages; confirm reuse terms |
| [MoSPI eSankhyiki](https://esankhyiki.mospi.gov.in/catalogue-main/catalogue) | IIP and official statistics | Industrial activity proxy | Catalogue/downloads |
| [RBI DBIE](https://dbie.rbi.org.in/) | FX, financial and macro time series | Currency and macro risk | Official downloads where available |
| [APEDA AgriExchange](https://agriexchange.apeda.gov.in/Home/) | Export trends, destination/product info, buy/sell leads, exporter directory and market guidance | Agricultural and processed-food exports | Portal reporting and leads; verify counterparts |
| [DGFT](https://www.dgft.gov.in/) | Foreign trade policy and notifications | Import/export restrictions and licensing | Official notifications; date-stamp policy |
| [PIB RSS](https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1) | Official press releases | Policy, investment and sector signals | RSS |
| [FSSAI](https://www.fssai.gov.in/), [BIS](https://www.bis.gov.in/), [CPCB](https://cpcb.nic.in/) | Product standards and regulatory updates | Compliance risk | Official notices and standards |

## Global sources

| Source | Data | Opportunity use | Integration |
|---|---|---|---|
| [UN Comtrade](https://comtrade.un.org/) | Monthly/annual merchandise trade by product, reporter, partner | Import demand, export supply, competition | Official API; free-preview/subscription limits |
| [World Bank Commodity Markets / Pink Sheet](https://www.worldbank.org/en/research/commodity-markets) | Historical commodity prices and outlook | Benchmarking and commodity risk | XLSX/CSV/PDF; separate observations from forecasts |
| [FAOSTAT](https://www.fao.org/faostat/en/#data) | Production, agriculture trade, food balance and prices | Agri fundamentals | Bulk/API; store release vintage |
| [Eurostat REST API](https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-introduction) | EU trade/economic datasets | EU importer demand | REST API + metadata |
| [World Bank Climate Knowledge Portal](https://climateknowledgeportal.worldbank.org/) | Historical and projected climate | Long-term climate exposure, not short-term weather | Keep projections separate |
| [NOAA Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) | Historical climate observations | Weather anomaly and seasonality | API token + coverage metadata |

## News and trend intelligence

Use news as a leading indicator, not proof of demand. Start with official PIB RSS, ministry/regulator announcements, company filings and reputable news metadata. Product-keyword news search is discovery-only. Save publisher, date, canonical URL, product/HS tags, geography and event type; deduplicate syndicated headlines.

## Research verification notes — 3 November 2026

- OGD's AGMARKNET daily mandi-price resource showed a recent update on 28 October 2026 and is attributed to the Directorate of Marketing & Inspection.
- Department of Commerce TIA reports HS-code/partner coverage and attributes trade data to DGCI&S.
- IMD's current API reference lists city forecasts, current weather, district warnings/nowcasts, rainfall, port/highway warnings and agromet advisories.
- CPPP exposes active tenders, corrigenda, bid awards, search by location/organisation/classification and tender dates.
- APEDA AgriExchange includes export statistics, buy leads, sell leads, exporter directory and market insights.
- UN Comtrade API supports preview and subscribed access with different limits.
- World Bank's October 2026 commodity page provides monthly prices and forecasts; forecasts must not be labelled realized prices.
- MoSPI IIP is an industrial production indicator, not a direct measure of sales.

## Data governance

Each record stores source_id, source_url, retrieved_at_utc, published_at, valid_from/to, original identifier, geography, product/HS code and nomenclature version, value, currency, unit, raw payload/checksum, quality status, revision/vintage and transformation version.

Never compare price data until grade, quality, packaging, unit, currency, date basis and market level (farmgate/mandi/wholesale/retail) are compatible. Do not merge HS revisions without explicit concordance. Verify source terms, rate limits, API key requirements, caching and redistribution rights before commercial use.
