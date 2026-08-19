from repository.servicos_repository import (
    atualizar_servico,
    buscar_servicos as buscar_servicos_repository,
    excluir_servico as excluir_servico_repository,
    inserir_servico,
    listar_servicos as listar_servicos_repository,
    obter_servico as obter_servico_repository,
)


def listar_servicos():
    return listar_servicos_repository()


def buscar_servicos(termo):
    return buscar_servicos_repository(termo)


def obter_servico(id_servico):
    return obter_servico_repository(id_servico)


def excluir_servico(id_servico):
    return excluir_servico_repository(id_servico)


def salvar_servico(dados, id_servico=None):
    nome = str(dados.get("nome_servico", "")).strip()
    if not nome:
        raise ValueError("O campo Nome e obrigatorio.")

    preco_texto = str(dados.get("preco_servico", "")).strip()
    try:
        preco = float(preco_texto.replace(",", ".")) if preco_texto else None
    except ValueError as e:
        raise ValueError("O preco deve ser um numero valido.") from e

    dados_normalizados = {"nome_servico": nome, "preco_servico": preco}
    if id_servico is not None:
        return atualizar_servico(id_servico, dados_normalizados)
    return inserir_servico(dados_normalizados)