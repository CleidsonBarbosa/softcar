from repository.login_repository import autenticar_funcionario


def realizar_login(email, senha):
    email = str(email or "").strip()
    senha = str(senha or "").strip()

    if not email or not senha:
        raise ValueError("Por favor, preencha todos os campos.")

    return autenticar_funcionario(email, senha)