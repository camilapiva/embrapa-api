from app.utils.fallback import load_production_csv

def test_fallback_returns_data_for_valid_year():
    year = 2022
    data = load_production_csv(year)

    assert isinstance(data, list), "Expected fallback to return a list"
    assert len(data) > 0, "Data list is empty"

    # Filter only the selected year
    filtered = [item for item in data if item.get("Year") == year]
    assert len(filtered) > 0, f"No data found for year {year}"

    # Check structure of a sample item
    sample = filtered[0]
    assert "Product" in sample
    assert "Quantity (L.)" in sample
    assert "Year" in sample

    # Check if total row exists
    assert any(item.get("Product") == "Total" for item in filtered), "'Total' row not found for the year"
