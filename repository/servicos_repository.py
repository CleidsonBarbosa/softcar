from banco.db_config import conectar


def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_servico, nome_servico, preco_servico "
            "FROM servicos ORDER BY nome_servico"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def buscar_servicos(termo):
    conn = conectar()
    cursor = conn.cursor()
    try:
        if termo:
            cursor.execute(
                "SELECT id_servico, nome_servico, preco_servico FROM servicos "
                "WHERE nome_servico LIKE %s ORDER BY nome_servico",
                (f"%{termo}%",)
            )
        else:
            cursor.execute(
                "SELECT id_servico, nome_servico, preco_servico "
                "FROM servicos ORDER BY nome_servico"
            )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def obter_servico(id_servico):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM servicos WHERE id_servico = %s", (id_servico,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def excluir_servico(id_servico):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM servicos WHERE id_servico = %s", (id_servico,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def inserir_servico(dados):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO servicos (nome_servico, preco_servico) VALUES (%s,%s)",
            (dados["nome_servico"], dados["preco_servico"])
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def atualizar_servico(id_servico, dados):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE servicos SET nome_servico=%s, preco_servico=%s WHERE id_servico=%s",
            (dados["nome_servico"], dados["preco_servico"], id_servico)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()