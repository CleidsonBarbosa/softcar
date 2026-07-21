USE softcar;

ALTER TABLE `softcar`.`clientes` DROP FOREIGN KEY `id_func`;

INSERT INTO clientes (nome_cliente, email_cliente, telefone_cliente, cpf, endereco, data_nascimento) VALUES
('João Silva', 'joao.silva@email.com', '11999887766', '12345678901', 'Rua A, 100', '1990-05-15'),
('Maria Santos', 'maria.santos@email.com', '11988776655', '23456789012', 'Rua B, 200', '1985-03-20'),
('Pedro Oliveira', 'pedro.oliveira@email.com', '11977665544', '34567890123', 'Rua C, 300', '1992-07-10'),
('Ana Costa', 'ana.costa@email.com', '11966554433', '45678901234', 'Rua D, 400', '1988-11-25'),
('Lucas Pereira', 'lucas.pereira@email.com', '11955443322', '56789012345', 'Rua E, 500', '1995-01-30'),
('Juliana Lima', 'juliana.lima@email.com', '11944332211', '67890123456', 'Rua F, 600', '1993-09-12'),
('Carlos Souza', 'carlos.souza@email.com', '11933221100', '78901234567', 'Rua G, 700', '1987-06-18'),
('Fernanda Almeida', 'fernanda.almeida@email.com', '11922110099', '89012345678', 'Rua H, 800', '1991-04-05'),
('Rafael Ferreira', 'rafael.ferreira@email.com', '11911009988', '90123456789', 'Rua I, 900', '1989-12-08'),
('Camila Ribeiro', 'camila.ribeiro@email.com', '11900998877', '01234567890', 'Rua J, 1000', '1994-08-22'),
('Bruno Martins', 'bruno.martins@email.com', '11999881122', '11223344556', 'Rua K, 1100', '1986-02-14'),
('Isabela Araujo', 'isabela.araujo@email.com', '11988772233', '22334455667', 'Rua L, 1200', '1990-10-03'),
('Thiago Gomes', 'thiago.gomes@email.com', '11977663344', '33445566778', 'Rua M, 1300', '1993-05-27'),
('Larissa Barbosa', 'larissa.barbosa@email.com', '11966554455', '44556677889', 'Rua N, 1400', '1988-07-16'),
('Gabriel Dias', 'gabriel.dias@email.com', '11955445566', '55667788990', 'Rua O, 1500', '1991-11-29'),
('Amanda Carvalho', 'amanda.carvalho@email.com', '11944336677', '66778899001', 'Rua P, 1600', '1994-03-08'),
('Diego Nascimento', 'diego.nascimento@email.com', '11933227788', '77889900112', 'Rua Q, 1700', '1987-09-21'),
('Patricia Moreira', 'patricia.moreira@email.com', '11922118899', '88990011223', 'Rua R, 1800', '1992-01-12'),
('Felipe Rocha', 'felipe.rocha@email.com', '11911009900', '99001122334', 'Rua S, 1900', '1989-06-05'),
('Mariana Campos', 'mariana.campos@email.com', '11900990011', '00112233445', 'Rua T, 2000', '1995-12-18');

INSERT INTO carros (placa, modelo, marca, cor) VALUES
('ABC1234', 'Onix', 'Chevrolet', 'Prata'),
('DEF5678', 'HB20', 'Hyundai', 'Branco'),
('GHI9012', 'Civic', 'Honda', 'Preto'),
('JKL3456', 'Corolla', 'Toyota', 'Vermelho'),
('MNO7890', 'Argo', 'Fiat', 'Azul'),
('PQR1122', 'Pulse', 'Fiat', 'Cinza'),
('STU3344', 'T-Cross', 'Volkswagen', 'Verde'),
('VWX5566', 'Tracker', 'Chevrolet', 'Amarelo'),
('YZA7788', 'Renegade', 'Jeep', 'Laranja'),
('BCD9900', 'Duster', 'Renault', 'Marrom'),
('EFG1122', 'Compass', 'Jeep', 'Azul Escuro'),
('HIJ3344', 'CR-V', 'Honda', 'Preto'),
('KLM5566', 'Tucson', 'Hyundai', 'Branco'),
('NOP7788', 'Sportage', 'Kia', 'Prata'),
('QRS9900', '208', 'Peugeot', 'Vermelho'),
('TUV1122', 'Creta', 'Hyundai', 'Cinza'),
('WXY3344', 'Captur', 'Renault', 'Verde'),
('ZAB5566', 'Bronco Sport', 'Ford', 'Laranja'),
('CDE7788', 'Wrangler', 'Jeep', 'Preto'),
('FGH9900', 'Crossfox', 'Volkswagen', 'Prata');
