import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "softcar",
}


def conectar():
    return mysql.connector.connect(**DB_CONFIG)

