from banco.db_config import conectar


def autenticar_funcionario(email, senha):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_func, nome_func, cargo FROM funcionarios "
            "WHERE email_func = %s AND senha = %s",
            (email, senha)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()