from banco.db_config import conectar


def listar_materiais():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_produto, tipo, quantidade FROM estoque ORDER BY tipo")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def buscar_materiais(termo):
    conn = conectar()
    cursor = conn.cursor()
    try:
        if termo:
            cursor.execute(
                "SELECT id_produto, tipo, quantidade FROM estoque WHERE tipo LIKE %s ORDER BY tipo",
                (f"%{termo}%",)
            )
        else:
            cursor.execute("SELECT id_produto, tipo, quantidade FROM estoque ORDER BY tipo")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def obter_material(id_produto):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM estoque WHERE id_produto = %s", (id_produto,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def excluir_material(id_produto):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM estoque WHERE id_produto = %s", (id_produto,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def inserir_material(dados):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO estoque (tipo, quantidade) VALUES (%s, %s)",
            (dados["tipo"], dados["quantidade"])
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def atualizar_material(id_produto, dados):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE estoque SET tipo=%s, quantidade=%s WHERE id_produto=%s",
            (dados["tipo"], dados["quantidade"], id_produto)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()