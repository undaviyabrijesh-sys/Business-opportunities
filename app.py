import json
import os
from datetime import date
from pathlib import Path
from urllib.parse import quote_plus
import pandas as pd
import streamlit as st
from src.demo_data import sample_opportunities
from src.search import item_dossier_plan, load_products
from src.opportunity_engine import calculate_unit_economics, assess_capital_fit, assess_opportunity
from src.connectors.apeda import opportunity_links
from src.connectors.tenders import CPPP_ADVANCED_SEARCH, CPPP_HOME, GEM_BIDS
from src.connectors.imd import IMDClient
from src.connectors.news import search_product_news, PIB_RSS
from src.connectors.live_market import fetch_agmarknet_prices, fetch_india_trade

ROOT = Path(__file__).parent

def configured_secret(name: str):
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name)

st.set_page_config(page_title="Opportunity Intelligence", page_icon="🌐", layout="wide")
st.markdown("""<style>.stApp{background:linear-gradient(135deg,#0b1220,#111c30,#101827);color:#e7eef9}[data-testid="stSidebar"]{background:#0a1322}div[data-testid="stMetric"]{background:rgba(25,42,65,.62);border:1px solid #253b59;padding:14px;border-radius:12px}.hero{padding:22px;border:1px solid #28415f;border-radius:16px;background:linear-gradient(110deg,#16304c,#0c1b2d)}.muted{color:#91a6c2}</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="muted">GLOBAL MARKET SCOUT · INDIA FIRST</div><h1>Opportunity Intelligence Desk</h1><div class="muted">Search any item. Discover sourcing, export markets, buyers, weather, news and tenders.</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Research controls")
    item = st.text_input("Search any item", value="Turmeric", placeholder="e.g. lactose, turmeric powder, coir pith")
    scope = st.selectbox("Market scope", ["India domestic", "India → Global exports", "Global sourcing → India imports", "Global markets"])
    model = st.selectbox("Business model", ["Trading / distribution", "Export", "Import", "Manufacturing / processing", "Tender supply"])
    region = st.selectbox("Base location", ["Ahmedabad, Gujarat", "Other Gujarat", "Other India", "Global"])
    capital = st.select_slider("Indicative capital", options=["Below ₹5 lakh", "₹5–25 lakh", "₹25–50 lakh", "₹50 lakh–₹2 crore", "Above ₹2 crore"], value="₹50 lakh–₹2 crore")
    catalogue = load_products()
    categories = ["All sectors"] + sorted({p["category"] for p in catalogue})
    category_filter = st.selectbox("Sector / product category", categories)
    opportunity_types = ["All opportunity types", "Domestic sourcing spread", "Export market screening", "Industrial demand screening"]
    opportunity_filter = st.selectbox("Opportunity type", opportunity_types)
    min_score = st.slider("Minimum opportunity score", 0, 100, 0, 5)
    confidence_filter = st.selectbox("Evidence confidence", ["All confidence levels", "High", "Medium", "Low (sample)"])
    mapping_filter = st.selectbox("HS classification", ["All products", "Candidate HS mapping", "HS classification pending"])
    show_illustrative = st.checkbox("Include illustrative/sample opportunities", value=True)
    st.caption("Filters narrow the current catalogue and opportunity records. Capital is a research profile, not yet a validated capex screen.")

plan = item_dossier_plan(item.strip() or "Turmeric")
suggestions = plan["suggestions"]
if category_filter != "All sectors":
    suggestions = [x for x in suggestions if x["category"] == category_filter]
if mapping_filter == "Candidate HS mapping":
    suggestions = [x for x in suggestions if x.get("hs_codes")]
elif mapping_filter == "HS classification pending":
    suggestions = [x for x in suggestions if not x.get("hs_codes")]
if suggestions:
    rec = suggestions[0]
    st.caption(f"Catalogue match: {rec['name']} · HS mapping: {chr(44).join(rec.get('hs_codes', [])) or 'Needs expert classification'}")
else:
    st.caption("New item: research as an unclassified product until its HS code is verified.")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Item", item or "—")
c2.metric("Scope", scope)
c3.metric("Business model", model)
c4.metric("Capital profile", capital)
tabs = st.tabs(["Overview","Opportunity engine","Live market data","Trade & export","International intelligence","Weather","News & trends","Tenders & buyers","Commercial model","Sources"])
with tabs[0]:
    st.subheader(f"Opportunity workspace: {item}")
    st.info("Live ranking is withheld until price, trade, buyer and risk signals are connected and validated.")
    st.write("India sourcing → domestic prices → global importer demand → export feasibility → buyer/tender leads → landed-cost model.")
    if suggestions:
        st.dataframe(pd.DataFrame([{"Product":x["name"],"Category":x["category"],"HS codes":", ".join(x.get("hs_codes",[])) or "Pending","Mapping":x["status"]} for x in suggestions]),use_container_width=True,hide_index=True)
    opps = sample_opportunities()
    product_categories = {p["name"]: p["category"] for p in catalogue}
    opps["category"] = opps["product"].map(product_categories).fillna("Unclassified")
    matches = opps[opps["product"].str.casefold().eq(item.casefold())].copy()
    if category_filter != "All sectors":
        matches = matches[matches["category"] == category_filter]
    if opportunity_filter != "All opportunity types":
        matches = matches[matches["type"] == opportunity_filter]
    matches = matches[matches["score"] >= min_score]
    if confidence_filter != "All confidence levels":
        matches = matches[matches["confidence"] == confidence_filter]
    if not show_illustrative:
        matches = matches.iloc[0:0]
    st.caption("Opportunity filters apply to the illustrative starter records below; live evidence-backed ranking is not connected yet.")
    st.dataframe(matches if not matches.empty else pd.DataFrame([{"Status":"No opportunity matches the selected filters","Action":"Broaden filters or collect verified market, buyer and cost data"}]),use_container_width=True,hide_index=True)
with tabs[1]:
    st.subheader("Evidence-led opportunity screening")
    st.caption("Build a first-pass case from your own quotes and evidence. No live demand or buyer data is assumed.")
    st.write(f"**Screening item:** {item or 'Unspecified'} · **Model:** {model} · **Base:** {region}")
    st.markdown("#### Commercial assumptions")
    a,b,c1 = st.columns(3)
    purchase = a.number_input("Purchase cost / unit (₹)", min_value=0.0, value=0.0, step=1.0, key="engine_purchase")
    freight = b.number_input("Freight & handling / unit (₹)", min_value=0.0, value=0.0, step=1.0, key="engine_freight")
    variable_other = c1.number_input("Other variable cost / unit (₹)", min_value=0.0, value=0.0, step=1.0, key="engine_other")
    d,e,fixed = st.columns(3)
    selling = d.number_input("Expected net selling price / unit (₹)", min_value=0.0, value=0.0, step=1.0, key="engine_selling")
    monthly_qty = e.number_input("Expected monthly quantity", min_value=0.0, value=0.0, step=1.0, key="engine_quantity")
    fixed_cost = fixed.number_input("Monthly fixed operating cost (₹)", min_value=0.0, value=0.0, step=1000.0, key="engine_fixed")
    g,h = st.columns(2)
    capex = g.number_input("Setup / equipment capex (₹)", min_value=0.0, value=0.0, step=10000.0, key="engine_capex")
    wc_days = h.number_input("Working-capital cycle (days)", min_value=0.0, value=30.0, step=5.0, key="engine_wc_days")
    commercial_ready = selling > 0 and monthly_qty > 0
    economics = calculate_unit_economics(purchase, freight, variable_other, selling, monthly_qty, fixed_cost, capex, wc_days)
    if commercial_ready:
        fit = assess_capital_fit(economics["estimated_funding_need"], capital)
        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Contribution / unit", f"₹{economics['contribution_per_unit']:,.2f}")
        k2.metric("Contribution margin", f"{economics['contribution_margin_pct']:.1f}%" if economics["contribution_margin_pct"] is not None else "—")
        k3.metric("Monthly net contribution", f"₹{economics['monthly_net_contribution']:,.0f}")
        k4.metric("Estimated funding need", f"₹{economics['estimated_funding_need']:,.0f}")
        st.write(f"Capital fit against **{capital}**: **{fit['status'].replace('_', ' ')}**")
        st.caption(economics["assumption_note"])
        if economics["simple_payback_months"] is not None:
            st.metric("Simple capex payback", f"{economics['simple_payback_months']:.1f} months")
        if economics["status"] != "positive_contribution":
            st.warning("Unit contribution is zero or negative before fixed operating costs.")
    else:
        fit = assess_capital_fit(0, capital)
        st.info("Enter a selling price and monthly quantity to calculate the commercial case. Zero values are treated as missing assumptions, not market prices.")
    st.markdown("#### Evidence assessment")
    st.caption("Rate only what you have evidence for. Leave a dimension as Not assessed if you have not checked it.")
    evidence_options = ["Not assessed", 0, 20, 40, 60, 80, 100]
    labels = [
        ("Demand momentum", "demand_momentum"),
        ("Supply gap", "supply_gap"),
        ("Price economics", "price_economics"),
        ("Buyer access", "buyer_access"),
        ("Supply stability", "supply_stability"),
        ("Risk severity", "risk"),
    ]
    signal_cols = st.columns(3)
    signals = {}
    for idx, (label, key) in enumerate(labels):
        value = signal_cols[idx % 3].select_slider(label, options=evidence_options, value="Not assessed", key=f"evidence_{key}")
        signals[key] = None if value == "Not assessed" else float(value)
    score = assess_opportunity(signals, fit)
    s1,s2,s3 = st.columns(3)
    s1.metric("Evidence-adjusted score", f"{score['score']:.1f}/100" if any(v is not None for v in signals.values()) else "Not scored")
    s2.metric("Evidence coverage", f"{score['coverage']*100:.0f}%")
    s3.metric("Risk deduction", f"{score['risk_penalty']:.1f} pts" if score["risk_penalty"] is not None else "Not assessed")
    if score["decision_gate"] == "screen_for_diligence":
        st.success("Gate passed: move to detailed due diligence. This is not an investment recommendation.")
    else:
        st.warning("Gate not passed: collect more evidence or revise the capital requirement before prioritising this opportunity.")
    st.caption("Score weights: demand 25%, supply gap 20%, price economics 20%, buyer access 15%, supply stability 10%; risk deduction up to 10 points. Missing evidence reduces coverage. Scores are analyst inputs, not automatically verified facts.")
    with st.expander("What to verify before investing"):
        st.markdown("- Obtain dated, grade-matched supplier and buyer quotations")
        st.markdown("- Verify trade volumes, import/export restrictions, HS classification and destination standards")
        st.markdown("- Confirm buyer identity, payment terms, credit exposure and repeat demand")
        st.markdown("- Include receivables, payables, inventory buffers, tax, insurance, financing and FX in working capital")
        st.markdown("- Validate machinery, premises, licences, manpower, utilities and contingency capex")

with tabs[2]:
    st.subheader("Live source data")
    st.caption("Fetched on demand from official sources; this is not tick-by-tick pricing. AGMARKNET is a daily dataset, while UN Comtrade is annual trade statistics. Source and retrieval time are displayed.")
    ogd_key = configured_secret("OGD_API_KEY")
    comtrade_key = configured_secret("COMTRADE_API_KEY")
    left, right = st.columns(2)
    left.metric("AGMARKNET / OGD", "Configured" if ogd_key else "API key needed")
    right.metric("UN Comtrade", "API key configured" if comtrade_key else "Public preview mode")
    st.markdown("#### India mandi prices")
    market_item = suggestions[0]["name"] if suggestions else item
    st.caption("Canonical commodity query: " + str(market_item))
    if st.button("Fetch live mandi prices", key="fetch_mandi"):
        if not ogd_key:
            st.error("Add OGD_API_KEY in Streamlit app Secrets or server environment.")
        else:
            try:
                result = fetch_agmarknet_prices(market_item, ogd_key)
                st.caption("Source: " + result["source"] + " | Retrieved: " + result["retrieved_at"] + " | Matched rows: " + str(result["matched_records"]))
                if result["records"]:
                    df = pd.DataFrame(result["records"])
                    for col in ["min_price", "max_price", "modal_price"]:
                        df[col] = pd.to_numeric(df[col], errors="coerce")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    prices = df.dropna(subset=["modal_price"])
                    if len(prices) >= 2:
                        x,y,z = st.columns(3)
                        x.metric("Average modal price", "INR {:,.0f}/quintal".format(prices["modal_price"].mean()))
                        y.metric("Lowest market quote", "INR {:,.0f}".format(prices["modal_price"].min()))
                        z.metric("Highest market quote", "INR {:,.0f}".format(prices["modal_price"].max()))
                else:
                    st.warning("API responded but no returned rows matched this item.")
            except Exception as exc:
                st.error("AGMARKNET request failed: " + str(exc))
    st.divider()
    st.markdown("#### India international trade")
    candidate_codes = sorted({str(code) for product in suggestions for code in product.get("hs_codes", []) if str(code).isdigit()})
    if candidate_codes:
        hs_code = st.selectbox("Candidate HS code", candidate_codes, key="live_hs_code")
        confirmed = st.checkbox("I verified this HS code for exact product form, grade and year", key="live_hs_confirm")
        flow = st.selectbox("Trade flow", ["Exports", "Imports"], key="live_trade_flow")
        years = date.today().year
        periods = ",".join(str(y) for y in range(years - 4, years))
        if st.button("Fetch UN Comtrade records", key="fetch_comtrade"):
            if not confirmed:
                st.warning("Confirm HS classification first. Catalogue codes are candidate mappings only.")
            else:
                try:
                    result = fetch_india_trade(hs_code, periods, "X" if flow == "Exports" else "M", comtrade_key)
                    st.caption("Source: " + result["source"] + " | Retrieved: " + result["retrieved_at"] + " | Status: " + result["source_status"])
                    if result["records"]:
                        df = pd.DataFrame(result["records"])
                        df["trade_value_usd"] = pd.to_numeric(df["trade_value_usd"], errors="coerce")
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        annual = df.groupby("period")["trade_value_usd"].sum().sort_index()
                        if len(annual) >= 2:
                            change = (annual.iloc[-1] / annual.iloc[-2] - 1) * 100 if annual.iloc[-2] else None
                            a,b = st.columns(2)
                            a.metric("Latest trade value", "USD {:,.0f}".format(annual.iloc[-1]))
                            b.metric("Change vs prior period", "{:+.1f}%".format(change) if change is not None else "Not calculable")
                    else:
                        st.warning("No trade rows returned. Check HS code, period availability and API limits.")
                except Exception as exc:
                    st.error("UN Comtrade request failed: " + str(exc))
    else:
        st.info("No candidate HS code for this item. Classification is required; no code will be invented.")
    st.caption("Trade data is not a live price or proof of reachable buyers. Validate HS revision, coverage and provisional periods.")
    st.markdown("Add OGD_API_KEY and optionally COMTRADE_API_KEY in Streamlit App Settings → Secrets. Never commit credentials to GitHub.")

with tabs[3]:
    st.subheader("Import, export and market discovery")
    st.markdown("- [India Trade Intelligence & Analytics](https://trade-analytics.commerce.gov.in/public/indiaTrade)")
    st.markdown("- [TradeStat monthly partner trade](https://tradestat.commerce.gov.in/ftspcc/ttrade_country_wise)")
    st.markdown("- [UN Comtrade global importer demand](https://comtrade.un.org/)")
    st.markdown("- [World Bank commodity prices and outlook](https://www.worldbank.org/en/research/commodity-markets)")
    for label,url in opportunity_links(item).items(): st.markdown(f"- [{label}]({url})")
    st.caption("APEDA is especially relevant to agricultural and processed-food goods; verify leads and counterparties.")
    st.checkbox("Confirm HS code and classification year",key="hs_confirm")
    st.checkbox("Compare India export growth with destination imports",key="trade_compare")
    st.checkbox("Check destination tariffs and product standards",key="tariff_check")
    st.checkbox("Check freight, port, insurance and payment risk",key="logistics_check")

with tabs[4]:
    st.subheader("International market intelligence")
    st.write(f"Research product: **{item}**")
    st.caption("These are external research portals, not live API integrations. Open a source, search the product and destination market, then record the source date and evidence in your opportunity assessment.")
    st.markdown("#### Market research and export readiness")
    st.markdown("- [CBI Market Information](https://www.cbi.eu/market-information) — sector and product studies, European buyer requirements, trends and market-entry guidance.")
    st.markdown("- [Global Trade Helpdesk](https://globaltradehelpdesk.org/) — product/country trade opportunities, import demand, tariffs, regulations and potential buyer discovery. Coverage varies by market.")
    st.markdown("- [India Trade Connect](https://www.trade.gov.in/) — India exporter support, market access guidance, export trends, FTA benefits and government/export-promotion connections.")
    st.divider()
    st.markdown("#### Trade statistics and export potential")
    st.markdown("- [ITC Trade Map](https://www.trademap.org/Index.aspx) — monthly, quarterly and annual trade values, quantities, growth, market shares, competing suppliers and company directory.")
    st.markdown("- [ITC Export Potential Map](https://exportpotential.intracen.org/en/) — modelled export potential and unrealised potential by product, exporter and destination market.")
    st.markdown("- [ITC Market Analysis Tools](https://marketanalysis.intracen.org/en) — access point for Trade Map, Export Potential Map, Market Access Map and related tools.")
    st.divider()
    st.markdown("#### Tariffs, rules and market-entry requirements")
    st.markdown("- [European Commission Access2Markets](https://trade.ec.europa.eu/access-to-markets/en/home) — tariffs, taxes, rules of origin, customs procedures, product requirements and trade barriers.")
    st.info("For Access2Markets, choose the relevant origin country, destination and product code. It is particularly useful for EU market entry; do not assume every tool has complete coverage for every country pair.")
    st.warning("Important: these portals provide research and decision support, not guaranteed buyers or confirmed orders. Trade Map company information and any buyer leads must be independently verified. Export-potential figures are model estimates, not sales forecasts.")
    st.markdown("#### Research checklist for this item")
    st.write(f"1. Search **{item}** and verify the exact product form, grade and HS code.")
    st.write("2. Compare destination import growth, supplier concentration and unit values.")
    st.write("3. Check tariffs, rules of origin, standards, certificates and import procedures.")
    st.write("4. Verify buyer identity, purchase history, payment risk and actual demand before quoting.")
    st.caption("No automated scraping or API ingestion is claimed for these portals. We will integrate structured data only where official access, terms and repeatable schemas permit it.")

with tabs[5]:
    st.subheader("Weather and operational disruption")
    st.write("Identify relevant production, warehouse, port or route locations, then enter their IMD IDs.")
    st.markdown("[Official IMD API portal](https://api.imd.gov.in/public/) · [API reference](https://api.imd.gov.in/public/api_reference.html)")
    station_id=st.text_input("IMD city forecast station ID")
    district_id=st.text_input("IMD district warning ID (optional)")
    if st.button("Fetch IMD forecast / warnings"):
        try:
            client=IMDClient()
            if station_id.strip(): st.json(client.city_forecast(station_id.strip()))
            if district_id.strip(): st.json(client.district_warnings(district_id.strip()))
            if not station_id.strip() and not district_id.strip(): st.warning("Enter an IMD identifier.")
        except Exception as exc: st.error(f"IMD request failed: {exc}")
    st.caption("Show issue time, validity, location, units and distinguish observations from forecasts.")
with tabs[6]:
    st.subheader("News and emerging trends")
    st.write(f"Product query: {item}")
    st.markdown(f"- [Search item-related news](https://news.google.com/search?q={quote_plus(item)}&hl=en-IN&gl=IN&ceid=IN%3Aen)")
    st.markdown(f"- [Official PIB press releases RSS]({PIB_RSS})")
    if st.button("Fetch item news headlines"):
        try:
            rows=search_product_news(item.strip())
            if rows: st.dataframe(pd.DataFrame(rows)[["title","source","published_at","url"]],use_container_width=True,hide_index=True)
            else: st.info("No headlines returned.")
        except Exception as exc: st.error(f"News feed request failed: {exc}")
    st.caption("News is a discovery signal, not verified demand. Corroborate with data and buyers.")
with tabs[7]:
    st.subheader("Tenders, buyers and seller leads")
    st.write(f"Search terms: {item}")
    st.markdown(f"- [CPPP active tenders]({CPPP_HOME})")
    st.markdown(f"- [CPPP advanced search]({CPPP_ADVANCED_SEARCH})")
    st.markdown(f"- [GeM bids]({GEM_BIDS})")
    st.markdown("- [APEDA international buyer leads](https://agriexchange.apeda.gov.in/Buyer/MyBuyOffers)")
    st.markdown("- [APEDA Indian seller leads](https://agriexchange.apeda.gov.in/Seller/SellLead)")
    st.caption("CPPP may require CAPTCHA; no bypass is attempted. Check closing date, EMD, eligibility and corrigenda. APEDA leads are not pre-verified.")
    st.write(", ".join([item, f"{item} supply", f"{item} procurement", f"{item} tender"]))
with tabs[8]:
    st.subheader("Commercial viability — unit economics")
    st.caption("Use actual quotes only; this calculator is not a live margin estimate.")
    a,b,c=st.columns(3)
    purchase=a.number_input("Purchase cost / unit (₹)",min_value=0.0,value=0.0)
    freight=b.number_input("Freight / handling / unit (₹)",min_value=0.0,value=0.0)
    other=c.number_input("Other costs / unit (₹)",min_value=0.0,value=0.0)
    d,e=st.columns(2)
    selling=d.number_input("Expected net selling price (₹)",min_value=0.0,value=0.0)
    quantity=e.number_input("Quantity (units)",min_value=0.0,value=1.0)
    cost=purchase+freight+other
    margin=selling-cost
    x,y,z=st.columns(3)
    x.metric("Total cost / unit",f"₹{cost:,.2f}")
    y.metric("Contribution / unit",f"₹{margin:,.2f}")
    z.metric("Total contribution",f"₹{margin*quantity:,.2f}")
    st.caption("Separately model duties, taxes, packaging, wastage, insurance, commission, finance, rejection, FX and working capital.")
with tabs[9]:
    st.subheader("Source coverage and setup")
    st.markdown("- OGD/AGMARKNET: configure `OGD_API_KEY` for documented API access.")
    st.markdown("- IMD: use documented endpoints and check current access requirements.")
    st.markdown("- UN Comtrade: preview has limits; configure `COMTRADE_API_KEY` for broader access.")
    st.markdown("- News: PIB RSS and item-keyword Google News RSS are discovery feeds.")
    st.markdown("- CPPP: official tender search is linked; CAPTCHA is not bypassed.")
    st.markdown("- APEDA: public export reporting and buyer/seller leads; verify counterparties.")
    st.markdown("- CBI, Global Trade Helpdesk, ITC Trade Map, Export Potential Map, Access2Markets and India Trade Connect: linked research portals; not yet ingested as live APIs.")
    st.markdown("See `docs/DATA_SOURCES.md` and `docs/ITEM_RESEARCH_AND_EXPORTS.md`.")
st.divider()
st.caption("India-first business research. Sample rankings are illustrative. Verify HS codes, counterparties, regulatory requirements and commercial quotes.")