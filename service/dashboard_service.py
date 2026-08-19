from repository.dashboard_repository import obter_indicadores


def obter_indicadores_dashboard():
    try:
        indicadores = obter_indicadores()
        return {
            "servicos_agendados": indicadores["servicos_agendados"],
            "servicos_realizados": indicadores["servicos_realizados"],
            "clientes": indicadores["clientes"],
            "veiculos": indicadores["veiculos"],
            "total_recebido": float(indicadores["total_recebido"]),
        }
    except Exception:
        return {
            "servicos_agendados": 0,
            "servicos_realizados": 0,
            "clientes": 0,
            "veiculos": 0,
            "total_recebido": 0.0,
        }