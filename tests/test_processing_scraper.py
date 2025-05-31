from app.services.processing import fetch_processing_data

def test_scraping_returns_data_for_valid_year_and_type():
    year = 2022
    grape_type = "subopt_01"
    data = fetch_processing_data(year, grape_type)

    assert isinstance(data, list)
    assert len(data) > 0

    # Check structure of the data
    sample = data[0]
    assert "Category" in sample
    assert "Cultivar" in sample
    assert "Quantity (kg)" in sample
    assert "Year" in sample
