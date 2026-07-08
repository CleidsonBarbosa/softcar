import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="softcar"
    )

def carregar_funcionarios(tree):
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_func, nome_func, email_func, telefone_func, cpf_func, cargo FROM funcionarios ORDER BY nome_func")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao carregar funcionários:\n{e}")

def buscar_funcionarios(tree, entry_busca):
    termo = entry_busca.get().strip()
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        if termo:
            cursor.execute(
                "SELECT id_func, nome_func, email_func, telefone_func, cpf_func, cargo FROM funcionarios WHERE nome_func LIKE %s OR email_func LIKE %s OR cpf_func LIKE %s OR cargo LIKE %s ORDER BY nome_func",
                (f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%")
            )
        else:
            cursor.execute("SELECT id_func, nome_func, email_func, telefone_func, cpf_func, cargo FROM funcionarios ORDER BY nome_func")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")

def abrir_formulario(tree, dados=None):
    modal = tk.Toplevel()
    modal.title("Editar Funcionário" if dados else "Novo Funcionário")
    modal.geometry("400x450")
    modal.resizable(False, False)
    modal.transient(tree.winfo_toplevel())
    modal.grab_set()

    frame = ttk.Frame(modal, padding=20)
    frame.pack(fill="both", expand=True)

    campos = ["nome_func", "email_func", "telefone_func", "cpf_func", "cargo", "endereco_func", "data_nascimento_func", "senha"]
    labels = ["Nome", "E-mail", "Telefone", "CPF", "Cargo (lavador/atendente)", "Endereço", "Data de Nascimento (YYYY-MM-DD)", "Senha"]
    entries = {}

    for i, (campo, label) in enumerate(zip(campos, labels)):
        ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=4)
        entry = ttk.Entry(frame, width=40)
        entry.grid(row=i, column=1, pady=4)
        if dados:
            entry.insert(0, dados[campo])
        entries[campo] = entry

    def salvar():
        valores = {}
        for campo, entry in entries.items():
            if not entry.get().strip():
                messagebox.showwarning("Validação", f"O campo {labels[campos.index(campo)]} é obrigatório.")
                return
            valores[campo] = entry.get().strip()
        try:
            conn = conectar()
            cursor = conn.cursor()
            if dados:
                cursor.execute(
                    "UPDATE funcionarios SET nome_func=%s, email_func=%s, telefone_func=%s, cpf_func=%s, cargo=%s, endereco_func=%s, data_nascimento_func=%s, senha=%s WHERE id_func=%s",
                    (valores["nome_func"], valores["email_func"], valores["telefone_func"], valores["cpf_func"], valores["cargo"], valores["endereco_func"], valores["data_nascimento_func"] if valores["data_nascimento_func"] else None, valores["senha"], dados["id_func"])
                )
            else:
                cursor.execute(
                    "INSERT INTO funcionarios (nome_func, email_func, telefone_func, cpf_func, cargo, endereco_func, data_nascimento_func, senha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (valores["nome_func"], valores["email_func"], valores["telefone_func"], valores["cpf_func"], valores["cargo"], valores["endereco_func"], valores["data_nascimento_func"] if valores["data_nascimento_func"] else None, valores["senha"])
                )
            conn.commit()
            cursor.close()
            conn.close()
            modal.destroy()
            carregar_funcionarios(tree)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
    ttk.Button(btn_frame, text="Salvar", command=salvar).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Cancelar", command=modal.destroy).pack(side="left", padx=5)

def excluir_funcionario(tree):
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um funcionário na lista.")
        return
    if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este funcionário?"):
        return
    id_func = tree.item(selecionado[0])["values"][0]
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM funcionarios WHERE id_func = %s", (id_func,))
        conn.commit()
        cursor.close()
        conn.close()
        carregar_funcionarios(tree)
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

def _carregar_icone(caminho, tamanho):
    try:
        img = Image.open(caminho)
        img = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

def tela_lista_funcionarios():
    janela = tk.Toplevel()
    janela.title("Soft Car - Lista de Funcionários")
    janela.geometry("1000x600")
    janela.minsize(800, 500)

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_fundo = "#2b3e50"
    cor_fundo2 = "#1a2735"
    MENU_X_START = 160

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def acao_menu(opcao):
        if opcao == "Cliente":
            from view.lista_clientes import tela_lista_clientes
            tela_lista_clientes()
        elif opcao == "Funcionários":
            pass
        else:
            messagebox.showinfo("Soft Car", f"Você clicou na opção: {opcao}")

    canvas = tk.Canvas(janela, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_path = "assets/listar_funcionarios.png"
    img_original = None
    if os.path.exists(img_path):
        img_original = Image.open(img_path)

    bg_image_tk = None
    menu_criado = False
    botoes_menu = []
    canvas.image_refs = []

    # ---- ESTILO ESCURO ----
    style = ttk.Style()
    style.theme_use("clam")
    style.layout("Treeview", [
        ("Treeview.field", {"sticky": "nswe", "border": 0, "children": [
            ("Treeview.padding", {"sticky": "nswe", "children": [
                ("Treeview.treearea", {"sticky": "nswe"})
            ]})
        ]})
    ])
    style.configure("Treeview",
                    background=cor_fundo,
                    foreground=cor_branco,
                    fieldbackground=cor_fundo,
                    borderwidth=0)
    style.configure("Treeview.Heading",
                    background=cor_fundo2,
                    foreground=cor_branco,
                    relief="flat",
                    borderwidth=0)
    style.map("Treeview",
              background=[("selected", cor_dourado)])

    # ---- BARRA DE BUSCA ----
    frame_top = tk.Frame(canvas, bg=cor_fundo, padx=10, pady=10)
    frame_top_window = canvas.create_window(0, 0, window=frame_top, anchor="nw")

    tk.Label(frame_top, text="Buscar:", font=("Arial", 10), bg=cor_fundo, fg=cor_branco).pack(side="left", padx=5)
    entry_busca = tk.Entry(frame_top, width=30, font=("Arial", 10))
    entry_busca.pack(side="left", padx=5)
    tk.Button(frame_top, text="Buscar", font=("Arial", 9, "bold"), bg=cor_fundo2, fg=cor_branco, bd=0, command=lambda: buscar_funcionarios(tree, entry_busca)).pack(side="left", padx=5)
    tk.Button(frame_top, text="Limpar", font=("Arial", 9, "bold"), bg=cor_fundo2, fg=cor_branco, bd=0, command=lambda: [entry_busca.delete(0, "end"), carregar_funcionarios(tree)]).pack(side="left", padx=5)

    # ---- BOTÕES DE AÇÃO ----
    frame_btns = tk.Frame(canvas, bg=cor_fundo, padx=10, pady=5)
    frame_btns_window = canvas.create_window(0, 0, window=frame_btns, anchor="nw")
    tk.Button(frame_btns, text="Novo", font=("Arial", 9, "bold"), bg=cor_fundo2, fg=cor_branco, bd=0, command=lambda: abrir_formulario(tree)).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Editar", font=("Arial", 9, "bold"), bg=cor_fundo2, fg=cor_branco, bd=0, command=lambda: editar_selecionado(tree)).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Excluir", font=("Arial", 9, "bold"), bg=cor_fundo2, fg=cor_branco, bd=0, command=lambda: excluir_funcionario(tree)).pack(side="left", padx=5)

   # ---- TABELA ----
    colunas = ("id_func", "nome_func", "email_func", "telefone_func", "cpf_func", "cargo")
    tree = ttk.Treeview(canvas, columns=colunas, show="headings", selectmode="browse", height=15)
    tree.heading("id_func", text="ID")
    tree.heading("nome_func", text="Nome")
    tree.heading("email_func", text="E-mail")
    tree.heading("telefone_func", text="Telefone")
    tree.heading("cpf_func", text="CPF")
    tree.heading("cargo", text="Cargo")
    tree.column("id_func", width=0, stretch=False)
    tree.column("cpf_func", width=0, stretch=False)
    tree.column("nome_func", width=250)
    tree.column("email_func", width=250)
    tree.column("telefone_func", width=150, anchor="center")
    tree.column("cargo", width=120, anchor="center")

    scrollbar = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)

    def _atualizar_scrollbar(*args):
        scrollbar.set(*args)
        try:
            low, high = (float(args[0]), float(args[1]))
            state = "hidden" if low <= 0.0 and high >= 1.0 else "normal"
            canvas.itemconfig(scrollbar_window, state=state)
        except (ValueError, IndexError):
            pass

    tree.configure(yscrollcommand=_atualizar_scrollbar)

    tree_window = canvas.create_window(0, 0, window=tree, anchor="nw")
    scrollbar_window = canvas.create_window(0, 0, window=scrollbar, anchor="ne")

    def editar_selecionado(tree):
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um funcionário na lista.")
            return
        id_func = tree.item(selecionado[0])["values"][0]
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM funcionarios WHERE id_func = %s", (id_func,))
            dados = cursor.fetchone()
            cursor.close()
            conn.close()
            if dados:
                abrir_formulario(tree, dados)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")

    carregar_funcionarios(tree)

   # ---- REDIMENSIONAMENTO ----
    def _redimensionar(w, h):
        nonlocal bg_image_tk, menu_criado

        if img_original:
            img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_image_tk = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
            canvas.tag_lower("bg")

        if not menu_criado:
            y_pos = 220
            for nome, arquivo in icones_info:
                icone = _carregar_icone(arquivo, 24)

                img_item = canvas.create_image(20, y_pos, image=icone, anchor="nw")
                txt_item = canvas.create_text(50, y_pos + 12, text=nome, font=("Arial", 11, "bold"), fill=cor_branco, anchor="nw")

                def make_handler(opcao):
                    return lambda e: acao_menu(opcao)

                canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
                canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))

                def on_enter(e, txt=txt_item):
                    canvas.itemconfig(txt, fill=cor_dourado)
                def on_leave(e, txt=txt_item):
                    canvas.itemconfig(txt, fill=cor_branco)

                canvas.tag_bind(img_item, "<Enter>", on_enter)
                canvas.tag_bind(img_item, "<Leave>", on_leave)
                canvas.tag_bind(txt_item, "<Enter>", on_enter)
                canvas.tag_bind(txt_item, "<Leave>", on_leave)

                canvas.image_refs.append(icone)
                botoes_menu.append((img_item, txt_item))
                y_pos += 50
            menu_criado = True

        y = 220
        for img_item, txt_item in botoes_menu:
            canvas.coords(img_item, 20, y)
            canvas.coords(txt_item, 50, y + 12)
            y += 50

        cx = w * 0.191
        cy = h * 0.178
        cw = w * 0.753
        ch = h * 0.750

        canvas.coords(frame_top_window, cx + 2, cy + 2)
        canvas.coords(frame_btns_window, cx + 2, cy + 40)
        canvas.coords(tree_window, cx + 2, cy + 78)
        canvas.itemconfig(tree_window, width=max(100, cw - 8), height=max(100, ch - 85))
        canvas.coords(scrollbar_window, cx + cw - 22, cy + 78)
        canvas.itemconfig(scrollbar_window, height=max(100, ch - 85))
        _atualizar_scrollbar(*tree.yview())

    def redimensionar(event):
        if event.widget != janela:
            return
        w, h = event.width, event.height
        if w < 10 or h < 10:
            return
        _redimensionar(w, h)

    janela.bind("<Configure>", redimensionar)
    janela.after(100, lambda: [janela.update_idletasks(), _redimensionar(janela.winfo_width(), janela.winfo_height())])

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    tela_lista_funcionarios()
    root.mainloop()