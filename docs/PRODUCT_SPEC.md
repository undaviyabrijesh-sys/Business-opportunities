# Product specification

## Core user journey

1. User selects market scope: India domestic, India import, India export, global or local radius.
2. User selects a product, category or HS code; the app proposes mappings and asks the user to confirm uncertain ones.
3. User configures business model: trading/distribution, import, export, manufacturing, processing, contract supply or tender participation.
4. User selects constraints: budget, state/city, minimum gross margin, capacity, preferred markets, risk tolerance and time horizon.
5. Engine ranks opportunities and shows evidence behind each score.
6. User opens an opportunity dossier: source/sell markets, suppliers, buyer leads, tenders, trade trends, price history, weather exposure, logistics assumptions, compliance checklist and unit economics.
7. User records outreach and outcome so scores can be calibrated.

## Main dashboard pages

- **Market Radar:** opportunity ranking, changes since last refresh, evidence confidence and filters.
- **Product Explorer:** search products, HS-code mapping, market/commodity price and trade trends.
- **Buy & Source:** origin markets, producer/exporter leads, availability, indicative prices and supplier verification tasks.
- **Sell & Demand:** destination markets, importers, buyer leads, tender demand and channel options.
- **Price Intelligence:** mandi/wholesale/benchmark price series, price dispersion, seasonality, spreads and volatility.
- **Trade Map:** origin-to-destination trade flows by product, partner and HS code.
- **Weather & Disruption:** forecast warnings, climate anomalies and exposure of production/logistics regions.
- **Tender Radar:** open bids, buyer department, item/specification, quantity, closing date, eligibility and tender documents.
- **Opportunity Dossier:** commercial thesis, evidence, economics, constraints, risks, validation checklist and sources.
- **Watchlist & Alerts:** tracked products, markets, price thresholds, tender deadlines and new trade signals.

## Opportunity types

- Domestic arbitrage: comparable product at lower source-market price versus higher destination-market price.
- Import substitution: domestic import dependence + local supply feasibility + price/lead-time advantage.
- Export expansion: growing destination imports + India's export capability + market access.
- Seasonal sourcing: predictable production/harvest cycles and price seasonality.
- Processing/value addition: raw material availability + downstream demand and margin potential.
- Procurement: relevant tenders with achievable technical and commercial eligibility.
- Climate/weather-driven: an explicit, evidence-backed demand/supply change, not speculative weather correlation.

## Ranking model (initial transparent baseline)

All component scores are normalized 0-100; weights are configurable and versioned.

- Demand momentum: 25%
- Supply gap / import dependence: 20%
- Price-spread / unit-economics potential: 20%
- Buyer accessibility / evidence: 15%
- Supply stability / seasonality: 10%
- Risk penalty: up to 10 percentage points

Opportunity score = weighted positive components minus risk penalty. Missing data must lower evidence confidence, not silently be interpreted as zero risk or high opportunity.

Every opportunity must display:
- score and score version
- confidence (coverage, recency, source reliability and agreement)
- supporting and contradicting evidence
- as-of timestamp and source freshness
- assumptions and scenario range
- key reasons it may fail
- next validation action

Do not call the highest score "profitable". Label it "research priority" until quotes, buyer confirmation, compliance and logistics have been validated.

## Commercial unit economics

At minimum, expose:
- purchase price and unit normalization
- packaging / processing / wastage
- inland freight and handling
- insurance
- customs duties / cess / taxes where applicable
- port, documentation and customs broker charges
- finance / working-capital cost
- selling price net of discounts and channel costs
- bad debt / returns / quality rejection allowance
- gross contribution and break-even selling price
- low/base/high scenarios and sensitivity to FX/freight/price movement

Tariffs and regulatory rules must come from current official sources and be date-stamped. Never hard-code a tariff as timeless.

## Geographic model

Use standardized ISO country codes, Indian state/district identifiers and a canonical market/location table. Separate:
- production origin
- wholesale market
- port / border
- warehouse / logistics hub
- buyer destination
- tender delivery location

Do not infer the cheapest route or exact freight from straight-line distance. Add real carrier/route quotes in a later phase.

## MVP acceptance criteria

- Product selection updates all visible metrics and charts.
- Source records link back to the original official page/file.
- All chart axes show units and date ranges.
- Missing or stale data is visible.
- Illustrative records are clearly marked.
- Opportunity score can be explained component by component.
- CSV export includes provenance.
- Tests cover unit/currency normalization, HS-code mapping and score calculation.
