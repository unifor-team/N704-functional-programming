import os
import psycopg2
import smtplib
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from query import CREATE_USERS_TABLE, INSERT_USERS_TABLE, SELECT_ALL_USERS, DELETE_USER
import email.message



load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

def enviar_email(destinatario, assunto, corpo):
    remetente = os.getenv('EMAIL_REMETENTE')
    senha = 'okqiptypzmixqtqr'
    
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)
    
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        servidor.quit()

        print(f"E-mail enviado para {destinatario} com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

@app.route('/enviar_email', methods=['POST'])
def api_enviar_email():
    data = request.get_json()
    destinatario = data.get('destinatario')
    assunto = data.get('assunto')
    corpo = data.get('corpo')
    
    if not destinatario or not assunto or not corpo:
        return jsonify({'message': 'Dados insuficientes'}), 400
    
    enviar_email(destinatario, assunto, corpo)
    return jsonify({'message': 'E-mail enviado com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)

@app.post('/user')
def create_user():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]

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
            print(users)
            response = []
            for user in users:
                each_user = {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "password": user[3]
                }
                response.append(each_user)
    return response, 200 

@app.delete('/user/<int:user_id>')
def delete_user(user_id):
    try:
        with connection:
            with connection.cursor() as cursor:
                
                cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                
                if result is None:
                    return jsonify({'message': 'Usuário não encontrado'}), 404
                
                email = result[0]
                
                
                cursor.execute(DELETE_USER, (user_id,))
                if cursor.rowcount == 0:
                    return jsonify({'message': 'Usuário não encontrado'}), 404
                
                
                assunto = "Conta excluída"
                corpo = f"Olá,\n\nSua conta com o ID {user_id} foi excluída com sucesso."
                enviar_email(email, assunto, corpo)
                
                return jsonify({'message': f'Usuário com ID {user_id} excluído com sucesso!'}), 200
    except psycopg2.Error as db_error:
        return jsonify({'message': f'Erro de banco de dados: {db_error}'}), 500
    except Exception as e:
        return jsonify({'message': f'Erro ao excluir o usuário: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)