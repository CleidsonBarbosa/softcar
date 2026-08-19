from repository.servico_execucao_repository import (
    buscar_ordens as buscar_ordens_repository,
    excluir_ordem as excluir_ordem_repository,
    finalizar_ordem as finalizar_ordem_repository,
    listar_itens_ordem as listar_itens_ordem_repository,
    listar_ordens as listar_ordens_repository,
)


def listar_ordens():
    return listar_ordens_repository()


def buscar_ordens(termo):
    return buscar_ordens_repository(termo)


def finalizar_ordem(id_ordem, status):
    if status == "finalizado":
        raise ValueError("Esta ordem ja foi finalizada.")
    return finalizar_ordem_repository(id_ordem)


def excluir_ordem(id_ordem):
    return excluir_ordem_repository(id_ordem)


def listar_itens_ordem(id_ordem):
    return listar_itens_ordem_repository(id_ordem)