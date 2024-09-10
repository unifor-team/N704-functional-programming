import os
import psycopg2

from dotenv import load_dotenv
from flask import Flask, request
from query import CREATE_USERS_TABLE, INSERT_USERS_TABLE, SELECT_ALL_USERS, DELETE_USER, SELECT_EMAIL_BY_ID

from utils.email import enviar_email, retornar_assunto_exclusao, retornar_assunto_criacao
from utils.request import extrair_dados
from utils.response import retornar_resposta

from status_code import NOT_FOUND, OK, CREATED, BAD_REQUEST
from response_msg import EMAIL_SUCCESSS, INSUFICIENT_MSG, USER_ERROR_MSG, USER_DELETED, USER_ERRO_DELETE, USER_CREATED

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

if __name__ == '__main__':
    app.run(debug=True)

response = retornar_resposta()

@app.route('/enviar_email', methods=['POST'])
def api_enviar_email():
    data = request.get_json()
    dados_email = extrair_dados(data, ["destinatario", "assunto", "corpo"])
    destinatario, assunto, corpo = dados_email["destinatario"], dados_email["assunto"], dados_email["corpo"]

    if not destinatario or not assunto or not corpo:
        return response(INSUFICIENT_MSG, BAD_REQUEST)
    
    enviar_email(destinatario, assunto, corpo)
    return response(EMAIL_SUCCESSS, OK)

@app.post('/user')
def create_user():
    data = request.get_json()

    dados_usuario = extrair_dados(data, ["destinatario", "assunto", "corpo"])
    name, email, password = dados_usuario["name"], dados_usuario["email"], dados_usuario["password"]

    if not name or not email or not password:
        return response(INSUFICIENT_MSG, BAD_REQUEST)
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USERS_TABLE, (name, email, password))

    assunto, corpo = retornar_assunto_criacao()
    enviar_email(email, assunto, corpo)
    
    return response(USER_CREATED, CREATED)

@app.get("/user")
def list_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_USERS)
            users = cursor.fetchall()
            #lambda function e high order function
            response_list = list(map(lambda user: {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "password": user[3]
                }, users))
    return response(response_list, BAD_REQUEST)

@app.get("/user_whitout_password")
def list_users_whitout_password():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_USERS)
            users = cursor.fetchall()
            # list comprehension
            response_list = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]

    return response(response_list, BAD_REQUEST)

@app.delete('/user/<int:user_id>')
def delete_user(user_id):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_EMAIL_BY_ID, (user_id,))
                result = cursor.fetchone()
                
                if result is None:
                    return response(USER_ERROR_MSG, NOT_FOUND)
                
                email = result[0]
                             
                cursor.execute(DELETE_USER, (user_id,))
                if cursor.rowcount == 0:
                    return response(USER_ERROR_MSG, NOT_FOUND)
                
                assunto, corpo = retornar_assunto_exclusao(user_id)
                enviar_email(email, assunto, corpo)
                
                return response(USER_DELETED(user_id), OK)
    except Exception as e:
        return response(USER_ERRO_DELETE(e), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)