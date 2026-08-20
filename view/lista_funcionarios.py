import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from view.img_softcar_utils import carregar_img_softcar, criar_img_softcar, redimensionar_img_softcar
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
        for i, row in enumerate(cursor.fetchall()):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
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
        resultados = cursor.fetchall()
        for i, row in enumerate(resultados):
            tag = "even" if i % 2 == 0 else "odd"
            item_id = tree.insert("", "end", values=row, tags=(tag,))
            if i == 0 and termo:
                tree.selection_set(item_id)
                tree.see(item_id)
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")


def abrir_formulario(tree, dados=None):
    root_anterior = tree.winfo_toplevel()
    root_anterior.destroy()
    modal = ctk.CTk()
    modal.title("Editar Funcionário" if dados else "Novo Funcionário")
    modal.state("zoomed")
    modal.minsize(800, 500)
    modal.resizable(True, True)
    try:
        modal.attributes('-zoomed', True)
    except:
        pass

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_cinza = "#777777"

    img_fundo = "assets/cadastrar_funcionarios.png" if not dados else "assets/editar_funcionarios.png"
    if not os.path.exists(img_fundo):
        img_fundo = "assets/img_frame.png"

    canvas = ctk.CTkCanvas(modal, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_softcar_original_form_func = carregar_img_softcar()
    if img_softcar_original_form_func:
        btn_dashboard_id_form_func, img_softcar_tk_form_func = criar_img_softcar(canvas, img_softcar_original_form_func)
        canvas.tag_bind("dashboard_img", "<Button-1>", lambda e: ir_dashboard_form_func())
        canvas.tag_bind("dashboard_img", "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind("dashboard_img", "<Leave>", lambda e: canvas.config(cursor=""))

    def ir_dashboard_form_func():
        from view.bemvindo import tela_dashboard
        modal.after(10, lambda: tela_dashboard(root_anterior=modal))

    bg_img_original = None
    if os.path.exists(img_fundo):
        bg_img_original = Image.open(img_fundo)

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def acao_menu(opcao):
        def _navegar():
            modal.destroy()
            if opcao == "Cliente":
                from view.tela_clientes import tela_clientes
                tela_clientes()
            elif opcao == "Serviços":
                from view.tela_servicos import tela_servicos
                tela_servicos()
            elif opcao == "Funcionários":
                from view.lista_funcionarios import tela_lista_funcionarios
                tela_lista_funcionarios()
            elif opcao == "Materiais":
                from view.tela_materiais import tela_materiais
                tela_materiais()
            elif opcao == "Relatórios":
                from view.tela_servico import tela_execucao_servico
                tela_execucao_servico()
        modal.after(100, _navegar)

    y_pos = 120
    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        ativo = (nome == "Funcionários")
        cor_texto = cor_cinza if ativo else cor_branco

        img_item = canvas.create_image(20, y_pos, image=icone, anchor="nw")
        txt_item = canvas.create_text(50, y_pos + 12, text=nome, font=("Arial", 11, "bold"), fill=cor_texto, anchor="nw")

        def on_enter(e, txt=txt_item):
            canvas.itemconfig(txt, fill=cor_dourado)
        def on_leave(e, txt=txt_item, cor=cor_texto):
            canvas.itemconfig(txt, fill=cor)

        canvas.tag_bind(img_item, "<Enter>", on_enter)
        canvas.tag_bind(img_item, "<Leave>", on_leave)
        canvas.tag_bind(txt_item, "<Enter>", on_enter)
        canvas.tag_bind(txt_item, "<Leave>", on_leave)

        def make_handler(opcao):
            return lambda e: acao_menu(opcao)

        canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
        canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))

        canvas.image_refs = getattr(canvas, "image_refs", [])
        canvas.image_refs.append(icone)
        y_pos += 50

    campos = ["nome_func", "email_func", "telefone_func", "cpf_func", "cargo", "endereco_func", "data_nascimento_func", "senha"]
    labels = ["Nome", "E-mail", "Telefone", "CPF", "Cargo (lavador/atendente)", "Endereço", "Data de Nasc.", "Senha"]
    entries = {}
    itens_form = []

    x_label = 400
    x_entry = 420
    y_inicio = 100

    for i, (campo, label) in enumerate(zip(campos, labels)):
        y_atual = y_inicio + i * 55
        lbl = canvas.create_text(x_label, y_atual, text=label, font=("Arial", 11, "bold"), fill="#ffffff", anchor="e")
        entry = ctk.CTkEntry(canvas, width=35*10, fg_color="#c2c7cc", text_color="#000000", font=("Arial", 12))
        entry_win = canvas.create_window(x_entry, y_atual, window=entry, anchor="w")
        if dados:
            entry.insert(0, dados[campo] if dados[campo] is not None else "")
        entries[campo] = entry
        itens_form.append((lbl, entry_win))

    def salvar():
        valores = {}
        for campo, label in zip(campos, labels):
            if not entries[campo].get().strip():
                messagebox.showwarning("Validação", f"O campo {label} é obrigatório.")
                return
            valores[campo] = entries[campo].get().strip()
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
            tela_lista_funcionarios()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    def voltar():
        modal.destroy()
        tela_lista_funcionarios()

    btn_salvar_img_original = Image.open("assets/btn_salvar.png") if os.path.exists("assets/btn_salvar.png") else None
    btn_salvar_img = None
    if btn_salvar_img_original:
        btn_salvar_img_resized = btn_salvar_img_original.resize((60, 25), Image.Resampling.LANCZOS)
        btn_salvar_img = ImageTk.PhotoImage(btn_salvar_img_resized)
    btn_salvar_win = canvas.create_image(0, 0, image=btn_salvar_img, anchor="nw")
    canvas.image_refs = getattr(canvas, "image_refs", [])
    canvas.image_refs.append(btn_salvar_img)
    canvas.tag_bind(btn_salvar_win, "<Button-1>", lambda e: salvar())
    canvas.tag_bind(btn_salvar_win, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(btn_salvar_win, "<Leave>", lambda e: canvas.config(cursor=""))

    btn_excluir_img_original = Image.open("assets/btn_excluir.png") if os.path.exists("assets/btn_excluir.png") else None
    btn_excluir_img = None
    if btn_excluir_img_original:
        btn_excluir_img_resized = btn_excluir_img_original.resize((60, 25), Image.Resampling.LANCZOS)
        btn_excluir_img = ImageTk.PhotoImage(btn_excluir_img_resized)
    btn_excluir_win = canvas.create_image(0, 0, image=btn_excluir_img, anchor="nw")
    canvas.image_refs.append(btn_excluir_img)

    def excluir_func_form():
        if not dados:
            return
        if not messagebox.askyesno("Excluir", "Tem certeza que deseja excluir este funcionário?"):
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM funcionarios WHERE id_func = %s", (dados["id_func"],))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
            modal.after(100, lambda: (modal.destroy(), tela_lista_funcionarios()))
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

    canvas.tag_bind(btn_excluir_win, "<Button-1>", lambda e: excluir_func_form())
    canvas.tag_bind(btn_excluir_win, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(btn_excluir_win, "<Leave>", lambda e: canvas.config(cursor=""))

    def voltar_login():
        modal.destroy()
        from main import tela_login
        tela_login()

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    def _redimensionar(event=None):
        if event is not None and event.widget != modal:
            return
        w, h = modal.winfo_width(), modal.winfo_height()
        if w < 10 or h < 10:
            return

        if bg_img_original:
            img_resized = bg_img_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_tk = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_tk, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
            canvas.image_bg = bg_tk

        form_w = min(500, w * 0.45)
        cx = w * 0.5 + 50
        cy_inicio = h * 0.15 + 100
        entry_w = int(form_w * 0.65)
        espacamento = max(45, min(60, h * 0.08))

        for i, (lbl, entry_win) in enumerate(itens_form):
            cy = cy_inicio + i * espacamento
            canvas.coords(lbl, cx - entry_w // 2 + 90, cy)
            canvas.coords(entry_win, cx + entry_w // 2 - 100, cy)
            canvas.itemconfig(entry_win, width=entry_w)

        y_btns = cy_inicio + len(campos) * espacamento + 20
        if btn_salvar_img_original:
            btn_w = int(60 * w / 800)
            btn_h = int(25 * h / 600)
            btn_salvar_resized = btn_salvar_img_original.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
            btn_salvar_img_tk = ImageTk.PhotoImage(btn_salvar_resized)
            canvas.itemconfig(btn_salvar_win, image=btn_salvar_img_tk)
            canvas.image_refs = getattr(canvas, "image_refs", [])
            canvas.image_refs.append(btn_salvar_img_tk)
        canvas.coords(btn_salvar_win, cx - 55, y_btns)
        canvas.tag_raise(btn_salvar_win)

        if btn_excluir_img_original and dados:
            btn_w = int(60 * w / 800)
            btn_h = int(25 * h / 600)
            btn_excluir_resized = btn_excluir_img_original.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
            btn_excluir_img_tk = ImageTk.PhotoImage(btn_excluir_resized)
            canvas.itemconfig(btn_excluir_win, image=btn_excluir_img_tk)
            canvas.image_refs.append(btn_excluir_img_tk)
            canvas.coords(btn_excluir_win, cx + 155, y_btns)
        elif not dados:
            canvas.coords(btn_excluir_win, -200, -200)
        canvas.coords(btn_sair_win, w * 0.02, h - 50)

        redimensionar_img_softcar(canvas, btn_dashboard_id_form_func, img_softcar_original_form_func, w, h)

    modal.bind("<Configure>", _redimensionar)
    modal.after(100, _redimensionar)

    def maximizar():
        modal.update_idletasks()
        modal.state("zoomed")
        try:
            modal.attributes('-zoomed', True)
        except:
            pass
    modal.after(100, maximizar)

    modal.mainloop()

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

def _criar_icone_fallback(tamanho, cor, forma="circle"):
    from PIL import ImageDraw
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if forma == "circle":
        draw.ellipse([2, 2, tamanho-2, tamanho-2], fill=cor)
    elif forma == "square":
        draw.rectangle([2, 2, tamanho-2, tamanho-2], fill=cor)
    return ImageTk.PhotoImage(img)

def tela_lista_funcionarios(root_anterior=None):
    if root_anterior:
        root_anterior.destroy()
    root = ctk.CTk()
    root.title("Soft Car - Lista de Funcionários")
    root.state("zoomed")
    root.minsize(800, 500)
    root.resizable(True, True)
    try:
        root.attributes('-zoomed', True)
    except:
        pass

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_fundo = "#2b3e50"

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def navegar(opcao):
        if opcao == "Funcionários":
            return
        def _navegar():
            if opcao == "Cliente":
                from view.tela_clientes import tela_clientes
                tela_clientes(root_anterior=root)
            elif opcao == "Serviços":
                from view.tela_servicos import tela_servicos
                tela_servicos(root_anterior=root)
            elif opcao == "Materiais":
                from view.tela_materiais import tela_materiais
                tela_materiais(root_anterior=root)
            elif opcao == "Relatórios":
                from view.tela_servico import tela_execucao_servico
                tela_execucao_servico(root_anterior=root)
        root.after(10, _navegar)

    canvas = ctk.CTkCanvas(root, highlightthickness=0, bg=cor_fundo)
    canvas.pack(fill="both", expand=True)

    def ir_dashboard():
        from view.bemvindo import tela_dashboard
        root.after(10, lambda: tela_dashboard(root_anterior=root))

    img_softcar_original = carregar_img_softcar()

    btn_dashboard_id = None
    if img_softcar_original:
        btn_dashboard_id, img_softcar_tk_init = criar_img_softcar(canvas, img_softcar_original)
        canvas.tag_bind("dashboard_img", "<Button-1>", lambda e: ir_dashboard())
        canvas.tag_bind("dashboard_img", "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind("dashboard_img", "<Leave>", lambda e: canvas.config(cursor=""))

    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img_frame.png")
    img_original = None
    if os.path.exists(img_path):
        img_original = Image.open(img_path)

    bg_image_tk = None
    menu_criado = False
    botoes_menu = []
    canvas.image_refs = []

    style = ttk.Style()
    style.theme_use("clam")
    style.layout("Treeview", [
        ("Treeview.field", {"sticky": "nswe", "children": [
            ("Treeview.padding", {"sticky": "nswe", "children": [
                ("Treeview.treearea", {"sticky": "nswe"})
            ]})
        ]})
    ])
    style.configure("Treeview",
                    background="#375269",
                    foreground=cor_branco,
                    fieldbackground="#375269",
                    rowheight=28,
                    borderwidth=0,
                    bordercolor="#375269",
                    lightcolor="#375269",
                    darkcolor="#375269",
                    troughcolor="#375269")
    style.configure("Treeview.Heading",
                    background="#2c4a5c",
                    foreground=cor_branco,
                    relief="flat",
                    borderwidth=0,
                    bordercolor="#2c4a5c",
                    lightcolor="#2c4a5c",
                    darkcolor="#2c4a5c",
                    troughcolor="#2c4a5c")
    style.layout("Treeview.Heading", [
        ("Treeview.Heading.cell", {"sticky": "nswe", "children": [
            ("Treeview.Heading.padding", {"sticky": "nswe", "children": [
                ("Treeview.Heading.label", {"sticky": "nswe"})
            ]})
        ]})
    ])
    style.map("Treeview",
              background=[("selected", cor_dourado)])
    style.map("Treeview.Heading",
              background=[("active", "#2c4a5c")],
              relief=[("active", "flat")])

    style.configure("Vertical.TScrollbar",
                    background="#375269",
                    troughcolor="#375269",
                    borderwidth=0,
                    relief="flat",
                    lightcolor="#375269",
                    darkcolor="#375269",
                    arrowcolor="#375269")

    frame_top = ctk.CTkFrame(canvas, fg_color="#375269")
    frame_top_window = canvas.create_window(0, 0, window=frame_top, anchor="nw")

    ctk.CTkLabel(frame_top, text="Pesquisar", font=("Arial", 11, "bold"), text_color=cor_branco, fg_color="transparent").pack(side="left", padx=5)
    entry_busca = ctk.CTkEntry(frame_top, width=20*10, fg_color="#375269", text_color="#ffffff", placeholder_text="Pesquisar...", font=("Arial", 10))
    entry_busca.pack(side="left", padx=5, ipady=3)
    
    def _buscar(*args):
        buscar_funcionarios(tree, entry_busca)
    
    entry_busca.bind("<KeyRelease>", _buscar)

    btn_cadastrar_img_original = Image.open("assets/btn_funcionario.png") if os.path.exists("assets/btn_funcionario.png") else None
    btn_cadastrar_img = None
    if btn_cadastrar_img_original:
        btn_cadastrar_img_resized = btn_cadastrar_img_original.resize((65, 25), Image.Resampling.LANCZOS)
        btn_cadastrar_img = ImageTk.PhotoImage(btn_cadastrar_img_resized)
    btn_cadastrar_window = canvas.create_image(0, 0, image=btn_cadastrar_img, anchor="nw")
    canvas.image_refs = getattr(canvas, "image_refs", [])
    canvas.image_refs.append(btn_cadastrar_img)
    canvas.tag_bind(btn_cadastrar_window, "<Button-1>", lambda e: abrir_formulario(tree))
    canvas.tag_bind(btn_cadastrar_window, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(btn_cadastrar_window, "<Leave>", lambda e: canvas.config(cursor=""))

    def cmd_editar():
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

    def cmd_excluir():
        excluir_funcionario(tree)

    frame_tabela = ctk.CTkFrame(canvas, fg_color="#375269")
    frame_tabela_window = canvas.create_window(0, 0, window=frame_tabela, anchor="nw")

    colunas = ("id_func", "nome_func", "email_func", "telefone_func", "cpf_func", "cargo")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse", height=15)
    tree.heading("id_func", text="ID", anchor="center")
    tree.heading("nome_func", text="Nome", anchor="center")
    tree.heading("email_func", text="E-mail", anchor="center")
    tree.heading("telefone_func", text="Telefone", anchor="center")
    tree.heading("cpf_func", text="CPF", anchor="center")
    tree.heading("cargo", text="Cargo", anchor="center")
    tree.column("id_func", width=0, stretch=False)
    tree.column("cpf_func", width=0, stretch=False)
    tree.column("nome_func", width=180, anchor="center")
    tree.column("email_func", width=200, anchor="center")
    tree.column("telefone_func", width=120, anchor="center")
    tree.column("cargo", width=100, anchor="center")

    tree.tag_configure("odd", background="#375269")
    tree.tag_configure("even", background="#375269")

    tree.bind("<Double-1>", lambda e: cmd_editar())

    btn_editar_img_original = Image.open("assets/btn_editar.png") if os.path.exists("assets/btn_editar.png") else None
    btn_editar_img = None
    if btn_editar_img_original:
        btn_editar_img_resized = btn_editar_img_original.resize((60, 25), Image.Resampling.LANCZOS)
        btn_editar_img = ImageTk.PhotoImage(btn_editar_img_resized)
    btn_editar_window = canvas.create_image(0, 0, image=btn_editar_img, anchor="nw")
    canvas.image_refs.append(btn_editar_img)
    canvas.tag_bind(btn_editar_window, "<Button-1>", lambda e: cmd_editar())
    canvas.tag_bind(btn_editar_window, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(btn_editar_window, "<Leave>", lambda e: canvas.config(cursor=""))

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")

    def _atualizar_scrollbar(*args):
        scrollbar.set(*args)

    tree.configure(yscrollcommand=_atualizar_scrollbar)

    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    carregar_funcionarios(tree)

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
                if icone is None:
                    icone = _criar_icone_fallback(24, cor_dourado, "circle")

                ativo = (nome == "Funcionários")
                cor_texto = "#777777" if ativo else cor_branco
                img_item = canvas.create_image(20, y_pos, image=icone, anchor="nw")
                txt_item = canvas.create_text(50, y_pos + 12, text=nome, font=("Arial", 11, "bold"), fill=cor_texto, anchor="nw")

                def make_handler(opcao):
                    return lambda e: navegar(opcao)

                canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
                canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))

                def on_enter(e, txt=txt_item):
                    canvas.itemconfig(txt, fill=cor_dourado)
                def on_leave(e, txt=txt_item, cor=cor_texto):
                    canvas.itemconfig(txt, fill=cor)

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

        canvas.coords(frame_top_window, cx + 130, cy - 145)
        if btn_cadastrar_img_original:
            btn_w = int(65 * w / 800)
            btn_h = int(25 * h / 600)
            btn_cadastrar_img_resized = btn_cadastrar_img_original.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
            btn_cadastrar_img_tk = ImageTk.PhotoImage(btn_cadastrar_img_resized)
            canvas.itemconfig(btn_cadastrar_window, image=btn_cadastrar_img_tk)
            canvas.image_refs.append(btn_cadastrar_img_tk)
        canvas.coords(btn_cadastrar_window, cx + cw - 260, cy - 145)
        canvas.coords(frame_tabela_window, cx + 176, cy - 42)
        canvas.itemconfig(frame_tabela_window, width=max(100, cw - 254), height=max(100, ch - 122))
        canvas.coords(btn_sair_win, w * 0.02, h - 50)

        cx_table = cx + 176
        cw_table = max(100, cw - 254)
        if btn_editar_img_original:
            btn_w = int(60 * w / 800)
            btn_h = int(25 * h / 600)
            btn_editar_resized = btn_editar_img_original.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
            btn_editar_img_tk = ImageTk.PhotoImage(btn_editar_resized)
            canvas.itemconfig(btn_editar_window, image=btn_editar_img_tk)
            canvas.image_refs.append(btn_editar_img_tk)
        canvas.coords(btn_editar_window, cx_table + cw_table / 2, h - 180)

        redimensionar_img_softcar(canvas, btn_dashboard_id, img_softcar_original, w, h)

    def redimensionar(event):
        if event.widget != root:
            return
        w, h = event.width, event.height
        if w < 10 or h < 10:
            return
        _redimensionar(w, h)

    root.bind("<Configure>", redimensionar)
    root.after(100, lambda: [root.update_idletasks(), _redimensionar(root.winfo_width(), root.winfo_height())])

    def maximizar():
        root.update_idletasks()
        root.state("zoomed")
        try:
            root.attributes('-zoomed', True)
        except:
            pass
    root.after(100, maximizar)

    def voltar_login():
        root.destroy()
        from main import tela_login
        tela_login()

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    root.mainloop()


if __name__ == "__main__":
    tela_lista_funcionarios()