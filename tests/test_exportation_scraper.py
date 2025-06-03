from app.services.exportation import EXPORT_TYPE_TO_SUBOPT, fetch_exportation_data
from app.models.exportation_types import ExportTypeEnum


def test_exportation_scraping_valid_year_and_type():
    year = 2022
    export_type = ExportTypeEnum.vinhos_de_mesa.value
    export_type_code = EXPORT_TYPE_TO_SUBOPT[export_type]
    data = fetch_exportation_data(year, export_type_code)

    assert isinstance(data, list)
    assert len(data) > 0

    sample = data[0]
    assert "Country" in sample
    assert "Quantity (kg)" in sample
    assert "Value (US$)" in sample
    assert "Year" in sample
    assert "Type" in sample
