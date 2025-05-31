from app.repositories.fallback import load_commercialization_csv

def test_fallback_returns_data_for_valid_year():
    year = 2022
    data = load_commercialization_csv(year)

    assert isinstance(data, list)
    assert len(data) > 0

    sample = data[0]
    assert "Category" in sample
    assert "Product" in sample
    assert "Quantity (L.)" in sample
    assert "Year" in sample
    assert sample["Year"] == year
