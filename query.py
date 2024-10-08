CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, email TEXT, password TEXT);"
)

INSERT_USERS_TABLE = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;"

SELECT_ALL_USERS = "SELECT * FROM users"

DELETE_USER = "DELETE FROM users WHERE id = %s"

SELECT_EMAIL_BY_ID = "SELECT email FROM users WHERE id = %s"