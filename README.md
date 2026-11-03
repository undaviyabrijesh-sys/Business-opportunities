# Business Opportunities Intelligence Platform

A data-driven discovery system for local and global business opportunities. The platform combines official trade, commodity, weather, procurement, industrial, news and trend signals to identify products worth sourcing, manufacturing, importing, exporting or distributing.

## Product vision

For a selected product or product category, the platform should answer:

1. **Demand:** Where is demand growing, and what evidence supports it?
2. **Supply:** Which regions/countries produce or export it?
3. **Buy:** Where can it be sourced, at what benchmark price, and from whom?
4. **Sell:** Which domestic markets, import destinations, buyers or tenders are relevant?
5. **Economics:** What are indicative landed costs, logistics, duties, gross margins and working-capital needs?
6. **Risk:** What could invalidate the opportunity (seasonality, weather, policy, quality, concentration, currency, regulation)?

This is decision support, not a guarantee of profit. Every opportunity must show evidence, source dates, assumptions and confidence.

## Initial build priorities

- India-first data foundation with global trade comparison.
- Selectable product/category and HS-code mapping.
- Mandi/commodity price spreads and seasonality.
- Import/export growth and destination discovery.
- Government tender and procurement demand.
- Weather/crop/production risk overlays.
- Opportunity scoring with transparent components.
- Buyer/supplier/market discovery links.
- Streamlit research desk with filters, charts and an opportunity detail view.

## Data sources

See [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) for the source registry, official links, access notes and integration status.

Primary sources to start with:

- Open Government Data Platform India / AGMARKNET
- Department of Commerce Trade Intelligence & Analytics and TradeStat (DGCI&S)
- India Meteorological Department API portal
- Central Public Procurement Portal and GeM
- MoSPI eSankhyiki / Index of Industrial Production
- UN Comtrade
- CBI Market Information, Global Trade Helpdesk and ITC Trade Map / Export Potential Map
- European Commission Access2Markets and India Trade Connect
- World Bank Commodity Markets / Pink Sheet
- FAOSTAT and Eurostat

## Architecture

```text
Official/public sources
        |
        v
Source adapters (API / CSV / download / monitored web)
        |
        v
Raw landing zone (immutable, timestamped)
        |
        v
Validation + normalization + HS/product/geography mapping
        |
        +----> PostgreSQL (operational metadata, opportunities)
        +----> Parquet/DuckDB (analytical history)
        |
        v
Signal & opportunity engine
        |
        +----> demand signals
        +----> supply signals
        +----> price spreads / arbitrage
        +----> weather & seasonality
        +----> procurement / buyer signals
        +----> risk & feasibility
        |
        v
Streamlit opportunity research desk
```

## Suggested stack

- Python 3.11+
- Streamlit for the interactive research desk
- Pandas / Polars for processing
- DuckDB + Parquet for the initial analytical store
- PostgreSQL when multi-user workflows and persistent operational records are needed
- Plotly for charts and maps
- Pydantic for validated data contracts
- APScheduler or GitHub Actions for scheduled ingestion
- pytest + Ruff for quality checks

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The first version uses clearly labelled illustrative/sample records until each source adapter is connected and verified. Do not treat sample values as current market quotes.

## Opportunity scoring (initial hypothesis)

A transparent 0-100 score will combine:

- Demand momentum (25%)
- Supply gap / import dependence (20%)
- Price spread and gross-margin potential (20%)
- Market accessibility / buyer evidence (15%)
- Seasonality and supply reliability (10%)
- Regulatory, logistics and execution risk (10%, deducted)

Weights are provisional and must be calibrated against observed outcomes. The interface will expose component scores and evidence rather than present a black-box recommendation.

## Roadmap

1. Foundation: source registry, schemas, sample dashboard, validation.
2. India signals: AGMARKNET + TradeStat + IMD + tenders + IIP.
3. Product intelligence: HS-code mapping, market pairs, seasonality.
4. Global expansion: UN Comtrade + World Bank + FAOSTAT + Eurostat.
5. Commercial layer: buyer/supplier discovery, logistics and landed-cost models.
6. Alerts, watchlists, backtesting and opportunity outcome tracking.

## Responsible use

Respect each source's terms, API keys, rate limits and redistribution rules. Prefer official APIs/downloads. Do not scrape authenticated or rate-limited portals in ways that violate terms. Preserve source URLs, retrieval timestamps, units, revisions and data lineage.

## Item research: search, weather, news, exports and tenders

The dashboard accepts a free-text product search and opens an item research workspace. It includes trade/export market links, an international market-intelligence tab (CBI, Global Trade Helpdesk, ITC Trade Map, Export Potential Map, Access2Markets and India Trade Connect), an IMD forecast and district-warning lookup, item-keyword news discovery, CPPP/GeM tender links, APEDA buyer/seller leads and a basic unit-economics calculator. The international portals are currently research links, not automated data feeds.

See:
- [Item research and exports workflow](docs/ITEM_RESEARCH_AND_EXPORTS.md)
- [Official source registry](docs/DATA_SOURCES.md)

### Environment variables

Copy `.env.example` to `.env` if using API connectors. Set keys only in your local environment or deployment secrets; never commit credentials. OGD resource calls require `OGD_API_KEY`; broader UN Comtrade use may require `COMTRADE_API_KEY`.

Install dependencies with `pip install -r requirements.txt`, then run `streamlit run app.py`.

Current data views clearly distinguish live portal lookups from illustrative/sample data. CPPP CAPTCHA is not bypassed, and user-submitted buyer/seller leads must be independently verified.
