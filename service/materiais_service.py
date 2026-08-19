from repository.materiais_repository import (
    atualizar_material,
    buscar_materiais as buscar_materiais_repository,
    excluir_material as excluir_material_repository,
    inserir_material,
    listar_materiais as listar_materiais_repository,
    obter_material as obter_material_repository,
)


def listar_materiais():
    return listar_materiais_repository()


def buscar_materiais(termo):
    return buscar_materiais_repository(termo)


def obter_material(id_produto):
    return obter_material_repository(id_produto)


def excluir_material(id_produto):
    return excluir_material_repository(id_produto)


def salvar_material(dados, id_produto=None):
    tipo = str(dados.get("tipo", "")).strip()
    if not tipo:
        raise ValueError("O campo Tipo e obrigatorio.")

    quantidade_texto = str(dados.get("quantidade", "")).strip()
    try:
        quantidade = int(quantidade_texto) if quantidade_texto else 0
    except ValueError as e:
        raise ValueError("A quantidade deve ser um numero inteiro.") from e

    dados_normalizados = {"tipo": tipo, "quantidade": quantidade}
    if id_produto is not None:
        return atualizar_material(id_produto, dados_normalizados)
    return inserir_material(dados_normalizados)