from src.search import suggest_products, item_dossier_plan


def test_alias_search_finds_common_item_names():
    rows = suggest_products("haldi")
    assert rows
    assert rows[0]["product_id"] == "turmeric"
    assert rows[0]["match_reason"] == "exact_match"


def test_category_search_returns_multiple_sectors():
    rows = suggest_products("metals")
    assert rows
    assert all(row["category"] == "Metals" for row in rows)


def test_unmapped_product_does_not_invent_hs_code():
    rows = suggest_products("pharma lactose")
    assert rows[0]["product_id"] == "pharma_lactose"
    assert rows[0]["hs_codes"] == []
    assert rows[0]["status"] == "classification_required_check_purity_and_form"


def test_unknown_product_returns_no_false_match():
    assert suggest_products("xyzqv unrelated item") == []


def test_dossier_marks_new_product():
    result = item_dossier_plan("xyzqv unrelated item")
    assert result["catalogue_match_status"] == "new_item"
