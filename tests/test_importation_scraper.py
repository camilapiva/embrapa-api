from app.services.exportation import EXPORT_TYPE_TO_SUBOPT
from app.services.importation import fetch_importation_data
from app.models.importation_types import ImportTypeEnum


def test_scraping_returns_data_for_valid_year_and_type():
    year = 2022
    import_type = ImportTypeEnum.vinhos_de_mesa.value
    import_type_code = EXPORT_TYPE_TO_SUBOPT[import_type]
    data = fetch_importation_data(year, import_type_code)

    assert isinstance(data, list)
    assert len(data) > 0

    sample = data[0]
    assert "Country" in sample
    assert "Quantity (kg)" in sample
    assert "Value (US$)" in sample
    assert "Year" in sample
    assert "Type" in sample
