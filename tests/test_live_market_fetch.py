from src.connectors import live_market


class FakeOGDClient:
    last_call = None

    def __init__(self, api_key=None):
        self.api_key = api_key

    def records(self, resource_id, **kwargs):
        FakeOGDClient.last_call = (resource_id, kwargs)
        return {"records": [{"commodity": "Turmeric", "market": "Unjha", "modal_price": "9000"}]}


def test_agmarknet_fetch_uses_resource_and_exact_commodity_filter(monkeypatch):
    monkeypatch.setattr(live_market, "OGDClient", FakeOGDClient)
    result = live_market.fetch_agmarknet_prices("Turmeric", "test-key")
    resource_id, params = FakeOGDClient.last_call
    assert resource_id == live_market.AGMARKNET_RESOURCE_ID
    assert params["filters"] == {"commodity": "Turmeric"}
    assert params["limit"] <= 100
    assert result["matched_records"] == 1
