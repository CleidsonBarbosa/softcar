import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
import customtkinter as ctk
from view.img_softcar_utils import carregar_img_softcar, criar_img_softcar, redimensionar_img_softcar

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="softcar"
    )


def carregar_clientes(tree):
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco FROM clientes ORDER BY nome_cliente")
        for i, row in enumerate(cursor.fetchall()):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao carregar clientes:\n{e}")


def buscar_clientes(tree, entry_busca):
    termo = entry_busca.get().strip()
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        if termo:
            cursor.execute(
                "SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco FROM clientes WHERE nome_cliente LIKE %s OR email_cliente LIKE %s OR cpf LIKE %s ORDER BY nome_cliente",
                (f"%{termo}%", f"%{termo}%", f"%{termo}%")
            )
        else:
            cursor.execute("SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco FROM clientes ORDER BY nome_cliente")
        for i, row in enumerate(cursor.fetchall()):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")


def abrir_formulario(tree, dados=None):
    root_lista = tree.winfo_toplevel()
    root_lista.destroy()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    modal = ctk.CTk()
    modal.title("Editar Cliente" if dados else "Novo Cliente")
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

    canvas = ctk.CTkCanvas(modal, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_softcar_original_form = carregar_img_softcar()
    btn_dashboard_id_form = None
    if img_softcar_original_form:
        btn_dashboard_id_form, img_softcar_tk_form = criar_img_softcar(canvas, img_softcar_original_form)
        canvas.tag_bind("dashboard_img", "<Button-1>", lambda e: ir_dashboard_form())
        canvas.tag_bind("dashboard_img", "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind("dashboard_img", "<Leave>", lambda e: canvas.config(cursor=""))

    # ---- MENU VERTICAL ----
    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def acao_menu(opcao):
        if opcao == "Cliente":
            return
        def _navegar():
            if opcao == "Serviços":
                from view.tela_servicos import tela_servicos
                tela_servicos(root_anterior=modal)
            elif opcao == "Funcionários":
                from view.lista_funcionarios import tela_lista_funcionarios
                tela_lista_funcionarios(root_anterior=modal)
            elif opcao == "Materiais":
                from view.tela_materiais import tela_materiais
                tela_materiais(root_anterior=modal)
            elif opcao == "Relatórios":
                from view.tela_servico import tela_execucao_servico
                tela_execucao_servico(root_anterior=modal)
        modal.after(100, _navegar)

    def make_handler(opcao):
        return lambda e: acao_menu(opcao)

    y_pos = 220
    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        ativo = (nome == "Cliente")
        cor_texto = cor_cinza if ativo else cor_branco

        img_item = canvas.create_image(20, y_pos, image=icone, anchor="nw")
        txt_item = canvas.create_text(50, y_pos + 12, text=nome, font=("Arial", 11, "bold"), fill=cor_texto, anchor="nw")

        def make_handler(opcao):
            return lambda e: acao_menu(opcao)

        def on_enter(e, txt=txt_item):
            canvas.itemconfig(txt, fill=cor_dourado)
        def on_leave(e, txt=txt_item, cor=cor_texto):
            canvas.itemconfig(txt, fill=cor)

        canvas.tag_bind(img_item, "<Enter>", on_enter)
        canvas.tag_bind(img_item, "<Leave>", on_leave)
        canvas.tag_bind(txt_item, "<Enter>", on_enter)
        canvas.tag_bind(txt_item, "<Leave>", on_leave)
        canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
        canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))

        canvas.image_refs = getattr(canvas, "image_refs", [])
        canvas.image_refs.append(icone)
        y_pos += 50

    # ---- FORMULÁRIO ----
    campos = ["nome_cliente", "email_cliente", "telefone_cliente", "cpf", "endereco", "data_nascimento"]
    labels = ["Nome", "E-mail", "Telefone", "CPF", "Endereço", "Data de Nasc."]
    entries = {}
    itens_form = []

    for i, (campo, label) in enumerate(zip(campos, labels)):
        lbl = canvas.create_text(0, 0, text=label, font=("Arial", 11, "bold"), fill="#ffffff", anchor="e")
        entry = ctk.CTkEntry(canvas, width=400, corner_radius=8, fg_color="#c2c7cc", text_color="#000000", border_color="#304C62", border_width=2)
        entry_win = canvas.create_window(0, 0, window=entry, anchor="w")
        if dados:
            entry.insert(0, dados[campo] if dados[campo] is not None else "")
        entries[campo] = entry
        itens_form.append((lbl, entry_win))

    def _abrir_lista_carros(id_cliente, nome_cliente):
        modal.destroy()
        listar_carros_cliente(id_cliente, nome_cliente)

    def salvar_e_avancar():
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
                    "UPDATE clientes SET nome_cliente=%s, email_cliente=%s, telefone_cliente=%s, cpf=%s, endereco=%s, data_nascimento=%s WHERE id_cliente=%s",
                    (valores["nome_cliente"], valores["email_cliente"], valores["telefone_cliente"], valores["cpf"], valores["endereco"], valores["data_nascimento"] if valores["data_nascimento"] else None, dados["id_cliente"])
                )
                id_cliente = dados["id_cliente"]
            else:
                cursor.execute(
                    "INSERT INTO clientes (nome_cliente, email_cliente, telefone_cliente, cpf, endereco, data_nascimento) VALUES (%s, %s, %s, %s, %s, %s)",
                    (valores["nome_cliente"], valores["email_cliente"], valores["telefone_cliente"], valores["cpf"], valores["endereco"], valores["data_nascimento"] if valores["data_nascimento"] else None)
                )
                id_cliente = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            id_salvo = id_cliente
            nome_salvo = valores["nome_cliente"]
            modal.after(100, lambda: _abrir_lista_carros(id_salvo, nome_salvo))
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    btn_salvar = ctk.CTkButton(canvas, text="Avançar", command=salvar_e_avancar, width=90, fg_color=cor_dourado, text_color=cor_branco, hover_color="#d4a857")
    btn_salvar_win = canvas.create_window(0, 0, window=btn_salvar, anchor="center")

    btn_cancelar = ctk.CTkButton(canvas, text="Cancelar", command=modal.destroy, width=90, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_cancelar_win = canvas.create_window(0, 0, window=btn_cancelar, anchor="center")

    def voltar_login_modal():
        modal.destroy()
        from main import tela_login
        tela_login()

    def ir_dashboard_form():
        from view.bemvindo import tela_dashboard
        modal.after(10, lambda: tela_dashboard(root_anterior=modal))

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login_modal, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    img_fundo = "assets/img_frame.png"
    img_original_form = None
    if os.path.exists(img_fundo):
        img_original_form = Image.open(img_fundo)

    def _redimensionar_formulario(event=None):
        if event is not None and event.widget != modal:
            return
        w, h = modal.winfo_width(), modal.winfo_height()
        if w < 10 or h < 10:
            return

        if img_original_form:
            img_resized = img_original_form.resize((w, h), Image.Resampling.LANCZOS)
            bg_form = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_form, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
            canvas.image_bg_form = bg_form

        form_w = min(500, w * 0.45)
        cx = w * 0.5 + 50
        cy_inicio = h * 0.15
        entry_w = int(form_w * 0.65)
        espacamento = max(45, min(60, h * 0.08))

        for i, (lbl, entry_win) in enumerate(itens_form):
            cy = cy_inicio + i * espacamento
            canvas.coords(lbl, cx - entry_w // 2 - 10, cy)
            canvas.coords(entry_win, cx + entry_w // 2, cy)
            canvas.itemconfig(entry_win, width=entry_w)

        y_btns = cy_inicio + len(campos) * espacamento + 20
        canvas.coords(btn_salvar_win, cx - 55, y_btns)
        canvas.coords(btn_cancelar_win, cx + 55, y_btns)
        canvas.coords(btn_sair_win, w * 0.02, h - 50)

        redimensionar_img_softcar(canvas, btn_dashboard_id_form, img_softcar_original_form, w, h)

    modal.bind("<Configure>", _redimensionar_formulario)
    modal.after(100, _redimensionar_formulario)

    def maximizar():
        modal.update_idletasks()
        modal.state("zoomed")
        try:
            modal.attributes('-zoomed', True)
        except:
            pass
    modal.after(100, maximizar)

    modal.mainloop()


def abrir_formulario_carro(id_cliente, nome_cliente, dados_carro=None, voltar_para_lista=False):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    modal = ctk.CTk()
    modal.title("Editar Carro" if dados_carro else "Cadastrar Carro")
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

    canvas = ctk.CTkCanvas(modal, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_softcar_original_carro = carregar_img_softcar()
    btn_dashboard_id_carro = None
    if img_softcar_original_carro:
        btn_dashboard_id_carro, img_softcar_tk_carro = criar_img_softcar(canvas, img_softcar_original_carro)
        canvas.tag_bind("dashboard_img", "<Button-1>", lambda e: ir_dashboard_carro())
        canvas.tag_bind("dashboard_img", "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind("dashboard_img", "<Leave>", lambda e: canvas.config(cursor=""))

    img_original = None
    if os.path.exists("assets/img_frame.png"):
        img_original = Image.open("assets/img_frame.png")

    # ---- MENU VERTICAL ----
    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def acao_menu_modal(opcao):
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

    def make_handler(opcao):
        return lambda e: acao_menu_modal(opcao)

    y_pos = 120
    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        if icone is None:
            icone = _criar_icone_fallback(24, cor_dourado, "circle")
        ativo = (nome == "Cliente")
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
        canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
        canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))

        canvas.image_refs = getattr(canvas, "image_refs", [])
        canvas.image_refs.append(icone)
        y_pos += 50

    # ---- FORMULÁRIO ----
    campos = ["placa", "modelo", "marca", "cor"]
    labels = ["Placa", "Modelo", "Marca", "Cor"]
    entries = {}
    itens_form = []

    for i, (campo, label) in enumerate(zip(campos, labels)):
        lbl = canvas.create_text(0, 0, text=label, font=("Arial", 11, "bold"), fill="#ffffff", anchor="e")
        entry = ctk.CTkEntry(canvas, width=400, corner_radius=8, fg_color="#c2c7cc", text_color="#000000", border_color="#304C62", border_width=2)
        entry_win = canvas.create_window(0, 0, window=entry, anchor="w")
        if dados_carro:
            entry.insert(0, dados_carro[campo] if dados_carro[campo] is not None else "")
        entries[campo] = entry
        itens_form.append((lbl, entry_win))

    def salvar_carro():
        valores = {}
        for campo in campos:
            if not entries[campo].get().strip():
                messagebox.showwarning("Validação", "Todos os campos são obrigatórios.")
                return
            valores[campo] = entries[campo].get().strip()
        try:
            conn = conectar()
            cursor = conn.cursor()
            if dados_carro:
                cursor.execute(
                    "UPDATE carros SET placa=%s, modelo=%s, marca=%s, cor=%s WHERE id_carro=%s",
                    (valores["placa"], valores["modelo"], valores["marca"], valores["cor"], dados_carro["id_carro"])
                )
            else:
                cursor.execute(
                    "INSERT INTO carros (placa, modelo, marca, cor) VALUES (%s, %s, %s, %s)",
                    (valores["placa"], valores["modelo"], valores["marca"], valores["cor"])
                )
                id_carro = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO clientes_has_carros (clientes_id_cliente, carros_id_carro) VALUES (%s, %s)",
                    (id_cliente, id_carro)
                )
            conn.commit()
            cursor.close()
            conn.close()
            modal.after(100, lambda: (modal.destroy(), messagebox.showinfo("Sucesso", "Carro salvo com sucesso!"), listar_carros_cliente(id_cliente, nome_cliente) if voltar_para_lista else None))
        except mysql.connector.IntegrityError:
            messagebox.showerror("Erro", "Placa já cadastrada.")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar carro:\n{e}")

    def avancar():
        modal.after(10, lambda: listar_servicos(id_cliente, nome_cliente, dados_carro, root_anterior=modal))

    def cancelar():
        modal.after(100, lambda: (modal.destroy(), voltar_para_lista and listar_carros_cliente(id_cliente, nome_cliente)))

    btn_salvar = ctk.CTkButton(canvas, text="Salvar", command=salvar_carro, width=90, fg_color=cor_dourado, text_color=cor_branco, hover_color="#d4a857")
    btn_salvar_win = canvas.create_window(0, 0, window=btn_salvar, anchor="center")
    btn_avancar = ctk.CTkButton(canvas, text="Avançar", command=avancar, width=90, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_avancar_win = canvas.create_window(0, 0, window=btn_avancar, anchor="center")
    btn_cancelar = ctk.CTkButton(canvas, text="Cancelar", command=cancelar, width=90, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_cancelar_win = canvas.create_window(0, 0, window=btn_cancelar, anchor="center")
    def voltar_login_modal():
        modal.destroy()
        from main import tela_login
        tela_login()

    def ir_dashboard_carro():
        from view.bemvindo import tela_dashboard
        modal.after(10, lambda: tela_dashboard(root_anterior=modal))

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login_modal, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    def _redimensionar_formulario(event=None):
        if event is not None and event.widget != modal:
            return
        w, h = modal.winfo_width(), modal.winfo_height()
        if w < 10 or h < 10:
            return

        if img_original:
            img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_form = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_form, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
            canvas.image_bg_form = bg_form

        form_w = min(500, w * 0.45)
        cx = w * 0.5
        cy_inicio = h * 0.15
        entry_w = int(form_w * 0.65)
        espacamento = max(45, min(60, h * 0.08))

        for i, (lbl, entry_win) in enumerate(itens_form):
            cy = cy_inicio + i * espacamento
            canvas.coords(lbl, cx - entry_w // 2 - 10, cy)
            canvas.coords(entry_win, cx + entry_w // 2, cy)
            canvas.itemconfig(entry_win, width=entry_w)

        y_btns = cy_inicio + len(campos) * espacamento + 30
        canvas.coords(btn_salvar_win, cx - 165, y_btns)
        canvas.coords(btn_avancar_win, cx - 55, y_btns)
        canvas.coords(btn_cancelar_win, cx + 55, y_btns)
        canvas.coords(btn_sair_win, w * 0.02, h - 50)

        redimensionar_img_softcar(canvas, btn_dashboard_id_carro, img_softcar_original_carro, w, h)

    modal.bind("<Configure>", _redimensionar_formulario)
    modal.after(100, _redimensionar_formulario)

    def maximizar():
        modal.update_idletasks()
        modal.state("zoomed")
        try:
            modal.attributes('-zoomed', True)
        except:
            pass
    modal.after(100, maximizar)

    modal.mainloop()


def listar_carros_cliente(id_cliente, nome_cliente):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    modal = ctk.CTk()
    modal.title("Carros do Cliente")
    modal.state("zoomed")
    modal.minsize(800, 500)
    modal.resizable(True, True)
    try:
        modal.attributes('-zoomed', True)
    except:
        pass

    canvas = ctk.CTkCanvas(modal, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_softcar_original_carros = carregar_img_softcar()
    btn_dashboard_id_carros = None
    if img_softcar_original_carros:
        btn_dashboard_id_carros, img_softcar_tk_carros = criar_img_softcar(canvas, img_softcar_original_carros)
        canvas.tag_bind("dashboard_img", "<Button-1>", lambda e: ir_dashboard_carros())
        canvas.tag_bind("dashboard_img", "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind("dashboard_img", "<Leave>", lambda e: canvas.config(cursor=""))

    img_original = None
    if os.path.exists("assets/img_frame.png"):
        img_original = Image.open("assets/img_frame.png")

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_cinza = "#777777"

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def acao_menu_modal(opcao):
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
            else:
                messagebox.showinfo("Soft Car", "Em desenvolvimento")
        modal.after(100, _navegar)

    menu_items = []
    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        if icone is None:
            icone = _criar_icone_fallback(24, cor_dourado, "circle")
        ativo = (nome == "Cliente")
        cor_texto = cor_cinza if ativo else cor_branco
        img_item = canvas.create_image(0, 0, image=icone, anchor="nw")
        txt_item = canvas.create_text(0, 0, text=nome, font=("Arial", 11, "bold"), fill=cor_texto, anchor="nw")
        def on_enter(e, t=txt_item):
            canvas.itemconfig(t, fill=cor_dourado)
        def on_leave(e, t=txt_item, c=cor_texto):
            canvas.itemconfig(t, fill=c)
        canvas.tag_bind(img_item, "<Enter>", on_enter)
        canvas.tag_bind(img_item, "<Leave>", on_leave)
        canvas.tag_bind(txt_item, "<Enter>", on_enter)
        canvas.tag_bind(txt_item, "<Leave>", on_leave)
        canvas.tag_bind(img_item, "<Button-1>", lambda e, o=nome: acao_menu_modal(o))
        canvas.tag_bind(txt_item, "<Button-1>", lambda e, o=nome: acao_menu_modal(o))
        canvas.image_refs = getattr(canvas, "image_refs", [])
        canvas.image_refs.append(icone)
        menu_items.append((img_item, txt_item))

    lbl_cliente = canvas.create_text(0, 0, text=f"Cliente: {nome_cliente}", font=("Arial", 14, "bold"), fill="#ffffff", anchor="nw")

    btn_novo = ctk.CTkButton(canvas, text="+ Novo Carro", command=lambda: modal.after(100, lambda: (modal.destroy(), abrir_formulario_carro(id_cliente, nome_cliente, voltar_para_lista=True))), fg_color=cor_dourado, text_color=cor_branco, hover_color="#d4a857")
    btn_novo_win = canvas.create_window(0, 0, window=btn_novo, anchor="nw")

    frame = ctk.CTkFrame(canvas, fg_color="#2b3e50", corner_radius=8)
    frame_win = canvas.create_window(0, 0, window=frame, anchor="nw")

    colunas = ("id_carro", "placa", "modelo", "marca", "cor")
    tree_carros = ttk.Treeview(frame, columns=colunas, show="headings", height=14)

    tree_carros.heading("id_carro", text="Código")
    tree_carros.heading("placa", text="Placa")
    tree_carros.heading("modelo", text="Modelo")
    tree_carros.heading("marca", text="Marca")
    tree_carros.heading("cor", text="Cor")

    tree_carros.column("id_carro", width=60, anchor="center")
    tree_carros.column("placa", width=100, anchor="center")
    tree_carros.column("modelo", width=200)
    tree_carros.column("marca", width=150)
    tree_carros.column("cor", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree_carros.yview)
    tree_carros.configure(yscrollcommand=scrollbar.set)

    tree_carros.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#375269", foreground="#ffffff", fieldbackground="#375269", rowheight=28, borderwidth=0, bordercolor="#375269")
    style.configure("Treeview.Heading", background="#2c4a5c", foreground="#ffffff", borderwidth=0, bordercolor="#2c4a5c")
    style.layout("Treeview", [("Treeview.field", {"sticky": "nswe", "children": [("Treeview.padding", {"sticky": "nswe", "children": [("Treeview.treearea", {"sticky": "nswe"})]})]})])

    def editar_carro_tree():
        selecionado = tree_carros.selection()
        if not selecionado:
            return
        valores = tree_carros.item(selecionado[0])["values"]
        dados_carro = {"id_carro": valores[0], "placa": valores[1], "modelo": valores[2], "marca": valores[3], "cor": valores[4]}
        modal.after(100, lambda: (modal.destroy(), abrir_formulario_carro(id_cliente, nome_cliente, dados_carro, voltar_para_lista=True)))

    tree_carros.bind("<Double-1>", lambda e: editar_carro_tree())

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_carro, c.placa, c.modelo, c.marca, c.cor
            FROM carros c
            INNER JOIN clientes_has_carros chc ON chc.carros_id_carro = c.id_carro
            WHERE chc.clientes_id_cliente = %s
        """, (id_cliente,))
        for row in cursor.fetchall():
            tree_carros.insert("", "end", values=row)
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar carros:\n{e}")

    btn_fechar = ctk.CTkButton(canvas, text="Fechar", command=modal.destroy, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_fechar_win = canvas.create_window(0, 0, window=btn_fechar, anchor="nw")

    def voltar_login_modal():
        modal.destroy()
        from main import tela_login
        tela_login()

    def ir_dashboard_carros():
        from view.bemvindo import tela_dashboard
        modal.after(10, lambda: tela_dashboard(root_anterior=modal))

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login_modal, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    def _redimensionar(event=None):
        w, h = modal.winfo_width(), modal.winfo_height()
        if w < 10 or h < 10:
            return

        if img_original:
            img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_img = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_img, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
            canvas.image_bg = bg_img

        y = 220
        for img_item, txt_item in menu_items:
            canvas.coords(img_item, 20, y)
            canvas.coords(txt_item, 50, y + 12)
            y += 50

        cx = w * 0.191
        cy = h * 0.05
        cw = w * 0.753
        ch = h * 0.80

        canvas.coords(lbl_cliente, cx + 4, cy)
        canvas.coords(btn_novo_win, cx + cw - 120, cy)
        canvas.coords(frame_win, cx + 4, cy + 40)
        canvas.itemconfig(frame_win, width=max(100, cw - 4), height=max(100, ch - 50))

        canvas.coords(btn_fechar_win, cx + 4, cy + ch + 10)
        canvas.coords(btn_sair_win, w * 0.02, h - 50)

        redimensionar_img_softcar(canvas, btn_dashboard_id_carros, img_softcar_original_carros, w, h)

    modal.bind("<Configure>", _redimensionar)
    modal.after(100, lambda: [modal.update_idletasks(), _redimensionar()])

    def maximizar():
        modal.update_idletasks()
        modal.state("zoomed")
        try:
            modal.attributes('-zoomed', True)
        except:
            pass
    modal.after(100, maximizar)

    modal.mainloop()


def listar_servicos(id_cliente, nome_cliente, dados_carro, root_anterior=None):
    if root_anterior:
        root_anterior.destroy()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    modal = ctk.CTk()
    modal.title("Serviços Disponíveis")
    modal.state("zoomed")
    modal.minsize(800, 500)
    modal.resizable(True, True)
    try:
        modal.attributes('-zoomed', True)
    except:
        pass

    canvas = ctk.CTkCanvas(modal, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_softcar_original_serv = carregar_img_softcar()
    btn_dashboard_id_serv = None
    if img_softcar_original_serv:
        btn_dashboard_id_serv, img_softcar_tk_serv = criar_img_softcar(canvas, img_softcar_original_serv)
        canvas.tag_bind("dashboard_img", "<Button-1>", lambda e: ir_dashboard_serv())
        canvas.tag_bind("dashboard_img", "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind("dashboard_img", "<Leave>", lambda e: canvas.config(cursor=""))

    img_original = None
    if os.path.exists("assets/img_frame.png"):
        img_original = Image.open("assets/img_frame.png")

    bg_image_tk = None

    menu_items = []
    img_refs = []

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        if icone is None:
            icone = _criar_icone_fallback(24, "#b88b4a", "circle")
        img_refs.append(icone)

    y_pos = 220
    for nome, icone in zip(icones_info, img_refs):
        nome_texto = nome[0]
        ativo = (nome_texto == "Serviços")
        cor_texto = "#777777" if ativo else "#ffffff"
        img_item = canvas.create_image(20, y_pos, image=icone, anchor="nw")
        txt_item = canvas.create_text(50, y_pos + 12, text=nome_texto, font=("Arial", 11, "bold"), fill=cor_texto, anchor="nw")

        def on_enter(e, t=txt_item):
            canvas.itemconfig(t, fill="#b88b4a")
        def on_leave(e, t=txt_item, c=cor_texto):
            canvas.itemconfig(t, fill=cor_texto)

        canvas.tag_bind(img_item, "<Enter>", on_enter)
        canvas.tag_bind(img_item, "<Leave>", on_leave)
        canvas.tag_bind(txt_item, "<Enter>", on_enter)
        canvas.tag_bind(txt_item, "<Leave>", on_leave)

        def make_handler(opcao):
            def _navegar():
                if opcao == "Cliente":
                    tela_clientes(root_anterior=modal)
                elif opcao == "Serviços":
                    pass
                elif opcao == "Funcionários":
                    from view.lista_funcionarios import tela_lista_funcionarios
                    tela_lista_funcionarios(root_anterior=modal)
                elif opcao == "Materiais":
                    from view.tela_materiais import tela_materiais
                    tela_materiais(root_anterior=modal)
                elif opcao == "Relatórios":
                    from view.tela_servico import tela_execucao_servico
                    tela_execucao_servico(root_anterior=modal)
            return _navegar

        canvas.tag_bind(img_item, "<Button-1>", make_handler(nome_texto))
        canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome_texto))
        menu_items.append((img_item, txt_item))
        y_pos += 50

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_cinza = "#777777"

    titulo_lbl = ctk.CTkLabel(canvas, text=f"Cliente: {nome_cliente}  |  Carro: {dados_carro['placa'] if dados_carro else 'Novo carro'}", font=("Arial", 12, "bold"), text_color="#ffffff")
    titulo_win = canvas.create_window(180, 20, window=titulo_lbl, anchor="nw")

    total_label = ctk.CTkLabel(canvas, text="Total: R$ 0.00", font=("Arial", 14, "bold"), text_color="#b88b4a")
    total_win = canvas.create_window(0, 0, window=total_label, anchor="nw")

    frame = ctk.CTkFrame(canvas, fg_color="#2b3e50", corner_radius=8)
    frame_win = canvas.create_window(180, 60, window=frame, anchor="nw")

    colunas = ("check", "id_servico", "nome_servico", "preco_servico")
    tree_servicos = ttk.Treeview(frame, columns=colunas, show="headings", height=12)
    tree_servicos.heading("check", text="✓")
    tree_servicos.heading("id_servico", text="Código")
    tree_servicos.heading("nome_servico", text="Serviço")
    tree_servicos.heading("preco_servico", text="Preço")
    tree_servicos.column("check", width=40, stretch=False, anchor="center")
    tree_servicos.column("id_servico", width=60, stretch=False, anchor="center")
    tree_servicos.column("nome_servico", width=370, stretch=True)
    tree_servicos.column("preco_servico", width=90, stretch=True, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree_servicos.yview)
    tree_servicos.configure(yscrollcommand=scrollbar.set)
    tree_servicos.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#375269", foreground="#ffffff", fieldbackground="#375269", rowheight=28, borderwidth=0, bordercolor="#375269")
    style.configure("Treeview.Heading", background="#2c4a5c", foreground="#ffffff", borderwidth=0, bordercolor="#2c4a5c")
    style.layout("Treeview", [("Treeview.field", {"sticky": "nswe", "children": [("Treeview.padding", {"sticky": "nswe", "children": [("Treeview.treearea", {"sticky": "nswe"})]})]})])

    servicos_checks = {}
    servicos_precos = {}

    def atualizar_total():
        total = sum(servicos_precos[i] for i, checked in servicos_checks.items() if checked)
        total_label.configure(text=f"Total: R$ {total:.2f}")

    def toggle_check(event):
        item = tree_servicos.identify_row(event.y)
        if item:
            valores = tree_servicos.item(item, "values")
            checked = valores[0] == "☑"
            novo = "☐" if checked else "☑"
            tree_servicos.item(item, values=(novo, valores[1], valores[2], valores[3]))
            id_serv = int(valores[1])
            servicos_checks[id_serv] = not checked
            atualizar_total()

    tree_servicos.bind("<ButtonRelease-1>", toggle_check)

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_servico, nome_servico, preco_servico FROM servicos ORDER BY nome_servico")
        for id_servico, nome_servico, preco in cursor.fetchall():
            preco_str = f"R$ {preco:.2f}" if preco else "-"
            tree_servicos.insert("", "end", values=("☐", id_servico, nome_servico, preco_str))
            servicos_checks[id_servico] = False
            servicos_precos[id_servico] = float(preco) if preco else 0.0
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar serviços:\n{e}")

    def salvar_ordem():
        selecionados = [i for i, checked in servicos_checks.items() if checked]
        if not selecionados:
            messagebox.showwarning("Seleção", "Selecione pelo menos um serviço.")
            return
        total = sum(servicos_precos[i] for i in selecionados)
        id_carro = dados_carro["id_carro"] if dados_carro else None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ordem_servico (id_cliente, id_carro, total) VALUES (%s, %s, %s)",
                (id_cliente, id_carro, total)
            )
            id_ordem = cursor.lastrowid
            for id_servico in selecionados:
                cursor.execute(
                    "INSERT INTO ordem_servico_itens (id_ordem, id_servico, preco) VALUES (%s, %s, %s)",
                    (id_ordem, id_servico, servicos_precos[id_servico])
                )
            conn.commit()
            cursor.close()
            conn.close()
            def _abrir_dashboard():
                modal.destroy()
                from view.bemvindo import tela_dashboard
                tela_dashboard()
            modal.after(100, lambda: (messagebox.showinfo("Sucesso", f"Ordem de serviço #{id_ordem} criada! Total: R$ {total:.2f}"), _abrir_dashboard()))
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar ordem:\n{e}")

    btn_salvar = ctk.CTkButton(canvas, text="Salvar Ordem", command=salvar_ordem, width=100, fg_color=cor_dourado, text_color=cor_branco, hover_color="#d4a857")
    btn_voltar = ctk.CTkButton(canvas, text="Voltar", command=lambda: modal.after(100, lambda: (modal.destroy(), abrir_formulario_carro(id_cliente, nome_cliente, dados_carro, voltar_para_lista=True))), width=80, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_fechar = ctk.CTkButton(canvas, text="Fechar", command=modal.destroy, width=80, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")

    def voltar_login_modal():
        modal.destroy()
        from main import tela_login
        tela_login()

    def ir_dashboard_serv():
        from view.bemvindo import tela_dashboard
        modal.after(10, lambda: tela_dashboard(root_anterior=modal))

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login_modal, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")

    btn_salvar_win = canvas.create_window(0, 0, window=btn_salvar, anchor="nw")
    btn_voltar_win = canvas.create_window(0, 0, window=btn_voltar, anchor="nw")
    btn_fechar_win = canvas.create_window(0, 0, window=btn_fechar, anchor="nw")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    def _redim(event=None):
        w = modal.winfo_width()
        h = modal.winfo_height()
        if w < 10 or h < 10:
            return

        if img_original:
            img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_img = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_img, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
            canvas.image_bg = bg_img

        y = 220
        for img_item, txt_item in menu_items:
            canvas.coords(img_item, 20, y)
            canvas.coords(txt_item, 50, y + 12)
            y += 50

        cx = w * 0.191
        cy = h * 0.178
        cw = w * 0.753
        ch = h * 0.750

        canvas.coords(titulo_win, cx + 30, cy - 55)
        canvas.coords(total_win, cx + cw - 150, cy - 55)
        canvas.coords(frame_win, cx + 4, cy + 20)
        canvas.itemconfig(frame_win, width=max(100, cw - 4), height=max(100, ch - 42))

        btn_y = cy + ch + 10
        canvas.coords(btn_salvar_win, cx, btn_y)
        canvas.coords(btn_voltar_win, cx + 110, btn_y)
        canvas.coords(btn_fechar_win, cx + 200, btn_y)
        canvas.coords(btn_sair_win, w * 0.02, h - 50)
        tree_servicos.column("nome_servico", width=int(col_w * 0.60))
        tree_servicos.column("preco_servico", width=int(col_w * 0.40))

        redimensionar_img_softcar(canvas, btn_dashboard_id_serv, img_softcar_original_serv, w, h)

    modal.bind("<Configure>", _redim)
    modal.after(100, lambda: [modal.update_idletasks(), _redim()])

    def maximizar():
        modal.update_idletasks()
        modal.state("zoomed")
        try:
            modal.attributes('-zoomed', True)
        except:
            pass
        modal.update_idletasks()
        _redim()
    modal.after(200, maximizar)

    modal.mainloop()


def excluir_cliente(tree):
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um cliente na lista.")
        return
    if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este cliente?"):
        return
    id_cliente = tree.item(selecionado[0])["values"][0]
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        cursor.close()
        conn.close()
        carregar_clientes(tree)
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

def tela_clientes(root_anterior=None):
    if root_anterior:
        root_anterior.destroy()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.title("Soft Car - Lista de Clientes")
    root.state("zoomed")
    root.minsize(800, 500)
    root.resizable(True, True)

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_cinza = "#777777"
    cor_fundo = "#2b3e50"

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def navegar(opcao):
        if opcao == "Cliente":
            return
        def _navegar():
            if opcao == "Serviços":
                from view.tela_servicos import tela_servicos
                tela_servicos(root_anterior=root)
            elif opcao == "Funcionários":
                from view.lista_funcionarios import tela_lista_funcionarios
                tela_lista_funcionarios(root_anterior=root)
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
                    bordercolor="#375269",
                    relief="flat",
                    lightcolor="#375269",
                    darkcolor="#375269",
                    arrowcolor="#375269")

    frame_top = ctk.CTkFrame(canvas, fg_color="#375269", corner_radius=0)
    frame_top_window = canvas.create_window(0, 0, window=frame_top, anchor="nw")

    ctk.CTkLabel(frame_top, text="Pesquisar", font=("Arial", 11, "bold"), text_color=cor_branco).pack(side="left", padx=5)
    search_var = tk.StringVar()
    entry_busca = ctk.CTkEntry(frame_top, width=200, fg_color="#375269", text_color="#ffffff", border_width=1, font=("Arial", 10))
    entry_busca.pack(side="left", padx=5, ipady=3)
    search_var.trace_add("write", lambda *args: buscar_clientes(tree, entry_busca))

    btn_cadastrar_img_original = Image.open("assets/btn_cliente.png") if os.path.exists("assets/btn_cliente.png") else None
    btn_cadastrar_img = None
    if btn_cadastrar_img_original:
        btn_w = int(65 * root.winfo_width() / 800) if root.winfo_width() > 0 else 65
        btn_h = int(25 * root.winfo_height() / 600) if root.winfo_height() > 0 else 25
        btn_cadastrar_img_resized = btn_cadastrar_img_original.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
        btn_cadastrar_img = ImageTk.PhotoImage(btn_cadastrar_img_resized)
    btn_cadastrar_window = canvas.create_image(0, 0, image=btn_cadastrar_img, anchor="nw")
    canvas.img_refs = getattr(canvas, "img_refs", [])
    canvas.img_refs.append(btn_cadastrar_img)
    canvas.tag_bind(btn_cadastrar_window, "<Button-1>", lambda e: abrir_formulario(tree))
    canvas.tag_bind(btn_cadastrar_window, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(btn_cadastrar_window, "<Leave>", lambda e: canvas.config(cursor=""))

    def cmd_editar():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um cliente na lista.")
            return
        id_cliente = tree.item(selecionado[0])["values"][0]
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
            dados = cursor.fetchone()
            cursor.close()
            conn.close()
            if dados:
                abrir_formulario(tree, dados)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")

    def cmd_excluir():
        excluir_cliente(tree)

    frame_tabela = ctk.CTkFrame(canvas, fg_color="transparent", corner_radius=8, border_width=0)
    frame_tabela_window = canvas.create_window(0, 0, window=frame_tabela, anchor="nw")

    colunas = ("id_cliente", "nome_cliente", "email_cliente", "telefone_cliente", "cpf", "endereco")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse", height=15)
    tree.heading("id_cliente", text="ID")
    tree.heading("nome_cliente", text="Nome")
    tree.heading("email_cliente", text="E-mail")
    tree.heading("telefone_cliente", text="Telefone")
    tree.heading("cpf", text="CPF")
    tree.heading("endereco", text="Endereço")
    tree.column("id_cliente", width=0, stretch=False)
    tree.column("nome_cliente", width=180)
    tree.column("email_cliente", width=200)
    tree.column("telefone_cliente", width=120, anchor="center")
    tree.column("cpf", width=130, anchor="center")
    tree.column("endereco", width=170)

    tree.tag_configure("odd", background="#375269")
    tree.tag_configure("even", background="#375269")

    tree.bind("<Double-1>", lambda e: cmd_editar())

    style.configure("Vertical.TScrollbar", gripcount=0, background="white", troughcolor="#2c4a5c", bordercolor="#2c4a5c", arrowcolor="#000000")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")

    def _atualizar_scrollbar(*args):
        scrollbar.set(*args)

    tree.configure(yscrollcommand=_atualizar_scrollbar)

    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    carregar_clientes(tree)

    def voltar_login():
        root.destroy()
        from main import tela_login
        tela_login()

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    def _redimensionar(w, h):
        nonlocal bg_image_tk, menu_criado

        if img_original:
            img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_image_tk = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
            if btn_dashboard_id:
                canvas.tag_raise(btn_dashboard_id)

        if not menu_criado:
            y_pos = 220
            for nome, arquivo in icones_info:
                icone = _carregar_icone(arquivo, 24)
                if icone is None:
                    icone = _criar_icone_fallback(24, cor_dourado, "circle")

                ativo = (nome == "Cliente")
                cor_texto = cor_cinza if ativo else cor_branco
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
                canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
                canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))

                canvas.image_refs.append(icone)
                botoes_menu.append((img_item, txt_item))
                y_pos += 50
            menu_criado = True

        y = 220
        for img_item, txt_item in botoes_menu:
            canvas.coords(img_item, 20, y)
            canvas.coords(txt_item, 50, y + 12)
            y += 50

        redimensionar_img_softcar(canvas, btn_dashboard_id, img_softcar_original, w, h)

        cx = w * 0.191
        cy = h * 0.178
        cw = w * 0.753
        ch = h * 0.750

        canvas.coords(frame_top_window, cx + 30, cy - 145)
        canvas.coords(btn_cadastrar_window, cx + cw - 260, cy - 145)
        if btn_cadastrar_img_original:
            btn_w = int(65 * w / 800)
            btn_h = int(25 * h / 600)
            btn_img_resized = btn_cadastrar_img_original.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
            btn_cadastrar_img = ImageTk.PhotoImage(btn_img_resized)
            canvas.itemconfig(btn_cadastrar_window, image=btn_cadastrar_img)
            canvas.img_refs = getattr(canvas, "img_refs", [])
            canvas.img_refs.append(btn_cadastrar_img)
        canvas.coords(frame_tabela_window, cx + 176, cy - 42)
        canvas.itemconfig(frame_tabela_window, width=max(100, cw - 254), height=max(100, ch - 22))
        canvas.coords(btn_sair_win, w * 0.02, h - 50)

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

    root.mainloop()


if __name__ == "__main__":
    tela_clientes()
