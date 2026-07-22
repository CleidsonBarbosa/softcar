-- -----------------------------------------------------
-- Schema softcar
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `softcar` DEFAULT CHARACTER SET utf8 ;
USE `softcar` ;

-- -----------------------------------------------------
-- Table `softcar`.`funcionarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `softcar`.`funcionarios` (
  `id_func` INT NOT NULL AUTO_INCREMENT,
  `nome_func` VARCHAR(80) NOT NULL,
  `email_func` VARCHAR(80) NOT NULL,
  `cpf_func` CHAR(11) NOT NULL,
  `senha` VARCHAR(255) NOT NULL,
  `cargo` ENUM('lavador', 'atendente') NOT NULL,
  `endereco_func` VARCHAR(100) NOT NULL,
  `data_nascimento_func` DATE NOT NULL,
  `telefone_func` CHAR(11) NOT NULL,
  PRIMARY KEY (`id_func`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `softcar`.`clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `softcar`.`clientes` (
  `nome_cliente` VARCHAR(80) NOT NULL,
  `email_cliente` VARCHAR(80) NOT NULL,
  `telefone_cliente` CHAR(11) NOT NULL,
  `cpf` CHAR(11) NOT NULL,
  `endereco` VARCHAR(100) NOT NULL,
  `data_nascimento` DATE NULL,
  `id_cliente` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_cliente`),
  UNIQUE INDEX `id_cliente_UNIQUE` (`id_cliente` ASC) VISIBLE,
  CONSTRAINT `id_func`
    FOREIGN KEY (`id_cliente`)
    REFERENCES `softcar`.`funcionarios` (`id_func`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `softcar`.`carros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `softcar`.`carros` (
  `placa` CHAR(7) NOT NULL,
  `modelo` VARCHAR(45) NULL,
  `marca` VARCHAR(45) NULL,
  `cor` VARCHAR(45) NULL,
  `id_carro` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_carro`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `softcar`.`estoque`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `softcar`.`estoque` (
  `id_produto` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(45) NOT NULL,
  `quantidade` INT NOT NULL,
  PRIMARY KEY (`id_produto`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `softcar`.`servicos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `softcar`.`servicos` (
  `id_servico` INT NOT NULL AUTO_INCREMENT,
  `nome_servico` VARCHAR(45) NOT NULL,
  `estoque_id_produto` INT NOT NULL,
  `data_hora_servico` DATETIME(4) NULL,
  PRIMARY KEY (`id_servico`),
  UNIQUE INDEX `id_servico_UNIQUE` (`id_servico` ASC) VISIBLE,
  INDEX `fk_servicos_estoque1_idx` (`estoque_id_produto` ASC) VISIBLE,
  CONSTRAINT `id_carro`
    FOREIGN KEY (`id_servico`)
    REFERENCES `softcar`.`carros` (`id_carro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_servicos_estoque1`
    FOREIGN KEY (`estoque_id_produto`)
    REFERENCES `softcar`.`estoque` (`id_produto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `softcar`.`clientes_has_carros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `softcar`.`clientes_has_carros` (
  `clientes_id_cliente` INT NOT NULL,
  `carros_id_carro` INT NOT NULL,
  PRIMARY KEY (`clientes_id_cliente`, `carros_id_carro`),
  INDEX `fk_clientes_has_carros_carros1_idx` (`carros_id_carro` ASC) VISIBLE,
  INDEX `fk_clientes_has_carros_clientes1_idx` (`clientes_id_cliente` ASC) VISIBLE,
  CONSTRAINT `fk_clientes_has_carros_clientes1`
    FOREIGN KEY (`clientes_id_cliente`)
    REFERENCES `softcar`.`clientes` (`id_cliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_clientes_has_carros_carros1`
    FOREIGN KEY (`carros_id_carro`)
    REFERENCES `softcar`.`carros` (`id_carro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Inserts
-- -----------------------------------------------------

INSERT INTO funcionarios (id_func, nome_func, email_func, cpf_func, senha, cargo, endereco_func, data_nascimento_func, telefone_func) VALUES
(1,  'Cleidson Barbosa',  'cleidson-barbosa@hotmail.com', '11111111101', '123456', 'atendente', 'End 1',  '1990-01-01', '11999999901'),
(8,  'Ananias de Rocha',  'func8@email.com',              '11111111108', '654321', 'atendente', 'End 8',  '1990-01-01', '11999999908'),
(12, 'Ana Silva do Santos','ana@email.com',               '11111111111', '123',    'atendente', 'Rua A, 100',  '1990-01-15', '11911111111'),
(13, 'Bruno Costa da Silva','bruno@email.com',            '22222222222', '123',    'lavador',   'Rua B, 200',  '1991-02-20', '11922222222'),
(14, 'Carla Souza de Marcedo','carla@email.com',          '33333333333', '123',    'atendente', 'Rua C, 300',  '1992-03-25', '11933333333'),
(15, 'Diego Oliveira',      'diego@email.com',            '44444444444', '123',    'lavador',   'Rua D, 400',  '1993-04-30', '11944444444'),
(16, 'Elena Santos',        'elena@email.com',            '55555555555', '123',    'lavador',   'Rua E, 500',  '1994-05-05', '11955555555'),
(17, 'Felipe Lima',         'felipe@email.com',           '66666666666', '123',    'lavador',   'Rua F, 600',  '1995-06-10', '11966666666'),
(18, 'Gabriela Rocha',      'gabriela@email.com',         '77777777777', '123',    'atendente', 'Rua G, 700',  '1996-07-15', '11977777777'),
(19, 'Henrique Martins',    'henrique@email.com',         '88888888888', '123',    'lavador',   'Rua H, 800',  '1997-08-20', '11988888888'),
(20, 'Isabela Pereira',     'isabela@email.com',          '99999999999', '123',    'atendente', 'Rua I, 900',  '1998-09-25', '11999999999'),
(21, 'João Almeida',        'joao@email.com',             '10101010101', '123',    'lavador',   'Rua J, 1000', '1999-10-30', '11910101010'),
(22, 'Karina Barbosa',      'karina@email.com',           '11111111112', '123',    'atendente', 'Rua K, 1100', '1988-11-05', '11911111112'),
(23, 'Leandro Dias',        'leandro@email.com',          '12121212121', 'abcd',   'lavador',   'Rua L, 1200', '1987-12-10', '11912121212'),
(24, 'Marina Teixeira',     'marina@email.com',           '13131313131', '123',    '',          'Rua M, 1300', '1986-01-15', '11913131313'),
(25, 'Nathan Ribeiro',      'nathan@email.com',           '14141414141', '123',    'lavador',   'Rua N, 1400', '1985-02-20', '11914141414'),
(26, 'Olivia Carvalho',     'olivia@email.com',           '15151515151', '123',    'atendente', 'Rua O, 1500', '1984-03-25', '11915151515'),
(27, 'Pedro Farias',        'pedro@email.com',            '16161616161', '123',    'lavador',   'Rua P, 1600', '1983-04-30', '11916161616'),
(28, 'Renata Gomes',        'renata@email.com',           '17171717171', '123',    'atendente', 'Rua Q, 1700', '1982-05-05', '11917171717'),
(29, 'Samuel Moreira',      'samuel@email.com',           '18181818181', '123',    'lavador',   'Rua R, 1800', '1981-06-10', '11918181818'),
(30, 'Tatiane Nunes',       'tatiane@email.com',          '19191919191', '123',    'atendente', 'Rua S, 1900', '1980-07-15', '11919191919'),
(31, 'Vinicius Campos de Araujo','vinicius@email.com',    '20202020202', '123',    'lavador',   'Rua T, 2000', '1979-08-20', '11920202020');

INSERT INTO clientes (id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco, data_nascimento) VALUES
(1,  'Cliente 1',  'cliente1@email.com',  '11999990001', '10000000001', 'End 1',  '1990-01-01'),
(2,  'Cliente 2',  'cliente2@email.com',  '11999990002', '10000000002', 'End 2',  '1990-01-01'),
(3,  'Cliente 3',  'cliente3@email.com',  '11999990003', '10000000003', 'End 3',  '1990-01-01'),
(4,  'Cliente 4',  'cliente4@email.com',  '11999990004', '10000000004', 'End 4',  '1990-01-01'),
(5,  'Cliente 5',  'cliente5@email.com',  '11999990005', '10000000005', 'End 5',  '1990-01-01'),
(6,  'Cliente 6',  'cliente6@email.com',  '11999990006', '10000000006', 'End 6',  '1990-01-01'),
(7,  'Cliente 7',  'cliente7@email.com',  '11999990007', '10000000007', 'End 7',  '1990-01-01'),
(8,  'Cliente 8',  'cliente8@email.com',  '11999990008', '10000000008', 'End 8',  '1990-01-01'),
(9,  'Cliente 9',  'cliente9@email.com',  '11999990009', '10000000009', 'End 9',  '1990-01-01'),
(10, 'Cliente 10', 'cliente10@email.com', '11999990010', '10000000010', 'End 10', '1990-01-01'),
(11, 'Cassio Andrade',   'cassio@mail.com',   '9187956542',  '78257746231', 'cidade dos politicos', '1985-06-25'),
(12, 'Adriana Pereira',  'adriana@mail.com',  '91989876574', '98659237413', 'cidade da farinha',    '1986-12-23');

