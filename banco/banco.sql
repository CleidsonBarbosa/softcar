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

