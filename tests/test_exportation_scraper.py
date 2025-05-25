from app.scraping.exportation import fetch_exportation_data

def test_exportation_scraping_valid_year_and_type():
    year = 2022
    export_type = "subopt_01"
    data = fetch_exportation_data(year, export_type)

    assert isinstance(data, list)
    assert len(data) > 0

    # Check structure of the data
    sample = data[0]
    assert "Country" in sample
    assert "Quantity (kg)" in sample
    assert "Value (US$)" in sample
    assert "Year" in sample
    assert "Type" in sample
