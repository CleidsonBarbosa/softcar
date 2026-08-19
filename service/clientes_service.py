from repository.clientes_repository import (
    atualizar_cliente,
    buscar_clientes as buscar_clientes_repository,
    excluir_cliente as excluir_cliente_repository,
    inserir_cliente,
    listar_clientes as listar_clientes_repository,
    obter_cliente as obter_cliente_repository,
)


def listar_clientes():
    return listar_clientes_repository()


def buscar_clientes(termo):
    return buscar_clientes_repository(termo)


def obter_cliente(id_cliente):
    return obter_cliente_repository(id_cliente)


def excluir_cliente(id_cliente):
    return excluir_cliente_repository(id_cliente)


def salvar_cliente(valores, id_cliente=None):
    if not valores.get("nome_cliente"):
        raise ValueError("O campo nome_cliente e obrigatorio.")
    if not valores.get("cpf"):
        raise ValueError("O campo cpf e obrigatorio.")

    if id_cliente is not None:
        return atualizar_cliente(id_cliente, valores)
    return inserir_cliente(valores)