# Data source registry

Status: official entrypoints researched. An adapter is not production-ready until access rules, schema, cadence, licensing and reproducibility are tested.

## India

| Source | Data and use | Integration approach |
|---|---|---|
| [OGD Platform India](https://data.gov.in/) | Government datasets and APIs | Catalogue and documented API/download |
| [AGMARKNET daily mandi prices](https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi) | Daily commodity/market/variety price and arrivals; domestic price spread | Implemented adapter: resource 9ef84268-d588-465a-a308-a864a43d0070; requires OGD_API_KEY; exact commodity filter; normalize grade, unit and market |
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


## International market intelligence portals

These portals are added to the Streamlit **International intelligence** tab as product-research destinations. They are currently outbound research links, not automated data connectors. Users should retain the query, exact product description, HS code/revision, country pair, access date and source citation when recording findings.

| Portal | Primary use | Current integration status / caveat |
|---|---|---|
| [CBI Market Information](https://www.cbi.eu/market-information) | Sector/product market studies, European market trends, buyer requirements, standards and market-entry guidance | Research portal link only. CBI covers selected sectors and does not broker trade or provide importer lists. |
| [Global Trade Helpdesk](https://globaltradehelpdesk.org/) | Product and country trade opportunities, import demand, tariffs, regulations and partner discovery | Research portal link only. Data depth varies by country and product; no API ingestion claimed. |
| [ITC Trade Map](https://www.trademap.org/Index.aspx) | Monthly/quarterly/annual trade values, quantities, growth, market shares, competing markets and company directory | Research portal link only. Access/registration and data availability can vary. Check direct versus mirror data and units. |
| [ITC Export Potential Map](https://exportpotential.intracen.org/en/) | Modelled export potential and unrealised potential by product, exporter and destination | Research portal link only. Modelled potential is not a sales forecast or confirmed demand. |
| [ITC Market Analysis Tools](https://marketanalysis.intracen.org/en) | Landing page for Trade Map, Export Potential Map, Market Access Map and related tools | Research portal link only; some features may require registration or have access limits. |
| [European Commission Access2Markets](https://trade.ec.europa.eu/access-to-markets/en/home) | Tariffs, taxes, rules of origin, customs procedures, product requirements and trade barriers | Research portal link only. Especially useful for EU market access; select origin, destination and product accurately. |
| [India Trade Connect](https://www.trade.gov.in/) | India exporter support, market access information, export trends, FTA benefits and institutional connections | Research portal link only. Login/registration may be required for some services. |

### Research governance

- Never treat a portal's export-potential estimate as a confirmed order, buyer commitment or achievable revenue.
- Never treat company directory entries or buyer leads as vetted counterparties. Independently verify legal identity, operating status, references, sanctions exposure, payment terms and credit risk.
- Compare exact product form, grade, packaging, HS revision, reporting period, quantity unit, currency and valuation basis before combining statistics.
- These portals are not yet programmatic feeds. Do not claim live synchronization until an official API/download workflow has been implemented, tested and source terms reviewed.

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


## Implemented live-data adapters — 3 Nov 2026

- AGMARKNET is queried from the data.gov.in resource API. The dataset publishes daily wholesale minimum, maximum and modal prices; its resource page showed an update on 31 Oct 2026 when checked. API credentials are required. The app does not label records live until a successful source response is returned.
- UN Comtrade is queried by India reporter, World partner, HS code, trade flow and annual period. Public preview has a 500-record limit and permits one period per request; the adapter splits year lists into individual preview requests. Authenticated access uses the subscription endpoint.
- Catalogue HS codes remain candidates. The UI requires explicit confirmation before querying trade statistics.
- Configure OGD_API_KEY and optionally COMTRADE_API_KEY in Streamlit deployment Secrets or environment variables. Never commit credentials.
- A mandi-price spread is only a screening lead. Grade, variety, moisture, date, transport, fees and market accessibility must be normalized before a trade decision.


## Product-specific international intelligence — implementation update

- The Streamlit International intelligence tab now queries UN Comtrade for product imports across all reporting countries (reporter=ALL, partner=World) and India exports for a user-confirmed HS code.
- Results are normalized with reporter, partner, period, trade flow, trade value, quantity and retrieval timestamp. The dashboard ranks the top importing markets for the latest returned year.
- Public Comtrade preview is limited to 500 records per annual period. All-reporter results can therefore be incomplete; the UI labels the cap and does not interpret missing countries as zero demand.
- Product-related CBI/ITC/Global Trade Helpdesk research articles are discovered through Google News RSS site queries. This is an indexed-search discovery layer, not a direct API or guarantee that every official report is indexed.
- Access2Markets and portal-specific searches remain product-keyword search links until an official structured API or permitted downloadable dataset is available.
