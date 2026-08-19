from banco.db_config import conectar


def listar_funcionarios():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_func, nome_func, email_func, cargo, telefone_func "
            "FROM funcionarios ORDER BY nome_func"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def buscar_funcionarios(termo):
    conn = conectar()
    cursor = conn.cursor()
    try:
        if termo:
            cursor.execute(
                "SELECT id_func, nome_func, email_func, cargo, telefone_func "
                "FROM funcionarios WHERE nome_func LIKE %s OR email_func LIKE %s OR cargo LIKE %s "
                "ORDER BY nome_func",
                (f"%{termo}%", f"%{termo}%", f"%{termo}%")
            )
        else:
            cursor.execute(
                "SELECT id_func, nome_func, email_func, cargo, telefone_func "
                "FROM funcionarios ORDER BY nome_func"
            )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def obter_funcionario(id_func):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM funcionarios WHERE id_func = %s", (id_func,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def excluir_funcionario(id_func):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM funcionarios WHERE id_func = %s", (id_func,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def inserir_funcionario(dados):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO funcionarios (nome_func, email_func, senha, cargo, telefone_func, cpf_func, endereco_func) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (
                dados["nome_func"], dados["email_func"], dados["senha"], dados["cargo"],
                dados["telefone_func"], dados["cpf_func"], dados["endereco_func"],
            )
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def atualizar_funcionario(id_func, dados):
    conn = conectar()
    cursor = conn.cursor()
    try:
        if dados["senha"]:
            cursor.execute(
                "UPDATE funcionarios SET nome_func=%s, email_func=%s, senha=%s, cargo=%s, "
                "telefone_func=%s, cpf_func=%s, endereco_func=%s WHERE id_func=%s",
                (
                    dados["nome_func"], dados["email_func"], dados["senha"], dados["cargo"],
                    dados["telefone_func"], dados["cpf_func"], dados["endereco_func"], id_func,
                )
            )
        else:
            cursor.execute(
                "UPDATE funcionarios SET nome_func=%s, email_func=%s, cargo=%s, telefone_func=%s, "
                "cpf_func=%s, endereco_func=%s WHERE id_func=%s",
                (
                    dados["nome_func"], dados["email_func"], dados["cargo"], dados["telefone_func"],
                    dados["cpf_func"], dados["endereco_func"], id_func,
                )
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()