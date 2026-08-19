USE softcar_novo;

INSERT INTO funcionarios (
    nome_func, email_func, cpf_func, senha, cargo,
    endereco_func, data_nascimento_func, telefone_func
)
VALUES (
    'Administrador Softcar',
    'admin@softcar.com',
    '00000000000',
    '123456',
    'atendente',
    'Sede Softcar',
    '1990-01-01',
    '11999999999'
)
ON DUPLICATE KEY UPDATE
    nome_func = VALUES(nome_func),
    senha = VALUES(senha),
    cargo = VALUES(cargo);

INSERT INTO clientes (nome_cliente, email_cliente, telefone_cliente, cpf, endereco, data_nascimento)
VALUES ('Cliente Seed', 'cliente@softcar.com', '11988888888', '11111111111', 'Sede Softcar', '1995-01-01')
ON DUPLICATE KEY UPDATE nome_cliente = VALUES(nome_cliente);

INSERT INTO estoque (tipo, quantidade)
VALUES ('Material inicial', 10);

INSERT INTO servicos (nome_servico, preco_servico)
VALUES ('Lavagem simples', 30.00);