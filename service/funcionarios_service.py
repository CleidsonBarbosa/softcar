from repository.funcionarios_repository import (
    atualizar_funcionario,
    buscar_funcionarios as buscar_funcionarios_repository,
    excluir_funcionario as excluir_funcionario_repository,
    inserir_funcionario,
    listar_funcionarios as listar_funcionarios_repository,
    obter_funcionario as obter_funcionario_repository,
)


def listar_funcionarios():
    return listar_funcionarios_repository()


def buscar_funcionarios(termo):
    return buscar_funcionarios_repository(termo)


def obter_funcionario(id_func):
    return obter_funcionario_repository(id_func)


def excluir_funcionario(id_func):
    return excluir_funcionario_repository(id_func)


def salvar_funcionario(dados, id_func=None):
    if not dados.get("nome_func") or not dados.get("email_func"):
        raise ValueError("Nome e E-mail sao obrigatorios.")
    if id_func is None and not dados.get("senha"):
        raise ValueError("A senha e obrigatoria para novos funcionarios.")

    if id_func is None:
        return inserir_funcionario(dados)
    return atualizar_funcionario(id_func, dados)