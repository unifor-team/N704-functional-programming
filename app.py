import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from query import CREATE_USERS_TABLE, INSERT_USERS_TABLE, SELECT_ALL_USERS

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post('/user')
def create_user():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USERS_TABLE, (name, email, password))
            user_id = cursor.fetchone()[0]
    
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)