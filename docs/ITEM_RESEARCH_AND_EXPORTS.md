# Item research, weather, news and export/tender workflows

## Item-first search

A user can enter a free-text item name (for example, "turmeric powder", "pharmaceutical-grade lactose", "aluminium extrusion" or "coconut coir pith"). The search process:

1. Normalize aliases and identify likely product category.
2. Suggest HS code(s) with a confidence and classification version. Do not guess one HS code silently for broad or multi-use products.
3. Assemble a dossier: India production/sourcing regions, mandi or benchmark prices when relevant, Indian import/export history, top trade partners, global import demand, seasonality, relevant industrial indicators and current policy restrictions.
4. Attach current weather/forecast/warnings to relevant production regions and transport corridors.
5. Find related headlines and official announcements, clearly separating news from measured demand.
6. Search tender and buyer/seller lead sources.
7. Show next validation tasks, not a claim that the item will make money.

## Weather

Primary Indian source: [IMD API portal](https://api.imd.gov.in/public/) and [official API reference](https://api.imd.gov.in/public/api_reference.html). The reference lists city 7-day forecasts, forecasts by latitude/longitude, current weather, district nowcasts, district warnings, rainfall, port warnings, highway warnings and agromet advisories.

Weather needs a geographic context. Product search should ask for or infer candidate production and logistics locations from reliable product/market evidence, then show:
- forecast issued time and validity range;
- temperature/rainfall/wind fields with units;
- warning level and source;
- exposed location and reason it matters (crop production, warehousing, port or road);
- whether the signal is short-term forecast, observation or long-term climate projection.

Do not infer a price move directly from a forecast. Show potential operational impact and require corroborating production, transport or market evidence.

## News and emerging trends

- Official India releases: [PIB RSS](https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1).
- Market coverage: product-keyword RSS searches from Google News can be used as discovery only. Deduplicate by canonical URL/title and preserve publisher/date. Add independent reputable sources and company filings over time.
- Tag items by product aliases, HS code, country, sector and event type (capacity expansion, investment, subsidy, ban/restriction, tariff, procurement, shortage, recall, weather disruption).
- Summarize as a hypothesis with supporting/contradicting sources. News volume is not measured sales or a verified buyer order.

## Export opportunity research

For each selected product:
- India export trend and destinations from [Department of Commerce TIA](https://trade-analytics.commerce.gov.in/public/indiaTrade).
- Agriculture/processed food export statistics and market intelligence from [APEDA AgriExchange](https://agriexchange.apeda.gov.in/Home/), including buyer leads, seller leads and exporter directory.
- Global country import demand and supplier competition from [UN Comtrade](https://comtrade.un.org/).
- Global commodity price benchmarks from [World Bank Pink Sheet](https://www.worldbank.org/en/research/commodity-markets).
- Export control/eligibility notifications from [DGFT](https://www.dgft.gov.in/) and product regulators such as FSSAI/BIS where relevant.

An export shortlist should display import value/volume trend, supplier countries, India export trend, unit values (not interpreted as transaction prices), market growth, concentration, tariff/NTM research tasks, logistics/port fit, currency and quality standards. Validate each product's precise HS code and destination market rules.

## Tenders and buyer leads

- [CPPP eProcurement](https://eprocure.gov.in/eprocure/app) lists active tenders, corrigenda and bid awards; latest tender updates are displayed on the official portal. Its advanced search includes work/item title, organisation, department, product category, location, value and dates. Search may require CAPTCHA and bidder registration/DSC for submission; do not bypass access controls.
- [GeM bids](https://bidplus.gem.gov.in/all-bids) is another government procurement discovery point.
- [APEDA buyer leads](https://agriexchange.apeda.gov.in/Buyer/MyBuyOffers) and [seller leads](https://agriexchange.apeda.gov.in/Seller/SellLead) are useful for agricultural/processed-food counterparties. Leads are user submitted; credentials must be independently verified.
- For non-agri exports, later connector sources should include relevant Export Promotion Councils, trade fair/exhibitor directories, public importer registries and paid trade-data providers where legally licensed.

Tender records should include title, tender ID/reference, buyer organisation, item/specification, quantity, estimated value (if published), location, publication date, closing date/time/timezone, EMD, eligibility, document link, corrigenda, award status and source timestamp. Highlight closing deadlines and corrigenda.

## Important limitations

- CPPP advanced search includes CAPTCHA; no CAPTCHA bypass or unauthorised scraping.
- APEDA says buyer/seller leads are supplied by third parties and users should verify counterparties.
- TIA/TradeStat pages may expose portal exports rather than a stable public API. Use verified downloads and preserve source vintage.
- Weather and news explain possible disruptions/signals; they do not alone prove a profitable trade.
