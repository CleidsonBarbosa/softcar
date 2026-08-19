import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "softcar_novo",
}


def conectar():
    return mysql.connector.connect(**DB_CONFIG)

