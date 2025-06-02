from app.services.commercialization import fetch_commercialization_data


def test_scraping_returns_data_for_valid_year():
    year = 2022
    data = fetch_commercialization_data(year)

    assert isinstance(data, list)
    assert len(data) > 0

    # Check structure of the data
    sample = data[0]
    assert "Category" in sample
    assert "Product" in sample
    assert "Quantity (L.)" in sample
    assert "Year" in sample
