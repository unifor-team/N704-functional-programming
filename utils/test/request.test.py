import unittest
from request import extrair_dados

class testApp(unittest.TestCase):
    def test_extrair_dados_sem_atributos(self):

        mock_data = {
            "id": 1,
            "nome": "João Silva",
            "idade": 30
        }
      
        dados = extrair_dados(mock_data, [])
        self.assertEqual(dados, dados)

    def test_extrair_dados_sem_entradas(self):
        mock_dados ={
        }
        noData = extrair_dados(mock_dados, [])
        self.assertEqual(noData, 0)

    def test_true(self):
        self.assertTrue(False) 
        
if __name__ == '__main__':
    unittest.main()