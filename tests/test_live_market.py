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



def test_comtrade_normalization_preserves_reporter_for_global_markets():
    payload = {"data": [{
        "period": "2024",
        "reporterCode": 840,
        "reporterDesc": "USA",
        "partnerCode": 0,
        "partnerDesc": "World",
        "flowCode": "M",
        "flowDesc": "Imports",
        "cmdCode": "391239",
        "cmdDesc": "Cellulose ethers",
        "primaryValue": 987654,
        "netWgt": 50000,
        "qtyUnitAbbr": "kg",
    }]}
    row = normalize_comtrade(payload)[0]
    assert row["reporter"] == "USA"
    assert row["flow"] == "Imports"
    assert row["trade_value_usd"] == 987654



def test_global_import_fetch_uses_all_reporters(monkeypatch):
    import src.connectors.live_market as live

    class FakeClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        def query(self, **kwargs):
            assert kwargs["reporter_code"] == "ALL"
            assert kwargs["partner_code"] == "0"
            assert kwargs["flow_code"] == "M"
            return {"data": [{
                "period": "2024",
                "reporterDesc": "Germany",
                "partnerDesc": "World",
                "flowDesc": "Imports",
                "cmdCode": "391239",
                "primaryValue": 250000,
            }], "messages": []}

    monkeypatch.setattr(live, "ComtradeClient", FakeClient)
    result = live.fetch_global_import_markets("391239", "2024")
    assert result["source_status"] == "live_records"
    assert result["records"][0]["reporter"] == "Germany"
    assert result["records"][0]["trade_value_usd"] == 250000
