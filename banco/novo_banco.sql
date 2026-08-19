CREATE DATABASE IF NOT EXISTS softcar_novo
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE softcar_novo;

CREATE TABLE IF NOT EXISTS funcionarios (
    id_func INT NOT NULL AUTO_INCREMENT,
    nome_func VARCHAR(80) NOT NULL,
    email_func VARCHAR(120) NOT NULL,
    cpf_func CHAR(11) NULL,
    senha VARCHAR(255) NOT NULL,
    cargo VARCHAR(30) NOT NULL DEFAULT 'atendente',
    endereco_func VARCHAR(150) NULL,
    data_nascimento_func DATE NULL,
    telefone_func VARCHAR(20) NULL,
    PRIMARY KEY (id_func),
    UNIQUE KEY uq_funcionarios_email (email_func),
    UNIQUE KEY uq_funcionarios_cpf (cpf_func)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT NOT NULL AUTO_INCREMENT,
    nome_cliente VARCHAR(80) NOT NULL,
    email_cliente VARCHAR(120) NULL,
    telefone_cliente VARCHAR(20) NULL,
    cpf CHAR(11) NULL,
    endereco VARCHAR(150) NULL,
    data_nascimento DATE NULL,
    PRIMARY KEY (id_cliente),
    UNIQUE KEY uq_clientes_cpf (cpf)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS carros (
    id_carro INT NOT NULL AUTO_INCREMENT,
    placa CHAR(7) NOT NULL,
    modelo VARCHAR(45) NULL,
    marca VARCHAR(45) NULL,
    cor VARCHAR(45) NULL,
    PRIMARY KEY (id_carro),
    UNIQUE KEY uq_carros_placa (placa)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS clientes_has_carros (
    clientes_id_cliente INT NOT NULL,
    carros_id_carro INT NOT NULL,
    PRIMARY KEY (clientes_id_cliente, carros_id_carro),
    CONSTRAINT fk_clientes_carros_cliente FOREIGN KEY (clientes_id_cliente)
        REFERENCES clientes (id_cliente) ON DELETE CASCADE,
    CONSTRAINT fk_clientes_carros_carro FOREIGN KEY (carros_id_carro)
        REFERENCES carros (id_carro) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS estoque (
    id_produto INT NOT NULL AUTO_INCREMENT,
    tipo VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id_produto),
    CONSTRAINT chk_estoque_quantidade CHECK (quantidade >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS servicos (
    id_servico INT NOT NULL AUTO_INCREMENT,
    nome_servico VARCHAR(100) NOT NULL,
    preco_servico DECIMAL(10,2) NULL,
    estoque_id_produto INT NULL,
    data_hora_servico DATETIME NULL,
    PRIMARY KEY (id_servico),
    CONSTRAINT fk_servicos_estoque FOREIGN KEY (estoque_id_produto)
        REFERENCES estoque (id_produto) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ordem_servico (
    id_ordem INT NOT NULL AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_carro INT NULL,
    data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'aberto',
    PRIMARY KEY (id_ordem),
    CONSTRAINT fk_ordem_cliente FOREIGN KEY (id_cliente)
        REFERENCES clientes (id_cliente),
    CONSTRAINT fk_ordem_carro FOREIGN KEY (id_carro)
        REFERENCES carros (id_carro) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ordem_servico_itens (
    id_item INT NOT NULL AUTO_INCREMENT,
    id_ordem INT NOT NULL,
    id_servico INT NOT NULL,
    preco DECIMAL(10,2) NULL,
    PRIMARY KEY (id_item),
    CONSTRAINT fk_ordem_item_ordem FOREIGN KEY (id_ordem)
        REFERENCES ordem_servico (id_ordem) ON DELETE CASCADE,
    CONSTRAINT fk_ordem_item_servico FOREIGN KEY (id_servico)
        REFERENCES servicos (id_servico)
) ENGINE=InnoDB;