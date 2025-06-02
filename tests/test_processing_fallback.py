from app.repositories.fallback import load_processing_csv
from app.models.processing_types import GrapeTypeEnum


def test_fallback_returns_data_for_valid_year_and_type():
    year = 2022
    grape_type = GrapeTypeEnum.viniferas.value
    data = load_processing_csv(year, grape_type)

    assert isinstance(data, list)
    assert len(data) > 0

    # Check structure of the data
    sample = data[0]
    assert "Category" in sample
    assert "Cultivar" in sample
    assert "Quantity (kg)" in sample
    assert "Year" in sample
    assert "GrapeType" in sample
