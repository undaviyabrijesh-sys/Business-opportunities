"""APEDA AgriExchange public discovery links; leads must be independently verified."""
APEDA_HOME = "https://agriexchange.apeda.gov.in/Home/"
APEDA_EXPORT_STATS = "https://agriexchange.apeda.gov.in/India/port/Index"
APEDA_BUY_LEADS = "https://agriexchange.apeda.gov.in/Buyer/MyBuyOffers"
APEDA_SELL_LEADS = "https://agriexchange.apeda.gov.in/Seller/SellLead"
APEDA_EXPORTER_DIRECTORY = "https://agriexchange.apeda.gov.in/Exporter/ExporterDirectory"


def opportunity_links(item: str = "") -> dict[str, str]:
    return {
        "APEDA market intelligence": APEDA_HOME,
        "Export statistics": APEDA_EXPORT_STATS,
        "International buyer leads": APEDA_BUY_LEADS,
        "India seller leads": APEDA_SELL_LEADS,
        "Exporter directory": APEDA_EXPORTER_DIRECTORY,
    }
