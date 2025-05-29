from app.utils.fallback import load_importation_csv
from app.models.importation_types import ImportTypeEnum

def test_fallback_returns_data_for_valid_year_and_type():
    year = 2022
    import_type = ImportTypeEnum.vinhos_de_mesa.value
    data = load_importation_csv(year, import_type)
    
    assert isinstance(data, list)
    assert len(data) > 0

    sample = data[0]
    assert "Country" in sample
    assert "Quantity (kg)" in sample
    assert "Value (US$)" in sample
    assert "Year" in sample
    assert "Type" in sample
