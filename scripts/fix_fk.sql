USE softcar;

SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_write_timeout = 600;
SET GLOBAL wait_timeout = 28800;
SET SESSION net_read_timeout = 600;
SET SESSION net_write_timeout = 600;

ALTER TABLE `softcar`.`clientes` DROP FOREIGN KEY `id_func`, DROP INDEX `id_func`;
