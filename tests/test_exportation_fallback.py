from app.repositories.fallback import load_exportation_csv
from app.models.exportation_types import ExportTypeEnum


def test_exportation_fallback_valid_year_and_type():
    year = 2022
    export_type = ExportTypeEnum.vinhos_de_mesa.value
    data = load_exportation_csv(year, export_type)

    assert isinstance(data, list)
    assert len(data) > 0

    sample = data[0]
    assert "Country" in sample
    assert "Quantity (kg)" in sample
    assert "Value (US$)" in sample
    assert "Year" in sample
    assert "Type" in sample
