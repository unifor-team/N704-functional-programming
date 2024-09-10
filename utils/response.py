import json

# closure
def retornar_resposta():
    def criar_json(msg: str, codigo: int):
        return json.dumps({'message': msg}), codigo
    return criar_json
