# Item research, weather, news and export/tender workflows

## Item-first search

A user enters any product name (e.g. "turmeric powder", "pharmaceutical-grade lactose", "aluminium extrusion" or "coconut coir pith"). Search should:

1. Normalize aliases and identify category.
2. Suggest plausible HS codes with confidence and classification version. Never silently force one HS code onto an ambiguous product.
3. Assemble Indian production/sourcing regions, mandi/benchmark prices when relevant, import/export history, top trade partners, global import demand, seasonality and industrial indicators.
4. Attach current weather and warnings to evidence-backed production and logistics locations.
5. Find related headlines and official announcements, separating news from measured demand.
6. Find export-market options, buyer/seller leads and relevant tenders.
7. Build next validation tasks; do not claim that an item will make money.

## Weather

Primary source: [IMD API portal](https://api.imd.gov.in/public/) and [API reference](https://api.imd.gov.in/public/api_reference.html). The official reference lists city 7-day forecasts, location-based forecasts, current weather, district nowcasts/warnings, rainfall, port warnings, highway warnings and agromet advisories.

The dashboard must show forecast issued time, validity, location, units, warning severity, source link and why the place is relevant (production region, warehouse, port or route). Distinguish observations, short-term forecasts and climate projections. A forecast is an operational risk signal, not proof of a price move.

## News and trends

- Government releases: [PIB RSS](https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1).
- Product news: Google News RSS search is discovery-only; preserve publisher/date/link and seek corroboration.
- Tag by aliases, HS, country, sector and event type (capacity expansion, investment, subsidy, restriction, tariff, procurement, shortage, recall, weather disruption).
- Summaries are hypotheses supported by links, not proof of orders or sales.

## Export opportunity dossier

For every product:
- India export trend/destinations: [Commerce TIA](https://trade-analytics.commerce.gov.in/public/indiaTrade).
- Agri/processed food export stats, exporter directory and buyer/seller leads: [APEDA AgriExchange](https://agriexchange.apeda.gov.in/Home/).
- Global importer demand and supplier competition: [UN Comtrade](https://comtrade.un.org/).
- Commodity benchmark: [World Bank Pink Sheet](https://www.worldbank.org/en/research/commodity-markets).
- Export control and licensing: [DGFT](https://www.dgft.gov.in/) plus FSSAI/BIS or sector regulators.

Rank destinations using import value/volume trend, supplier mix, Indian export trend, unit values (not transaction prices), tariff/NTM research, logistics fit, currency, product standards and market concentration. Confirm correct HS code and destination rules before recommending a route.

## Tenders and leads

- [CPPP eProcurement](https://eprocure.gov.in/eprocure/app): active tenders, corrigenda, bid awards and searches by item title, organisation, location, value and date. Advanced search may require CAPTCHA; no bypass. Bidding can require registration and a Digital Signature Certificate.
- [GeM bids](https://bidplus.gem.gov.in/all-bids): public procurement discovery.
- [APEDA buyer leads](https://agriexchange.apeda.gov.in/Buyer/MyBuyOffers) and [seller leads](https://agriexchange.apeda.gov.in/Seller/SellLead): useful for agri/processed-food counterparties. APEDA notes leads are user-submitted and must be verified.
- Other sectors: add relevant Export Promotion Councils, public trade fair directories, lawful public importer registries and licensed trade-data services.

Tender schema: title, tender ID/reference, buyer, item/specification, quantity, estimated value if published, location, publish/close dates and timezone, EMD, eligibility, documents, corrigenda, award state, source timestamp. Alert on closing dates and modifications.

## Limitations

CPPP CAPTCHA must not be bypassed. APEDA leads are not guaranteed or pre-verified. TIA/TradeStat may expose downloads rather than stable APIs. Weather/news explain possible signals but do not alone prove a profitable trade.
