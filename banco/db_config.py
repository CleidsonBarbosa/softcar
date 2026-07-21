import mysql.connector
import os
from mysql.connector import Error

DB_CONFIG = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '',
    'database' : 'softcar'
}

def verifica_login():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            senha=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )

        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM usuarios WHERE nome = %s ADN senha = %s", (usuario,senha))
        resultado = cursor.retchome()
        conn.close()

        return resultado
        
    except Error as e:
        print(f"error ao verificar login:{e}")
        return None
        
