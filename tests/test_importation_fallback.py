from app.utils.fallback import load_importation_csv

def test_fallback_returns_data_for_valid_year_and_type():
    data = load_importation_csv(2022, "subopt_01")
    assert isinstance(data, list)
    assert len(data) > 0

    sample = data[0]
    assert "Country" in sample
    assert "Quantity (kg)" in sample
    assert "Value (US$)" in sample
    assert "Year" in sample
    assert "Type" in sample
