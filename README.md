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

1. Criar o banco de dados no MySQL:
```sql
CREATE DATABASE softcar;
```

2. Importar o schema:
```bash
mysql -u root softcar < banco/banco.sql
```

3. (Opcional) Carregar dados de teste:
```bash
mysql -u root softcar < banco/script.sql
```

4. Configurar a conexao em `main.py` (linha 20):
```python
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",        # senha do MySQL
    database="softcar"
)
```

## Executacao

```bash
python main.py
```

## Credenciais de Teste

O `banco/banco.sql` ja inclui funcionarios de teste. Use qualquer email/senha inseridos no schema.

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
    banco.sql          -- Schema do banco
    script.sql         -- Dados de teste
  assets/              -- Imagens (icones, fundos, botoes)
```

## Stack

- **Frontend:** CustomTkinter (Python)
- **Backend:** Python 3.11
- **Banco de dados:** MySQL
- **Imagens:** Pillow

## Licenca

Projeto academico.
