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

 
 