<--inserir dados na tabela funcionarios-->

INSERT INTO funcionarios(
id_func,
nome_func,
 email_func,
 cpf_func,
 senha,
 cargo,
 endereco_func,
 data_nascimento_func,
 telefone_func)
 VALUES (
 1,
  'Cleidson',
 'cleidson-barbosa@hotmail.com',
 0000000000,
 123456,
 'lavador',
 'cidade',
 27/05/1985,
 981613531)

 <--selecionar a tabela para exibir-->
 
 SELECT * FROM clientes;

 <--inserir dados na tabela funcionarios-->
 
 INSERT INTO funcionarios(
id_func,
nome_func,
 email_func,
 cpf_func,
 senha,
 cargo,
 endereco_func,
 data_nascimento_func,
 telefone_func)
 VALUES (
 2,
  'Francisco',
 'fgomess744@gmail.com',
 111111111,
 123456,
 'lavador',
 'nova',
 2009-07-09,
 981613531)

 <---inserir dados na tabela cliente-->

 INSERT INTO clientes(
 id_cliente,
 nome_cliente,
 email_cliente,
 telefone_cliente
 cpf,
 endereco,
 data_nascimento)
 VALUES (
 1,
 'Marcos',
 'marcos@hotmail.com',
 915151515151,
 515151515151,
 'cidade da lagoa azul',
 1985-05-27)

<--atualizar dados de acordo com o id da tabela funcionarios-->

UPDATE funcionarios
SET nome_func = 'Cleidson Barbosa', email_func = 'cleidson-barbosa@hotmail.com'
WHERE id_func = 1;

INSERT INTO funcionarios (nome_func, email_func, telefone_func, cpf_func, cargo, endereco_func, data_nascimento_func, senha) VALUES
('Ana Silva', 'ana@email.com', '11911111111', '11111111111', 'atendente', 'Rua A, 100', '1990-01-15', '123'),
('Bruno Costa', 'bruno@email.com', '11922222222', '22222222222', 'lavador', 'Rua B, 200', '1991-02-20', '123'),
('Carla Souza', 'carla@email.com', '11933333333', '33333333333', 'atendente', 'Rua C, 300', '1992-03-25', '123'),
('Diego Oliveira', 'diego@email.com', '11944444444', '44444444444', 'lavador', 'Rua D, 400', '1993-04-30', '123'),
('Elena Santos', 'elena@email.com', '11955555555', '55555555555', 'gerente', 'Rua E, 500', '1994-05-05', '123'),
('Felipe Lima', 'felipe@email.com', '11966666666', '66666666666', 'lavador', 'Rua F, 600', '1995-06-10', '123'),
('Gabriela Rocha', 'gabriela@email.com', '11977777777', '77777777777', 'atendente', 'Rua G, 700', '1996-07-15', '123'),
('Henrique Martins', 'henrique@email.com', '11988888888', '88888888888', 'lavador', 'Rua H, 800', '1997-08-20', '123'),
('Isabela Pereira', 'isabela@email.com', '11999999999', '99999999999', 'atendente', 'Rua I, 900', '1998-09-25', '123'),
('João Almeida', 'joao@email.com', '11910101010', '10101010101', 'lavador', 'Rua J, 1000', '1999-10-30', '123'),
('Karina Barbosa', 'karina@email.com', '11911111112', '11111111112', 'atendente', 'Rua K, 1100', '1988-11-05', '123'),
('Leandro Dias', 'leandro@email.com', '11912121212', '12121212121', 'lavador', 'Rua L, 1200', '1987-12-10', '123'),
('Marina Teixeira', 'marina@email.com', '11913131313', '13131313131', 'gerente', 'Rua M, 1300', '1986-01-15', '123'),
('Nathan Ribeiro', 'nathan@email.com', '11914141414', '14141414141', 'lavador', 'Rua N, 1400', '1985-02-20', '123'),
('Olivia Carvalho', 'olivia@email.com', '11915151515', '15151515151', 'atendente', 'Rua O, 1500', '1984-03-25', '123'),
('Pedro Farias', 'pedro@email.com', '11916161616', '16161616161', 'lavador', 'Rua P, 1600', '1983-04-30', '123'),
('Renata Gomes', 'renata@email.com', '11917171717', '17171717171', 'atendente', 'Rua Q, 1700', '1982-05-05', '123'),
('Samuel Moreira', 'samuel@email.com', '11918181818', '18181818181', 'lavador', 'Rua R, 1800', '1981-06-10', '123'),
('Tatiane Nunes', 'tatiane@email.com', '11919191919', '19191919191', 'atendente', 'Rua S, 1900', '1980-07-15', '123'),
('Vinicius Campos', 'vinicius@email.com', '11920202020', '20202020202', 'lavador', 'Rua T, 2000', '1979-08-20', '123');

 
 