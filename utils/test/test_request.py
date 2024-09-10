from request import extrair_dados

def test_extrair():
    mock_data = {
            "id": 1,
            "nome": "João Silva",
            "idade": 30
        }
    assert mock_data == 0