from flask import jsonify

# closure
def retornar_resposta():
    def criar_json(msg: str, codigo: int):
        return jsonify({'message': msg}), codigo
    return criar_json
