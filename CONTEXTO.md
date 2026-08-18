# SOFTCAR - Contexto Completo do Projeto

## Visao Geral

Soft Car e um sistema de gestao automotiva (car wash / oficina) desenvolvido em Python com CustomTkinter (UI), MySQL (banco de dados) e Pillow (imagens). O sistema gerencia clientes, carros, servicos, funcionarios, materiais/estoque e ordens de servico.

## Stack Tecnico

- **Linguagem:** Python 3.11
- **UI:** CustomTkinter 6.0.0 (wrapper moderno do tkinter)
- **Banco de dados:** MySQL (mysql-connector-python 9.7.0)
- **Imagens:** Pillow 12.3.0
- **Deteccao de tema:** darkdetect 0.8.0
- **Ambiente:** venv local

## Arquitetura de Navegacao (IMPORTANTE)

O projeto usa um padrao de **janela unica destruida/recriada**. Cada navegacao entre telas:
1. Destroi a janela anterior via `root_anterior.destroy()`
2. Cria uma nova `ctk.CTk()` na tela de destino

**Isso causa o bug de "invalid command name"** porque callbacks `after` do customtkinter (ScalingTracker, AppearanceModeTracker) ficam orfaos quando a janela e destruida.

### Fluxo de navegacao:
```
main.py::tela_login()
  |-- (sucesso) --> bemvindo.py::tela_dashboard(cargo, root_anterior=root)
      |-- "Cliente"       --> tela_clientes.py::tela_clientes(root_anterior=root)
      |-- "Servicos"      --> tela_servicos.py::tela_servicos(root_anterior=root)
      |-- "Funcionarios"  --> lista_funcionarios.py::tela_lista_funcionarios(root_anterior=root)
      |-- "Materiais"     --> tela_materiais.py::tela_materiais(root_anterior=root)
      |-- "Relatorios"    --> tela_servico.py::tela_execucao_servico(root_anterior=root)
```

### Fluxo de cadastro (exemplo cliente):
```
tela_clientes
  |-- "Cadastrar" --> abrir_formulario() [NOVA CTk()]
      |-- "Avancar" --> salvar_e_avancar()
          |-- listar_carros_cliente() [NOVA CTk()]
              |-- "+ Novo Carro" --> abrir_formulario_carro() [NOVA CTk()]
                  |-- "Avancar" --> listar_servicos() [NOVA CTk()]
                      |-- "Salvar Ordem" --> tela_dashboard() [NOVA CTk()]
```

## Estrutura de Arquivos

```
softcar/
  main.py                    -- Ponto de entrada (login)
  view/
    bemvindo.py              -- Dashboard (tela inicial apos login)
    tela_clientes.py         -- Lista de clientes + sub-telas (1160 linhas, maior arquivo)
    tela_servicos.py         -- Lista de servicos + formulario
    tela_servico.py          -- Execucao de servico (relatorios)
    tela_materiais.py        -- Lista de materiais/estoque + formulario
    lista_funcionarios.py    -- Lista de funcionarios + formulario
    tela_login.py            -- Login antigo (NAO USADO)
  banco/
    banco.sql                -- Schema completo do banco
    db_config.py             -- Config de BD (QUEBRADO, nao usado)
    script.sql               -- Dados de teste
    insert_estoque.sql       -- Seed de materiais
  scripts/
    *.sql                    -- Scripts de migracao e seeds
  assets/
    *.png                    -- Imagens de fundo, icones, botoes
  venv/                      -- Ambiente virtual
```

## Arquivos de View - Detalhamento

### main.py (209 linhas)
- **tela_login()**: Cria janela de login com canvas, imagem de fundo, entries responsivos
- **verificar_login()**: Valida email/senha contra tabela `funcionarios`, navega para dashboard
- Usa `root.after(100, lambda: tela_dashboard(cargo, root_anterior=root))` para navegacao

### view/bemvindo.py (269 linhas)
- **tela_dashboard(cargo, root_anterior=None)**: Tela principal com cards de metricas
- Metricas: servicos agendados, realizados, clientes, veiculos, total recebido
- Sidebar desenhada no canvas (itens de menu com icones + texto)
- Navega via `root.after(10, lambda: ...)` para todas as telas

### view/tela_clientes.py (1160 linhas) -- MAIOR ARQUIVO
Funcoes principais:
- **tela_clientes(root_anterior=None)**: Lista de clientes com treeview
- **abrir_formulario(tree, dados=None)**: Formulario de cliente (NOVA CTk)
- **abrir_formulario_carro(...)**: Formulario de carro (NOVA CTk)
- **listar_carros_cliente(...)**: Lista de carros do cliente (NOVA CTk)
- **listar_servicos(...)**: Selecao de servicos para ordem (NOVA CTk)
- **excluir_cliente(tree)**: Exclusao de cliente

### view/tela_servicos.py (587 linhas)
- **tela_servicos(root_anterior=None)**: Lista de servicos
- **abrir_formulario_servico(tree, dados=None, root_anterior=None)**: Formulario (NOVA CTk)
- **excluir_servico(tree)**: Exclusao

### view/tela_servico.py (246 linhas)
- **tela_execucao_servico(root_anterior=None)**: Lista de ordens abertas
- **finalizar_ordem()**: Marca ordem como 'finalizado'

### view/tela_materiais.py (503 linhas)
- **tela_materiais(root_anterior=None)**: Lista de materiais
- **abrir_formulario_material(tree, dados=None)**: Formulario (CTkToplevel -- unico que usa Toplevel)
- **excluir_material(tree)**: Exclusao

### view/lista_funcionarios.py (509 linhas)
- **tela_lista_funcionarios(root_anterior=None)**: Lista de funcionarios
- **abrir_formulario(tree, dados=None)**: Formulario (CTkToplevel)
- **excluir_funcionario(tree)**: Exclusao

## Banco de Dados

### Tabelas:
- **funcionarios**: id_func, nome_func, email_func, cpf_func, senha, cargo (ENUM: lavador/atendente), endereco_func, data_nascimento_func, telefone_func
- **clientes**: id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco, data_nascimento
- **carros**: id_carro, placa, modelo, marca, cor
- **clientes_has_carros**: clientes_id_cliente, carros_id_carro (tabela associativa)
- **estoque**: id_produto, tipo, quantidade
- **servicos**: id_servico, nome_servico, preco_servico, estoque_id_produto, data_hora_servico
- **ordem_servico**: id_ordem, id_cliente, id_carro, data_hora, total, status (DEFAULT 'aberto')
- **ordem_servico_itens**: id_item, id_ordem, id_servico, preco

### Conexao:
```python
mysql.connector.connect(host="localhost", user="root", password="", database="softcar")
```
Cada arquivo define sua propria funcao `conectar()`. O `banco/db_config.py` existe mas esta quebrado e nao e usado.

## Queries SQL por Funcao

### Login:
- `SELECT * FROM funcionarios WHERE email_func = %s AND senha = %s`

### Dashboard:
- `SELECT COUNT(*) FROM ordem_servico WHERE status = 'aberto'`
- `SELECT COUNT(*) FROM ordem_servico WHERE status = 'finalizado'`
- `SELECT COUNT(*) FROM clientes`
- `SELECT COUNT(*) FROM carros`
- `SELECT COALESCE(SUM(total), 0) FROM ordem_servico WHERE status = 'finalizado'`

### Clientes:
- `SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco FROM clientes ORDER BY nome_cliente`
- `SELECT ... WHERE nome_cliente LIKE %s OR email_cliente LIKE %s OR cpf LIKE %s`
- `INSERT INTO clientes (...) VALUES (...)`
- `UPDATE clientes SET ... WHERE id_cliente=%s`
- `DELETE FROM clientes WHERE id_cliente = %s`
- `SELECT * FROM clientes WHERE id_cliente = %s`

### Carros:
- `INSERT INTO carros (placa, modelo, marca, cor) VALUES (...)`
- `UPDATE carros SET ... WHERE id_carro=%s`
- `INSERT INTO clientes_has_carros (clientes_id_cliente, carros_id_carro) VALUES (...)`
- `SELECT c.id_carro, c.placa, c.modelo, c.marca, c.cor FROM carros c INNER JOIN clientes_has_carros chc WHERE chc.clientes_id_cliente = %s`

### Servicos:
- `SELECT id_servico, nome_servico, estoque_id_produto, data_hora_servico FROM servicos ORDER BY nome_servico`
- `SELECT id_servico, nome_servico, preco_servico FROM servicos ORDER BY nome_servico`
- `INSERT INTO servicos (...) VALUES (...)`
- `UPDATE servicos SET ... WHERE id_servico=%s`
- `DELETE FROM servicos WHERE id_servico = %s`
- `SELECT id_produto, tipo FROM estoque ORDER BY tipo` (para combobox)

### Materiais/Estoque:
- `SELECT id_produto, tipo, quantidade FROM estoque ORDER BY tipo`
- `INSERT INTO estoque (tipo, quantidade) VALUES (...)`
- `UPDATE estoque SET ... WHERE id_produto=%s`
- `DELETE FROM estoque WHERE id_produto = %s`

### Funcionarios:
- `SELECT id_func, nome_func, email_func, telefone_func, cpf_func, cargo FROM funcionarios ORDER BY nome_func`
- `INSERT INTO funcionarios (...) VALUES (...)`
- `UPDATE funcionarios SET ... WHERE id_func=%s`
- `DELETE FROM funcionarios WHERE id_func = %s`

### Ordens de Servico:
- `SELECT os.id_ordem, c.nome_cliente, cr.placa, os.total, os.data_hora FROM ordem_servico os JOIN clientes c LEFT JOIN carros cr WHERE os.status = 'aberto'`
- `INSERT INTO ordem_servico (id_cliente, id_carro, total) VALUES (...)`
- `INSERT INTO ordem_servico_itens (id_ordem, id_servico, preco) VALUES (...)`
- `UPDATE ordem_servico SET status = 'finalizado' WHERE id_ordem = %s`

## Padroes de UI

### Sidebar (copiada em TODOS os arquivos):
```python
icones_info = [
    ("Cliente",      "assets/cliente.png"),
    ("Servicos",     "assets/servicos.png"),
    ("Funcionarios", "assets/funcionarios.png"),
    ("Materiais",    "assets/materiais.png"),
    ("Relatorios",   "assets/relatorios.png"),
]
```
- Itens desenhados no canvas (create_image + create_text)
- Hover: texto fica dourado (#b88b4a)
- Tela ativa: texto cinza (#777777)
- Posicao: y_pos comeca em 220, incrementa 50 por item

### Cores:
- Dourado: #b88b4a
- Branco: #ffffff
- Cinza: #777777
- Fundo: #2b3e50
- Menu bg: #2b3e50
- Menu hover: #3a536b
- Botao cancelar: #375269
- Botao cancelar hover: #2c4a5c
- Treeview bg: #375269
- Treeview heading: #2c4a5c
- Entry fg: #c2c7cc
- Entry text: #000000

### Maximizacao:
Todas as telas usam:
```python
root.state("zoomed")
try:
    root.attributes('-zoomed', True)
except:
    pass
```
Chamado tanto imediatamente apos criacao quanto via `root.after(100/200, maximizar)`

### Fundo responsivo:
Todas as telas carregam uma imagem PNG e redimensionam no `<Configure>`:
```python
img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
bg_image_tk = ImageTk.PhotoImage(img_resized)
canvas.delete("bg")
canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
canvas.tag_lower("bg")
```
- Listas: assets/tabela.png
- Formularios: assets/formulario.png
- Dashboard: assets/dashboard.png (note: arquivo e Dashboard.png com D maiusculo)

### Layout responsivo (listas):
```python
cx = w * 0.191    # inicio X da area de conteudo
cy = h * 0.178    # inicio Y da area de conteudo
cw = w * 0.753    # largura da area de conteudo
ch = h * 0.750    # altura da area de conteudo
```

### Layout responsivo (formularios):
```python
form_w = min(500, w * 0.45)
cx = w * 0.5
cy_inicio = h * 0.15
entry_w = int(form_w * 0.65)
espacamento = max(45, min(60, h * 0.08))
```

## Problemas Conhecidos

1. **"invalid command name"**: Callbacks `after` do customtkinter ficam orfaos quando janelas sao destruidas durante navegacao
2. **Sidebar duplicada**: Cada arquivo recria a sidebar completa (~30-50 linhas identicas)
3. **Funcoes duplicadas**: `_carregar_icone`, `_criar_icone_fallback`, `conectar` definidas em todos os arquivos
4. **banco/db_config.py quebrado**: Usa `senha=` ao inves de `password=`, `cursor.retchome()` ao inves de `cursor.fetchone()`
5. **Navegar apos destroy**: Algumas chamadas de navegacao tentam usar a janela ja destruida
6. **Imagem dashboard**: Codigo referencia `dashboard.png` mas arquivo e `Dashboard.png` (D maiusculo)
7. **tela_login.py**: Arquivo nao utilizado (login real esta no main.py)

## Assets

| Arquivo | Uso |
|---------|-----|
| Login.png | Fundo da tela de login |
| Dashboard.png | Fundo do dashboard |
| tabela.png | Fundo das telas de lista |
| formulario.png | Fundo dos formularios |
| cliente.png | Icone sidebar |
| servicos.png | Icone sidebar |
| funcionarios.png | Icone sidebar |
| materiais.png | Icone sidebar |
| relatorios.png | Icone sidebar |
| txt_email.png | Label do campo email no login |
| txt_senha.png | Label do campo senha no login |
| btn_entrar.png | Botao de entrar no login |
