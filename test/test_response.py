import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.response import retornar_resposta

def test_retornar_resposta_com_dados():
    mensagem_esperada = "test"
    codigo_esperado = 200
    resposta = retornar_resposta()
    (message, code) = resposta(mensagem_esperada, codigo_esperado)

    message = json.loads(message)

    assert code == codigo_esperado
    assert message['message'] ==  mensagem_esperada

def test_retornar_resposta_sem_codigo():
    mensagem_esperada = "test"
    codigo_esperado = None
    resposta = retornar_resposta()
    (message, code) = resposta(mensagem_esperada, codigo_esperado)

    message = json.loads(message)

    assert code == codigo_esperado
    assert message['message'] ==  mensagem_esperada

def test_retornar_resposta_sem_mensagem():
    mensagem_esperada = None
    codigo_esperado = 200
    resposta = retornar_resposta()
    (message, code) = resposta(mensagem_esperada, codigo_esperado)

    message = json.loads(message)

    assert code == codigo_esperado
    assert message['message'] ==  mensagem_esperada      
