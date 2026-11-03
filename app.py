import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.demo_data import sample_market_prices, sample_opportunities, sample_trade_data

ROOT = Path(__file__).parent
st.set_page_config(page_title="Opportunity Intelligence", page_icon="🌐", layout="wide")

st.markdown("""
<style>
  .stApp { background: linear-gradient(135deg, #0b1220 0%, #111c30 55%, #101827 100%); color: #e7eef9; }
  [data-testid="stSidebar"] { background: #0a1322; }
  div[data-testid="stMetric"] { background: rgba(25, 42, 65, .62); border: 1px solid #253b59; padding: 16px; border-radius: 12px; }
  .hero { padding: 22px 24px; border: 1px solid #28415f; border-radius: 16px; background: linear-gradient(110deg, rgba(22,48,76,.92), rgba(12,27,45,.8)); margin-bottom: 18px; }
  .muted { color: #91a6c2; font-size: 0.88rem; }
  .warning { background: rgba(178, 125, 27, .14); border: 1px solid rgba(238, 184, 74, .55); border-radius: 10px; padding: 10px 14px; color: #f1d18d; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="muted">GLOBAL MARKET SCOUT · INDIA FIRST</div><h1>Opportunity Intelligence Desk</h1><div class="muted">Find demand gaps. Compare sourcing markets. Validate buyers. Model the economics.</div></div>', unsafe_allow_html=True)
st.markdown('<div class="warning">DEMO MODE: the current charts use synthetic illustrative values. No displayed price, score or destination is a live market recommendation.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Research controls")
    scope = st.selectbox("Market scope", ["India domestic", "India → Global exports", "Global sourcing → India imports", "Global markets"])
    product_path = ROOT / "config" / "products.json"
    products = json.loads(product_path.read_text(encoding="utf-8"))
    product_names = [p["name"] for p in products]
    selected_product = st.selectbox("Product / category", product_names)
    model = st.selectbox("Business model", ["Trading / distribution", "Import", "Export", "Manufacturing / processing", "Tender supply"])
    region = st.selectbox("Base location", ["Ahmedabad, Gujarat", "Other Gujarat", "Other India", "Global"])
    budget = st.select_slider("Indicative capital (INR)", options=["Below ₹5 lakh", "₹5–25 lakh", "₹25–50 lakh", "₹50 lakh–₹2 crore", "Above ₹2 crore"])
    st.caption("Filters become active ranking constraints as verified data adapters are added.")

opps = sample_opportunities()
opps = opps[opps["product"].eq(selected_product)]
if opps.empty:
    opps = pd.DataFrame([{"product":selected_product,"type":"Research required","market_pair":"Not yet mapped","score":0,"confidence":"No evidence","thesis":"This product needs HS-code mapping and source onboarding."}])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Research candidates", len(opps))
col2.metric("Market scope", scope)
col3.metric("Product", selected_product)
col4.metric("Model", model)

left, right = st.columns([1.5, 1])
with left:
    st.subheader("Opportunity radar")
    st.dataframe(opps[["product","type","market_pair","score","confidence","thesis"]], use_container_width=True, hide_index=True)
with right:
    st.subheader("Signal coverage")
    st.info("Live source adapters are not connected yet. Source coverage and confidence will populate after ingestion is configured.")

st.divider()
st.subheader("Price intelligence")
price_df = sample_market_prices(selected_product)
fig = px.line(price_df, x="date", y="modal_price_inr_per_quintal", color="market",
              title="Illustrative modal-price movement (₹ / quintal)")
fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_title_text="Market")
st.plotly_chart(fig, use_container_width=True)
st.caption("Synthetic demonstration series. A production comparison must normalize commodity grade, variety, unit, date and market level.")

st.divider()
tab1, tab2, tab3 = st.tabs(["Where to buy / source", "Where to sell", "Commercial validation"])
with tab1:
    st.markdown("**Source-market research checklist**")
    st.write("Compare production centres, mandi arrivals, modal prices, exporter concentration, quality grade, seasonality and supplier verification.")
    st.dataframe(price_df.groupby("market", as_index=False)["modal_price_inr_per_quintal"].mean().sort_values("modal_price_inr_per_quintal"), use_container_width=True, hide_index=True)
with tab2:
    st.markdown("**Destination-market discovery**")
    trade_df = sample_trade_data(selected_product)
    st.dataframe(trade_df, use_container_width=True, hide_index=True)
    st.caption("Illustrative destination ranking only. Replace with UN Comtrade / DGCI&S values before use.")
with tab3:
    st.markdown("**Before spending money, validate:**")
    st.checkbox("Buyer demand confirmed directly")
    st.checkbox("Supplier quote and sample verified")
    st.checkbox("Specification / quality requirements confirmed")
    st.checkbox("Freight, duties, taxes and insurance quoted")
    st.checkbox("Licences, standards and import/export restrictions checked")
    st.checkbox("Working capital and payment terms modelled")
    st.checkbox("Low/base/high margin scenarios remain viable")

st.divider()
st.subheader("Official source quick links")
links = [
    ("India Open Government Data", "https://data.gov.in/"),
    ("AGMARKNET daily mandi price dataset", "https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi"),
    ("India Trade Intelligence & Analytics", "https://trade-analytics.commerce.gov.in/public/indiaTrade"),
    ("IMD API Management", "https://api.imd.gov.in/public/"),
    ("CPPP eProcurement", "https://eprocure.gov.in/"),
    ("UN Comtrade", "https://comtrade.un.org/"),
    ("World Bank Commodity Markets", "https://www.worldbank.org/en/research/commodity-markets"),
]
st.columns(2)[0].markdown("\n".join(f"- [{name}]({url})" for name, url in links[:4]))
st.columns(2)[1].markdown("\n".join(f"- [{name}]({url})" for name, url in links[4:]))
st.caption("Opportunity Intelligence · Research decision support. Verify all commercial, legal, quality and logistics details independently.")
