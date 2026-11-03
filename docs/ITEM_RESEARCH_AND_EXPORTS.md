# Item research, weather, news and export/tender workflows

## Item-first search

A user enters any product name (e.g. turmeric powder, pharmaceutical-grade lactose, aluminium extrusion or coconut coir pith). The system should:

1. Normalize aliases and identify product category.
2. Suggest plausible HS codes with confidence and classification version. Never silently force one HS code onto an ambiguous item.
3. Assemble Indian sourcing/production regions, mandi or benchmark prices where relevant, import/export history, top partners, global importer demand, seasonality and industrial indicators.
4. Attach current weather and warnings to relevant production and logistics locations.
5. Find related headlines and official announcements, separating news from measured demand.
6. Find export-market options, buyer/seller leads and relevant tenders.
7. Produce next validation tasks, not a claim that an item will make money.

## Weather

Primary source: [IMD API portal](https://api.imd.gov.in/public/) and [API reference](https://api.imd.gov.in/public/api_reference.html). The reference lists 7-day city forecasts, location-based forecasts, current weather, district nowcasts/warnings, rainfall, port warnings, highway warnings and agromet advisories.

Show forecast issue time, validity, location, units, warning severity, source link and why the location matters (production region, warehouse, port or route). Separate observations, short-term forecasts and long-term climate projections. A forecast is an operational risk signal, not proof of a price move.

## News and trends

- Official releases: [PIB RSS](https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1).
- Product news: RSS item searches are discovery-only; preserve publisher/date/link and corroborate.
- Tag aliases, HS, country, sector and event type (capacity expansion, investment, subsidy, restriction, tariff, procurement, shortage, recall, weather disruption).
- News summaries are hypotheses with links, not evidence of actual orders.

## Export opportunity dossier

For every product:
- India exports/destinations: [Commerce TIA](https://trade-analytics.commerce.gov.in/public/indiaTrade).
- Agri/processed-food stats, exporter directory and leads: [APEDA AgriExchange](https://agriexchange.apeda.gov.in/Home/).
- Global importer demand and supplier competition: [UN Comtrade](https://comtrade.un.org/).
- Benchmark prices: [World Bank Pink Sheet](https://www.worldbank.org/en/research/commodity-markets).
- Export policy/licensing: [DGFT](https://www.dgft.gov.in/) and applicable FSSAI/BIS/sector regulators.

Shortlist markets using import value/volume trend, supplier mix, Indian export trend, unit values (not transaction prices), tariff/NTM tasks, logistics fit, FX, quality standards and concentration. Confirm exact HS code and destination rules.

## Tenders and buyer leads

- [CPPP eProcurement](https://eprocure.gov.in/eprocure/app): active tenders, corrigenda, bid awards and searches by item title, buyer, location, value and date. Advanced search may require CAPTCHA; do not bypass it. Bid submission can require registration and Digital Signature Certificate.
- [GeM bids](https://bidplus.gem.gov.in/all-bids): public procurement discovery.
- [APEDA buyer leads](https://agriexchange.apeda.gov.in/Buyer/MyBuyOffers) and [seller leads](https://agriexchange.apeda.gov.in/Seller/SellLead): agricultural/processed-food counterparties. APEDA explicitly advises users to verify counterparties.
- Other industries: add relevant Export Promotion Councils, public trade-fair directories, lawful importer registries and licensed trade-data providers.

Tender schema: title, tender ID/reference, buyer, item/specification, quantity, value if published, location, publish/close date and timezone, EMD, eligibility, documents, corrigenda, award status, source timestamp. Alert on deadline/corrigendum.

## Limitations

CPPP CAPTCHA must not be bypassed. APEDA leads are user-submitted, not guaranteed. TIA/TradeStat may expose downloads rather than stable APIs. Weather and news alone do not prove profitable demand.
