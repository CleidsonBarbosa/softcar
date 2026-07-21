import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
import customtkinter as ctk

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
    modal = ctk.CTkToplevel()
    modal.title("Editar Cliente" if dados else "Novo Cliente")
    modal.geometry("1000x600")
    modal.minsize(800, 500)
    modal.resizable(False, False)
    modal.grab_set()

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_cinza = "#777777"

    # Imagem de fundo: editar_clientes.png para edição, cadastrar_clientes.png para cadastro
    img_fundo = "assets/editar_clientes.png" if dados else "assets/cadastrar_clientes.png"

    canvas = tk.Canvas(modal, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    bg_img = None
    if os.path.exists(img_fundo):
        img = Image.open(img_fundo)
        img = img.resize((1000, 600), Image.Resampling.LANCZOS)
        bg_img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=bg_img, anchor="nw")
        canvas.image = bg_img

    # ---- MENU VERTICAL ----
    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def acao_menu(opcao):
        modal.destroy()
        if opcao == "Cliente":
            from view.tela_clientes import tela_clientes
            tela_clientes()
        elif opcao == "Serviços":
            messagebox.showinfo("Soft Car", "Em desenvolvimento")
        elif opcao == "Funcionários":
            from view.lista_funcionarios import tela_lista_funcionarios
            tela_lista_funcionarios()
        elif opcao == "Materiais":
            messagebox.showinfo("Soft Car", "Em desenvolvimento")
        elif opcao == "Relatórios":
            messagebox.showinfo("Soft Car", "Em desenvolvimento")

    def make_handler(opcao):
        return lambda e: acao_menu(opcao)

    y_pos = 120
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

        canvas.image_refs = getattr(canvas, "image_refs", [])
        canvas.image_refs.append(icone)
        y_pos += 50

    # ---- FORMULÁRIO ----
    frame = ctk.CTkFrame(canvas, fg_color="#2b3e50", corner_radius=15)
    frame_window = canvas.create_window(500, 300, window=frame, anchor="center")

    campos = ["nome_cliente", "email_cliente", "telefone_cliente", "cpf", "endereco", "data_nascimento"]
    labels = ["Nome", "E-mail", "Telefone", "CPF", "Endereço", "Data de Nascimento"]
    entries = {}

    for i, (campo, label) in enumerate(zip(campos, labels)):
        ctk.CTkLabel(frame, text=label, font=("Arial", 11, "bold"), text_color="#ffffff").grid(row=i, column=0, sticky="w", pady=4, padx=10)
        entry = ctk.CTkEntry(frame, width=250, corner_radius=8)
        entry.grid(row=i, column=1, pady=4, padx=10)
        if dados:
            entry.insert(0, dados[campo] if dados[campo] is not None else "")
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
                    "UPDATE clientes SET nome_cliente=%s, email_cliente=%s, telefone_cliente=%s, cpf=%s, endereco=%s, data_nascimento=%s WHERE id_cliente=%s",
                    (valores["nome_cliente"], valores["email_cliente"], valores["telefone_cliente"], valores["cpf"], valores["endereco"], valores["data_nascimento"] if valores["data_nascimento"] else None, dados["id_cliente"])
                )
            else:
                cursor.execute(
                    "INSERT INTO clientes (nome_cliente, email_cliente, telefone_cliente, cpf, endereco, data_nascimento) VALUES (%s, %s, %s, %s, %s, %s)",
                    (valores["nome_cliente"], valores["email_cliente"], valores["telefone_cliente"], valores["cpf"], valores["endereco"], valores["data_nascimento"] if valores["data_nascimento"] else None)
                )
            conn.commit()
            cursor.close()
            conn.close()
            modal.destroy()
            carregar_clientes(tree)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
    ctk.CTkButton(btn_frame, text="Salvar", command=salvar, width=90).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Cancelar", command=modal.destroy, width=90).pack(side="left", padx=5)


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


def tela_clientes():
    janela = tk.Toplevel()
    janela.title("Soft Car - Lista de Clientes")
    janela.geometry("1000x600")
    janela.minsize(800, 500)

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

    def acao_menu(opcao):
        if opcao == "Funcionários":
            from view.lista_funcionarios import tela_lista_funcionarios
            tela_lista_funcionarios()
        elif opcao == "Cliente":
            pass
        else:
            messagebox.showinfo("Soft Car", f"Você clicou na opção: {opcao}")

    canvas = tk.Canvas(janela, highlightthickness=0, bg=cor_fundo)
    canvas.pack(fill="both", expand=True)

    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "listar_funcionarios.png")
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
                    lightcolor="#375269",
                    darkcolor="#375269",
                    troughcolor="#375269")
    style.configure("Treeview.Heading",
                    background="#2c4a5c",
                    foreground=cor_branco,
                    relief="flat",
                    borderwidth=0,
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

    frame_top = tk.Frame(canvas, bg="#375269")
    frame_top_window = canvas.create_window(0, 0, window=frame_top, anchor="nw")

    tk.Label(frame_top, text="Pesquisar", font=("Arial", 11, "bold"), fg=cor_branco, bg="#375269").pack(side="left", padx=5)
    search_var = tk.StringVar()
    entry_busca = tk.Entry(frame_top, width=20, bg="#375269", fg="#ffffff", insertbackground="#ffffff", textvariable=search_var, relief="flat", font=("Arial", 10))
    entry_busca.pack(side="left", padx=5, ipady=3)
    search_var.trace_add("write", lambda *args: buscar_clientes(tree, entry_busca))

    btn_cadastrar = tk.Button(canvas, text="Cadastrar Cliente +", font=("Arial", 11, "bold"),
                              bg="#375269", fg=cor_branco, activebackground=cor_dourado,
                              activeforeground=cor_branco, relief="flat", bd=0,
                              command=lambda: abrir_formulario(tree))
    btn_cadastrar_window = canvas.create_window(0, 0, window=btn_cadastrar, anchor="nw")

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

    frame_tabela = tk.Frame(canvas, bg="#375269")
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

        canvas.coords(frame_top_window, cx + 30, cy - 55)
        canvas.coords(btn_cadastrar_window, cx + cw - 190, cy - 55)
        canvas.coords(frame_tabela_window, cx + 4, cy + 20)
        canvas.itemconfig(frame_tabela_window, width=max(100, cw - 4), height=max(100, ch - 42))

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
    tela_clientes()
    root.mainloop()
