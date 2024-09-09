import os
import psycopg2

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from query import CREATE_USERS_TABLE, INSERT_USERS_TABLE, SELECT_ALL_USERS, DELETE_USER

from utils.email import enviar_email, retornar_assunto_exclusao
from utils.request import extrair_dados
from utils.response import retornar_erro

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/enviar_email', methods=['POST'])
def api_enviar_email():
    data = request.get_json()
    dados_email = extrair_dados(data, ["destinatario", "assunto", "corpo"])
    destinatario, assunto, corpo = dados_email["destinatario"], dados_email["assunto"], dados_email["corpo"]

    if not destinatario or not assunto or not corpo:
        return jsonify({'message': 'Dados insuficientes'}), 400
    
    enviar_email(destinatario, assunto, corpo)
    return jsonify({'message': 'E-mail enviado com sucesso!'}), 200

@app.post('/user')
def create_user():
    data = request.get_json()

    dados_usuario = extrair_dados(data, ["destinatario", "assunto", "corpo"])
    name, email, password = dados_usuario["name"], dados_usuario["email"], dados_usuario["password"]

    if not name or not email or not password:
        return jsonify({'message': 'Nome, e-mail e senha são necessários!'}), 400
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USERS_TABLE, (name, email, password))
            user_id = cursor.fetchone()[0]

    assunto = "Bem-vindo ao nosso sistema"
    corpo = f"Olá {name},\n\nSeu usuário foi criado com sucesso!\n\nBem-vindo!"
    enviar_email(email, assunto, corpo)
    
    return {"id": user_id, "message": f"User {name} created!"}, 201

@app.get("/user")
def list_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_USERS)
            users = cursor.fetchall()
            response = list(map(lambda user: {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "password": user[3]
                }, users))
    return response, 200 

@app.delete('/user/<int:user_id>')
def delete_user(user_id):
    try:
        with connection:
            with connection.cursor() as cursor:
                error_msg = 'Usuário não encontrado'
                codigo_not_found = 404
                
                # REFATORAR A QUERY PARA DENTRO DO ARQUIVO QUERY.PY
                cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                
                if result is None:
                    return retornar_erro(error_msg, codigo_not_found)
                
                email = result[0]
                
                
                cursor.execute(DELETE_USER, (user_id,))
                if cursor.rowcount == 0:
                    return retornar_erro(error_msg, codigo_not_found)
                
                
                assunto, corpo = retornar_assunto_exclusao(user_id)
                enviar_email(email, assunto, corpo)
                
                return jsonify({'message': f'Usuário com ID {user_id} excluído com sucesso!'}), 200
    except psycopg2.Error as db_error:
        return jsonify({'message': f'Erro de banco de dados: {db_error}'}), 500
    except Exception as e:
        return jsonify({'message': f'Erro ao excluir o usuário: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)