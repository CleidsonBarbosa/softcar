from banco.db_config import conectar


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco "
            "FROM clientes ORDER BY nome_cliente"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def buscar_clientes(termo):
    conn = conectar()
    cursor = conn.cursor()
    try:
        if termo:
            cursor.execute(
                "SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco "
                "FROM clientes WHERE nome_cliente LIKE %s OR email_cliente LIKE %s OR cpf LIKE %s "
                "ORDER BY nome_cliente",
                (f"%{termo}%", f"%{termo}%", f"%{termo}%")
            )
        else:
            cursor.execute(
                "SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco "
                "FROM clientes ORDER BY nome_cliente"
            )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def obter_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def excluir_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def atualizar_cliente(id_cliente, valores):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE clientes SET nome_cliente=%s, email_cliente=%s, telefone_cliente=%s, "
            "cpf=%s, endereco=%s, data_nascimento=%s WHERE id_cliente=%s",
            (
                valores["nome_cliente"], valores["email_cliente"], valores["telefone_cliente"],
                valores["cpf"], valores["endereco"], valores["data_nascimento"], id_cliente,
            )
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def inserir_cliente(valores):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO clientes (nome_cliente, email_cliente, telefone_cliente, cpf, endereco, data_nascimento) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (
                valores["nome_cliente"], valores["email_cliente"], valores["telefone_cliente"],
                valores["cpf"], valores["endereco"], valores["data_nascimento"],
            )
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()