CREATE DATABASE  IF NOT EXISTS `softcar` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `softcar`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: softcar
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `carros`
--

DROP TABLE IF EXISTS `carros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carros` (
  `placa` char(7) NOT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `marca` varchar(45) DEFAULT NULL,
  `cor` varchar(45) DEFAULT NULL,
  `id_carro` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_carro`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carros`
--

LOCK TABLES `carros` WRITE;
/*!40000 ALTER TABLE `carros` DISABLE KEYS */;
INSERT INTO `carros` VALUES ('ABC1234','Onix','Chevrolet','Prata',1),('DEF5678','HB20','Hyundai','Branco',2),('GHI9012','Civic','Honda','Preto',3),('JKL3456','Corolla','Toyota','Vermelho',4),('MNO7890','Argo','Fiat','Azul',5),('PQR1122','Pulse','Fiat','Cinza',6),('STU3344','T-Cross','Volkswagen','Verde',7),('VWX5566','Tracker','Chevrolet','Amarelo',8),('YZA7788','Renegade','Jeep','Laranja',9),('BCD9900','Duster','Renault','Marrom',10),('EFG1122','Compass','Jeep','Azul Escuro',11),('HIJ3344','CR-V','Honda','Preto',12),('KLM5566','Tucson','Hyundai','Branco',13),('NOP7788','Sportage','Kia','Prata',14),('QRS9900','208','Peugeot','Vermelho',15),('TUV1122','Creta','Hyundai','Cinza',16),('WXY3344','Captur','Renault','Verde',17),('ZAB5566','Bronco Sport','Ford','Laranja',18),('CDE7788','Wrangler','Jeep','Preto',19),('FGH9900','Crossfox','Volkswagen','Prata',20),('qvb2361','fit','honda','vermelha',21),('wmd5634','celta','fiat','preto',22),('quf2598','Volkswagen','Polo','Preto fosco',23),('qwd2564','Jeep','Toyota','Verde',24);
/*!40000 ALTER TABLE `carros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `nome_cliente` varchar(80) NOT NULL,
  `email_cliente` varchar(80) NOT NULL,
  `telefone_cliente` char(11) NOT NULL,
  `cpf` char(11) NOT NULL,
  `endereco` varchar(100) NOT NULL,
  `data_nascimento` date DEFAULT NULL,
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `id_cliente_UNIQUE` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES ('Cliente 1','cliente1@email.com','11999990001','10000000001','End 1','1990-01-01',1),('Cliente 2','cliente2@email.com','11999990002','10000000002','End 2','1990-01-01',2),('Cliente 3','cliente3@email.com','11999990003','10000000003','End 3','1990-01-01',3),('Cliente 4','cliente4@email.com','11999990004','10000000004','End 4','1990-01-01',4),('Cliente 5','cliente5@email.com','11999990005','10000000005','End 5','1990-01-01',5),('Cliente 6','cliente6@email.com','11999990006','10000000006','End 6','1990-01-01',6),('Cliente 7','cliente7@email.com','11999990007','10000000007','End 7','1990-01-01',7),('Cliente 8','cliente8@email.com','11999990008','10000000008','End 8','1990-01-01',8),('Cliente 9','cliente9@email.com','11999990009','10000000009','End 9','1990-01-01',9),('Cliente 10','cliente10@email.com','11999990010','10000000010','End 10','1990-01-01',10),('Cassio Andrade','cassio@mail.com','9187956542','78257746231','cidade dos politicos','1985-06-25',11),('Adriana Pereira','adriana@mail.com','91989876574','98659237413','cidade da farinha','1986-12-22',12),('Maria Izabel dos Santos','izabel@mail.com','(91)9816532','78259467238','cidade da princesa','1980-04-25',13);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes_has_carros`
--

DROP TABLE IF EXISTS `clientes_has_carros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes_has_carros` (
  `clientes_id_cliente` int NOT NULL,
  `carros_id_carro` int NOT NULL,
  PRIMARY KEY (`clientes_id_cliente`,`carros_id_carro`),
  KEY `fk_clientes_has_carros_carros1_idx` (`carros_id_carro`),
  KEY `fk_clientes_has_carros_clientes1_idx` (`clientes_id_cliente`),
  CONSTRAINT `fk_clientes_has_carros_carros1` FOREIGN KEY (`carros_id_carro`) REFERENCES `carros` (`id_carro`),
  CONSTRAINT `fk_clientes_has_carros_clientes1` FOREIGN KEY (`clientes_id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_has_carros`
--

LOCK TABLES `clientes_has_carros` WRITE;
/*!40000 ALTER TABLE `clientes_has_carros` DISABLE KEYS */;
INSERT INTO `clientes_has_carros` VALUES (12,21),(12,22),(13,23),(11,24);
/*!40000 ALTER TABLE `clientes_has_carros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoque`
--

DROP TABLE IF EXISTS `estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoque` (
  `id_produto` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) NOT NULL,
  `quantidade` int NOT NULL,
  PRIMARY KEY (`id_produto`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque`
--

LOCK TABLES `estoque` WRITE;
/*!40000 ALTER TABLE `estoque` DISABLE KEYS */;
INSERT INTO `estoque` VALUES (41,'Xampu automotivo 5L',15),(42,'Cera líquida 1L',10),(43,'Cera em pasta 500g',8),(44,'Desengraxante 5L',20),(45,'Limpa-alcatrão 500ml',10),(46,'Limpa-rodas ácido 5L',12),(47,'Lava a seco 500ml',15),(48,'Secante automotivo 1L',10),(49,'Finalizador brilho 1L',8),(50,'Espuma ativa 5L',12),(51,'Shampoo neutro 5L',20),(52,'Perfumador automotivo 500ml',15),(53,'Silicone spray 300ml',25),(54,'Revitalizador de pneus 500ml',15),(55,'Limpa-estofados 500ml',10),(56,'Bucha de espuma (macia)',20),(57,'Escova para rodas (pivotante)',8),(58,'Pano microfibra 40x40cm',40),(59,'Saco de lixo 200L (rolo 20un)',10),(60,'Balde 20L com cesto',8);
/*!40000 ALTER TABLE `estoque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcionarios`
--

DROP TABLE IF EXISTS `funcionarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionarios` (
  `id_func` int NOT NULL AUTO_INCREMENT,
  `nome_func` varchar(80) NOT NULL,
  `email_func` varchar(80) NOT NULL,
  `cpf_func` char(11) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `cargo` enum('lavador','atendente') NOT NULL,
  `endereco_func` varchar(100) NOT NULL,
  `data_nascimento_func` date NOT NULL,
  `telefone_func` char(11) NOT NULL,
  PRIMARY KEY (`id_func`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionarios`
--

LOCK TABLES `funcionarios` WRITE;
/*!40000 ALTER TABLE `funcionarios` DISABLE KEYS */;
INSERT INTO `funcionarios` VALUES (1,'Cleidson Barbosa','cleidson-barbosa@hotmail.com','11111111101','123456','atendente','End 1','1990-01-01','11999999901'),(8,'Ananias de Rocha','func8@email.com','11111111108','654321','atendente','End 8','1990-01-01','11999999908'),(12,'Ana Silva do Santos','ana@email.com','11111111111','123','atendente','Rua A, 100','1990-01-15','11911111111'),(13,'Bruno Costa da Silva','bruno@email.com','22222222222','123','lavador','Rua B, 200','1991-02-20','11922222222'),(14,'Carla Souza de Marcedo','carla@email.com','33333333333','123','atendente','Rua C, 300','1992-03-25','11933333333'),(15,'Diego Oliveira','diego@email.com','44444444444','123','lavador','Rua D, 400','1993-04-30','11944444444'),(16,'Elena Santos','elena@email.com','55555555555','123','lavador','Rua E, 500','1994-05-05','11955555555'),(17,'Felipe Lima','felipe@email.com','66666666666','123','lavador','Rua F, 600','1995-06-10','11966666666'),(18,'Gabriela Rocha','gabriela@email.com','77777777777','123','atendente','Rua G, 700','1996-07-15','11977777777'),(19,'Henrique Martins','henrique@email.com','88888888888','123','lavador','Rua H, 800','1997-08-20','11988888888'),(20,'Isabela Pereira','isabela@email.com','99999999999','123','atendente','Rua I, 900','1998-09-25','11999999999'),(21,'João Almeida','joao@email.com','10101010101','123','lavador','Rua J, 1000','1999-10-30','11910101010'),(22,'Karina Barbosa','karina@email.com','11111111112','123','atendente','Rua K, 1100','1988-11-05','11911111112'),(23,'Leandro Dias','leandro@email.com','12121212121','abcd','lavador','Rua L, 1200','1987-12-10','11912121212'),(24,'Marina Teixeira','marina@email.com','13131313131','123','','Rua M, 1300','1986-01-15','11913131313'),(25,'Nathan Ribeiro','nathan@email.com','14141414141','123','lavador','Rua N, 1400','1985-02-20','11914141414'),(26,'Olivia Carvalho','olivia@email.com','15151515151','123','atendente','Rua O, 1500','1984-03-25','11915151515'),(27,'Pedro Farias','pedro@email.com','16161616161','123','lavador','Rua P, 1600','1983-04-30','11916161616'),(28,'Renata Gomes','renata@email.com','17171717171','123','atendente','Rua Q, 1700','1982-05-05','11917171717'),(29,'Samuel Moreira','samuel@email.com','18181818181','123','lavador','Rua R, 1800','1981-06-10','11918181818'),(30,'Tatiane Nunes','tatiane@email.com','19191919191','123','atendente','Rua S, 1900','1980-07-15','11919191919'),(31,'Vinicius Campos de Araujo','vinicius@email.com','20202020202','123','lavador','Rua T, 2000','1979-08-20','11920202020');
/*!40000 ALTER TABLE `funcionarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordem_servico`
--

DROP TABLE IF EXISTS `ordem_servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordem_servico` (
  `id_ordem` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `id_carro` int DEFAULT NULL,
  `data_hora` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'aberto',
  PRIMARY KEY (`id_ordem`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordem_servico`
--

LOCK TABLES `ordem_servico` WRITE;
/*!40000 ALTER TABLE `ordem_servico` DISABLE KEYS */;
INSERT INTO `ordem_servico` VALUES (1,12,21,'2026-07-23 19:52:58',420.00,'aberto'),(2,12,21,'2026-07-23 19:54:12',370.00,'aberto'),(3,12,21,'2026-07-23 20:07:59',480.00,'aberto'),(4,12,22,'2026-07-24 19:29:54',180.00,'finalizado'),(5,12,22,'2026-08-11 19:42:57',320.00,'aberto'),(6,12,21,'2026-08-11 19:58:52',970.00,'aberto'),(7,12,22,'2026-08-12 19:35:58',150.00,'aberto'),(8,12,22,'2026-08-12 19:40:55',80.00,'aberto'),(9,1,NULL,'2026-08-12 19:52:35',250.00,'finalizado'),(10,13,NULL,'2026-08-12 20:13:02',100.00,'aberto'),(11,11,24,'2026-08-12 20:27:27',100.00,'aberto');
/*!40000 ALTER TABLE `ordem_servico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordem_servico_itens`
--

DROP TABLE IF EXISTS `ordem_servico_itens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordem_servico_itens` (
  `id_item` int NOT NULL AUTO_INCREMENT,
  `id_ordem` int NOT NULL,
  `id_servico` int NOT NULL,
  `preco` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_item`),
  KEY `id_ordem` (`id_ordem`),
  KEY `id_servico` (`id_servico`),
  CONSTRAINT `ordem_servico_itens_ibfk_1` FOREIGN KEY (`id_ordem`) REFERENCES `ordem_servico` (`id_ordem`),
  CONSTRAINT `ordem_servico_itens_ibfk_2` FOREIGN KEY (`id_servico`) REFERENCES `servicos` (`id_servico`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordem_servico_itens`
--

LOCK TABLES `ordem_servico_itens` WRITE;
/*!40000 ALTER TABLE `ordem_servico_itens` DISABLE KEYS */;
INSERT INTO `ordem_servico_itens` VALUES (1,1,14,150.00),(2,1,19,100.00),(3,1,13,80.00),(4,1,17,90.00),(5,2,14,150.00),(6,2,19,100.00),(7,2,13,80.00),(8,2,18,40.00),(9,3,14,150.00),(10,3,13,80.00),(11,3,15,250.00),(12,4,20,50.00),(13,4,19,100.00),(14,4,11,30.00),(15,5,14,150.00),(16,5,20,50.00),(17,5,16,120.00),(18,6,14,150.00),(19,6,20,50.00),(20,6,16,120.00),(21,6,12,60.00),(22,6,19,100.00),(23,6,13,80.00),(24,6,11,30.00),(25,6,17,90.00),(26,6,18,40.00),(27,6,15,250.00),(28,7,14,150.00),(29,8,13,80.00),(30,9,15,250.00),(31,10,19,100.00),(32,11,19,100.00);
/*!40000 ALTER TABLE `ordem_servico_itens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicos`
--

DROP TABLE IF EXISTS `servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicos` (
  `id_servico` int NOT NULL AUTO_INCREMENT,
  `nome_servico` varchar(45) NOT NULL,
  `preco_servico` decimal(10,2) DEFAULT NULL,
  `estoque_id_produto` int NOT NULL,
  `data_hora_servico` datetime(4) DEFAULT NULL,
  PRIMARY KEY (`id_servico`),
  UNIQUE KEY `id_servico_UNIQUE` (`id_servico`),
  KEY `fk_servicos_estoque1_idx` (`estoque_id_produto`),
  CONSTRAINT `fk_servicos_estoque1` FOREIGN KEY (`estoque_id_produto`) REFERENCES `estoque` (`id_produto`),
  CONSTRAINT `id_carro` FOREIGN KEY (`id_servico`) REFERENCES `carros` (`id_carro`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos`
--

LOCK TABLES `servicos` WRITE;
/*!40000 ALTER TABLE `servicos` DISABLE KEYS */;
INSERT INTO `servicos` VALUES (11,'Lavagem simples externa',30.00,41,NULL),(12,'Lavagem completa interna + externa',60.00,41,NULL),(13,'Lavagem de motor',80.00,44,NULL),(14,'Cristalização de pintura',150.00,42,NULL),(15,'Vitrificação de pintura',250.00,42,NULL),(16,'Higienização interna',120.00,55,NULL),(17,'Revitalização de bancos de couro',90.00,54,NULL),(18,'Revitalização de pneus',40.00,54,NULL),(19,'Lavagem de estofados',100.00,55,NULL),(20,'Enceramento profissional',50.00,43,NULL);
/*!40000 ALTER TABLE `servicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `table1`
--

DROP TABLE IF EXISTS `table1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table1` (
  `idtable1` int NOT NULL,
  PRIMARY KEY (`idtable1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table1`
--

LOCK TABLES `table1` WRITE;
/*!40000 ALTER TABLE `table1` DISABLE KEYS */;
/*!40000 ALTER TABLE `table1` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-13 19:46:24
