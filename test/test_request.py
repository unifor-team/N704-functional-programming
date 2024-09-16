import sys
import os
from utils.request import extrair_dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    
def test_extrair_dados_com_todos_os_dados():
    mock_data = {
    "id": 1,
    "nome": "João Silva",
    "idade": 30
    }
    dados_pessoa = extrair_dados(mock_data, ["id", "nome", "idade"])    
    assert dados_pessoa == mock_data

