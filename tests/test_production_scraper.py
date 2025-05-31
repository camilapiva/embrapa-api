from app.services.production import fetch_production_data

def test_scraping_returns_data_for_valid_year():
    year = 2022
    data = fetch_production_data(year)

    assert isinstance(data, list)
    assert len(data) > 0

    # Show the first 3 logs for debugging if it fails again
    print(data[:3])

    # Validates if the expected data exists
    valid = [
        item for item in data
        if isinstance(item, dict)
        and "Product" in item
        and "Quantity (L.)" in item
        and "Year" in item
    ]

    assert len(valid) > 0
