# Soft Car

Sistema de gestao automotiva para lava-rapido e oficina. Gerencia clientes, veiculos, servicos, funcionarios, estoque e ordens de servico.

## Funcionalidades

- **Login** com autenticacao contra banco de dados
- **Dashboard** com metricas (servicos agendados, realizados, clientes, veiculos, receita total)
- **Clientes** -- cadastro, edicao, exclusao, busca
- **Carros** -- cadastro de veiculos vinculados a clientes
- **Servicos** -- catalogo de servicos com precos
- **Ordens de Servico** -- criacao com selecao de servicos, finalizacao
- **Funcionarios** -- cadastro com cargos (lavador/atendente)
- **Materiais/Estoque** -- controle de materiais

## Pre-requisitos

- Python 3.11+
- MySQL Server 8.0+
- pip (gerenciador de pacotes)

## Instalacao

```bash
# Clonar o repositorio
git clone https://github.com/seu-usuario/softcar.git
cd softcar

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuracao do Banco de Dados

1. Criar o banco novo no MySQL:
```sql
SOURCE banco/novo_banco.sql;
```

Ou pelo terminal:
```bash
mysql -u root < banco/novo_banco.sql
```

2. Carregar o seed inicial:
```bash
mysql -u root < banco/seed.sql
```

O projeto já está configurado para usar o banco `softcar_novo` em `banco/db_config.py`.
Para outro usuário, senha ou servidor MySQL, altere `DB_CONFIG` nesse arquivo.

## Primeiro Login

Após executar o seed, use:

```text
E-mail: admin@softcar.com
Senha: 123456
```

## Banco de Dados

O arquivo `banco/novo_banco.sql` cria um schema limpo, com as tabelas e relacionamentos usados pela aplicação. O arquivo `banco/seed.sql` insere o usuário inicial e dados mínimos para testar clientes, estoque e serviços.

O banco antigo não é apagado. Os arquivos `banco/banco.sql` e `beckup do banco/softcar.sql` ficam preservados como referência.

Para executar a aplicação:
```python
python main.py
```

## Executacao

```bash
python main.py
```

## Estrutura do Projeto

```
softcar/
  main.py              -- Ponto de entrada (tela de login)
  view/
    bemvindo.py        -- Dashboard
    tela_clientes.py   -- Gestao de clientes
    tela_servicos.py   -- Gestao de servicos
    tela_servico.py    -- Execucao de servicos
    tela_materiais.py  -- Gestao de estoque
    lista_funcionarios.py -- Gestao de funcionarios
  banco/
    novo_banco.sql     -- Schema novo e relacionamentos
    seed.sql           -- Usuario inicial e dados minimos
    db_config.py       -- Configuracao central da conexao
  service/             -- Regras de negocio
  repository/          -- Consultas SQL
  assets/              -- Imagens (icones, fundos, botoes)
```

## Stack

- **Frontend:** CustomTkinter (Python)
- **Backend:** Python 3.11
- **Banco de dados:** MySQL
- **Imagens:** Pillow

## Licenca

Projeto academico.
