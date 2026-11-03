"""APEDA AgriExchange opportunity links and reporting entrypoints.

Buyer/seller leads on the portal are user-submitted. The portal itself advises
users to verify counterparties. This module intentionally links to public
search pages rather than scraping contact information or implying verification.
"""
APEDA_HOME = "https://agriexchange.apeda.gov.in/Home/"
APEDA_EXPORT_STATS = "https://agriexchange.apeda.gov.in/India/port/Index"
APEDA_BUY_LEADS = "https://agriexchange.apeda.gov.in/Buyer/MyBuyOffers"
APEDA_SELL_LEADS = "https://agriexchange.apeda.gov.in/Seller/SellLead"
APEDA_EXPORTER_DIRECTORY = "https://agriexchange.apeda.gov.in/Exporter/ExporterDirectory"


def opportunity_links(item: str) -> dict[str, str]:
    return {
        "APEDA market intelligence": APEDA_HOME,
        "APEDA export statistics": APEDA_EXPORT_STATS,
        "APEDA international buy leads": APEDA_BUY_LEADS,
        "APEDA India sell leads": APEDA_SELL_LEADS,
        "APEDA exporter directory": APEDA_EXPORTER_DIRECTORY,
    }
