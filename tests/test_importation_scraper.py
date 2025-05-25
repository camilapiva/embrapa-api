from app.scraping.importation import fetch_importation_data

def test_scraping_returns_data_for_valid_year_and_type():
    data = fetch_importation_data(2022, "subopt_01")
    assert isinstance(data, list)
    assert len(data) > 0

    sample = data[0]
    assert "Country" in sample
    assert "Quantity (kg)" in sample
    assert "Value (US$)" in sample
    assert "Year" in sample
    assert "Type" in sample
