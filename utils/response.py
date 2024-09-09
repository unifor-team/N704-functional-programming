from flask import jsonify

def retornar_erro(msg, codigo):
  return jsonify({'message': msg}), codigo