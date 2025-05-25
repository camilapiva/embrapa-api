from app.scraping.production import fetch_production_data

def test_scraping_returns_data_for_valid_year():
    year = 2022
    data = fetch_production_data(year)

    assert isinstance(data, list)
    assert len(data) > 0

    # Mostra os 3 primeiros registros para debug se falhar novamente
    print(data[:3])

    # Valida se os dados esperados existem (resiliente)
    valid = [
        item for item in data
        if isinstance(item, dict)
        and "Product" in item
        and "Quantity (L.)" in item
        and "Year" in item
    ]

    assert len(valid) > 0
