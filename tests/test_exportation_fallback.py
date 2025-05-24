from app.utils.fallback import load_exportation_csv

def test_exportation_fallback_valid_year_and_type():
    year = 2022
    export_type = "subopt_01"
    data = load_exportation_csv(year, export_type)

    assert isinstance(data, list)
    assert len(data) > 0
    sample = data[0]
    assert "Country" in sample
    assert "Quantity (kg)" in sample
    assert "Value (US$)" in sample
    assert "Year" in sample
    assert "Type" in sample
