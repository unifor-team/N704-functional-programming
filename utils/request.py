#dict comprehension
def extrair_dados(dados, lista_atributos):
    return {atributo: dados.get(atributo) for atributo in lista_atributos}
