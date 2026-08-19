from banco.db_config import conectar


def listar_ordens():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_ordem, id_cliente, total, status, data_hora "
            "FROM ordem_servico ORDER BY id_ordem DESC"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def buscar_ordens(termo):
    conn = conectar()
    cursor = conn.cursor()
    try:
        if termo:
            cursor.execute(
                "SELECT id_ordem, id_cliente, total, status, data_hora FROM ordem_servico "
                "WHERE status LIKE %s OR id_ordem LIKE %s ORDER BY id_ordem DESC",
                (f"%{termo}%", f"%{termo}%")
            )
        else:
            cursor.execute(
                "SELECT id_ordem, id_cliente, total, status, data_hora "
                "FROM ordem_servico ORDER BY id_ordem DESC"
            )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def finalizar_ordem(id_ordem):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE ordem_servico SET status = 'finalizado' WHERE id_ordem = %s",
            (id_ordem,)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def excluir_ordem(id_ordem):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ordem_servico_itens WHERE id_ordem = %s", (id_ordem,))
        cursor.execute("DELETE FROM ordem_servico WHERE id_ordem = %s", (id_ordem,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def listar_itens_ordem(id_ordem):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT osi.id_item, osi.id_servico, s.nome_servico, osi.preco "
            "FROM ordem_servico_itens osi "
            "LEFT JOIN servicos s ON s.id_servico = osi.id_servico "
            "WHERE osi.id_ordem = %s",
            (id_ordem,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()