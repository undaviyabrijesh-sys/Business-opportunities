from src.connectors.company_discovery import ResultParser, unwrap_url, search_company_leads


def test_unwrap_duckduckgo_redirect():
    assert unwrap_url("https://duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com") == "https://example.com"
    assert unwrap_url("//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.org") == "https://example.org"


def test_parser_extracts_multiple_search_results():
    html = """
    <div class="result results_links">
      <div class="result__body">
        <a class="result__a" href="https://buyer.example/">Buyer Company</a>
        <a class="result__snippet">Imports product in bulk</a>
      </div>
    </div>
    <div class="result results_links">
      <div class="result__body">
        <a class="result__a" href="https://seller.example/">Seller Company</a>
        <a class="result__snippet">Manufacturer and exporter</a>
      </div>
    </div>
    """
    parser = ResultParser()
    parser.feed(html)
    assert [row["title"] for row in parser.rows] == ["Buyer Company", "Seller Company"]


def test_buyer_and_seller_search_are_separate_and_labelled():
    class Response:
        status_code = 200
        url = "https://example.com"
        text = """
        <div class="result"><a class="result__a" href="https://buyer.example/">Buyer Company</a>
        <a class="result__snippet">Imports product</a></div>
        <div class="result"><a class="result__a" href="https://seller.example/">Seller Company</a>
        <a class="result__snippet">Manufacturer</a></div>
        """
        def raise_for_status(self):
            return None

    class Session:
        def get(self, *args, **kwargs):
            query = kwargs.get("params", {}).get("q", "")
            response = Response()
            if "manufacturer" in query or "distributor" in query:
                response.text = '<div class="result"><a class="result__a" href="https://seller.example/">Seller Company</a><a class="result__snippet">Manufacturer</a></div>'
            else:
                response.text = '<div class="result"><a class="result__a" href="https://buyer.example/">Buyer Company</a><a class="result__snippet">Imports product</a></div>'
            return response

    result = search_company_leads("Titanium Dioxide", session=Session(), enrich_contacts=False)
    assert result["query"] == "Titanium Dioxide"
    assert result["buyers"][0]["title"] == "Buyer Company"
    assert result["sellers"][0]["title"] == "Seller Company"
    assert "Unverified prospect" in result["buyers"][0]["verification"]
