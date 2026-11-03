from src.connectors.live_market import normalize_agmarknet, normalize_comtrade


def test_agmarknet_normalization_filters_item_and_keeps_provenance():
    payload = {
        "records": [
            {
                "Commodity": "Turmeric",
                "Arrival_Date": "03/11/2026",
                "State": "Gujarat",
                "District": "Mehsana",
                "Market": "Unjha",
                "Variety": "Local",
                "Min_Price": "8000",
                "Max_Price": "9500",
                "Modal_Price": "9000",
            },
            {"Commodity": "Wheat", "Modal_Price": "2500"},
        ]
    }
    rows = normalize_agmarknet(payload, "turmeric", "2026-11-03T00:00:00+00:00")
    assert len(rows) == 1
    assert rows[0]["market"] == "Unjha"
    assert rows[0]["modal_price"] == "9000"
    assert rows[0]["source"] == "data.gov.in / AGMARKNET"
    assert rows[0]["data_status"] == "LIVE_SOURCE_RECORD"


def test_agmarknet_no_match_returns_no_rows_not_fake_data():
    assert normalize_agmarknet({"records": [{"Commodity": "Rice"}]}, "turmeric") == []


def test_comtrade_normalization_preserves_period_and_currency_basis():
    payload = {
        "data": [{
            "period": "2025",
            "reporterDesc": "India",
            "partnerDesc": "World",
            "flowDesc": "Exports",
            "cmdCode": "091030",
            "cmdDesc": "Turmeric",
            "primaryValue": 123456.0,
            "netWgt": 12000,
            "qty": 12000,
            "qtyUnitAbbr": "kg",
        }]
    }
    rows = normalize_comtrade(payload, "2026-11-03T00:00:00+00:00")
    assert rows[0]["trade_value_usd"] == 123456.0
    assert rows[0]["period"] == "2025"
    assert rows[0]["reporter"] == "India"
    assert rows[0]["quantity_unit"] == "kg"
    assert rows[0]["source"] == "UN Comtrade"
