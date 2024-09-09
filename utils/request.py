def extrair_dados(dados, lista_atributos):
  resposta = {}
  for atributo in lista_atributos:
    resposta.update({atributo: dados.get(atributo)})
  
  return resposta