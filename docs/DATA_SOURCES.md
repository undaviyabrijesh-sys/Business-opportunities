# Data source registry

Status: official entrypoints researched. An adapter is not production-ready until access rules, schema, cadence, licensing and reproducibility are tested.

## India

| Source | Data and use | Integration approach |
|---|---|---|
| [OGD Platform India](https://data.gov.in/) | Government datasets and APIs | Catalogue and documented API/download |
| [AGMARKNET daily mandi prices](https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi) | Daily commodity/market/variety price and arrivals; domestic price spread | OGD API/CSV; normalize grade, unit and market |
| [Commerce TIA](https://trade-analytics.commerce.gov.in/public/indiaTrade) | India trade by HS code and partner, sourced from DGCI&S | Official portal data extraction; retain HS version |
| [TradeStat](https://tradestat.commerce.gov.in/ftspcc/ttrade_country_wise) | Monthly trade statistics | Official portal tables/downloads |
| [IMD API portal](https://api.imd.gov.in/public/) and [reference](https://api.imd.gov.in/public/api_reference.html) | Forecasts, current observations, warnings, rainfall, port/highway warnings and agromet advisories | Official API; review access requirements |
| [CPPP eProcurement](https://eprocure.gov.in/eprocure/app) | Active tenders, corrigenda, bid awards | Public notices/downloads; no CAPTCHA bypass |
| [GeM bids](https://bidplus.gem.gov.in/all-bids) | Government marketplace bids | Public pages; verify reuse terms |
| [MoSPI eSankhyiki](https://esankhyiki.mospi.gov.in/catalogue-main/catalogue) | IIP and official statistics | Catalogue/downloads; IIP is a production proxy |
| [RBI DBIE](https://dbie.rbi.org.in/) | FX, banking and macro time series | Official downloads where available |
| [APEDA AgriExchange](https://agriexchange.apeda.gov.in/Home/) | Export stats, destination/product market info, exporter directory, buyer/seller leads | Portal reporting and leads; independently verify counterparties |
| [DGFT](https://www.dgft.gov.in/) | Foreign trade policy and notifications | Official notification monitoring |
| [PIB RSS](https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1) | Official releases for policy/investment/sector news | RSS |
| [FSSAI](https://www.fssai.gov.in/), [BIS](https://www.bis.gov.in/), [CPCB](https://cpcb.nic.in/) | Product standards and compliance | Official updates |

## Global

| Source | Data and use | Integration approach |
|---|---|---|
| [UN Comtrade](https://comtrade.un.org/) | Monthly/annual trade by product, reporter and partner | Official API; preview/subscription limits |
| [World Bank Pink Sheet](https://www.worldbank.org/en/research/commodity-markets) | Commodity price observations and outlook | XLSX/CSV/PDF; separate forecasts from realized data |
| [FAOSTAT](https://www.fao.org/faostat/en/#data) | Agricultural production, trade and food balances | Bulk/API; store revision vintage |
| [Eurostat API](https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-introduction) | EU trade and economic statistics | REST API and metadata |
| [World Bank Climate Portal](https://climateknowledgeportal.worldbank.org/) | Long-term climate history/projections | Clearly separate projections from weather |
| [NOAA Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) | Historical climate observations | API token and station metadata |

## News and trends

Official PIB RSS, ministry/regulator notices, company filings and reputable media metadata. Item-keyword news feeds are discovery only, not proof of demand. Preserve publisher, date, canonical URL, product/HS tags and geography; deduplicate syndication.

## Research notes — 3 Nov 2026

- OGD's AGMARKNET daily mandi-price resource showed a recent update dated 28 Oct 2026.
- Commerce TIA publishes HS/partner trade data attributed to DGCI&S.
- IMD API reference lists city forecasts, current weather, district nowcast/warnings, rainfall, port/highway warnings and agromet advisories.
- CPPP shows active tenders, corrigenda, awards and search by item, organisation, location, value and dates.
- APEDA AgriExchange provides export stats, buyer/seller leads, exporter directory and market insights.
- UN Comtrade has preview and subscription endpoints with different limits.
- World Bank's October 2026 page publishes monthly commodity prices and forecasts. Do not mix the two.
- IIP is industrial production, not direct evidence of product sales.

## Governance

Preserve source URL, retrieval/publication times, valid dates, source identifier, geography, product/HS code and nomenclature version, value/currency/unit, raw payload checksum, quality status, source vintage and transformation version.

Never compare prices before grade, quality, packaging, units, currency, date and market-level normalization. Do not merge HS revisions without a concordance. Check source terms, rate limits, credentials, caching and redistribution before commercial use.
