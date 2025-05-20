from app.utils.fallback import load_production_csv

def test_fallback_returns_data_for_valid_year():
    year = 2022
    data = load_production_csv(year)

    assert isinstance(data, list), "Esperado que o fallback retorne uma lista"
    assert len(data) > 0, "A lista de dados está vazia"

    # Filtra apenas o ano solicitado
    filtered = [item for item in data if item.get("Ano") == year]
    assert len(filtered) > 0, f"Nenhum dado encontrado para o ano {year}"

    # Verifica estrutura de um item
    sample = filtered[0]
    assert "Produto" in sample
    assert "Quantidade (L.)" in sample
    assert "Ano" in sample

    # Verifica se a linha de total está presente
    assert any(item.get("Produto") == "Total" for item in filtered), "Linha 'Total' não encontrada para o ano"
