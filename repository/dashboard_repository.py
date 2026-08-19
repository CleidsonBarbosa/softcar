from banco.db_config import conectar


def obter_indicadores():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'aberto'")
        servicos_agendados = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'finalizado'")
        servicos_realizados = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM clientes")
        clientes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM carros")
        veiculos = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ordem_servico WHERE status = 'finalizado'")
        total_recebido = cursor.fetchone()[0]

        return {
            "servicos_agendados": servicos_agendados,
            "servicos_realizados": servicos_realizados,
            "clientes": clientes,
            "veiculos": veiculos,
            "total_recebido": total_recebido,
        }
    finally:
        cursor.close()
        conn.close()