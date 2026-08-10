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


def carregar_materiais(tree):
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, tipo, quantidade FROM estoque ORDER BY tipo")
        for i, row in enumerate(cursor.fetchall()):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao carregar materiais:\n{e}")


def buscar_materiais(tree, entry_busca):
    termo = entry_busca.get().strip()
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        if termo:
            cursor.execute(
                "SELECT id_produto, tipo, quantidade FROM estoque WHERE tipo LIKE %s ORDER BY tipo",
                (f"%{termo}%",)
            )
        else:
            cursor.execute("SELECT id_produto, tipo, quantidade FROM estoque ORDER BY tipo")
        for i, row in enumerate(cursor.fetchall()):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")


def abrir_formulario_material(tree, dados=None):
    modal = tk.Toplevel()
    modal.title("Editar Material" if dados else "Novo Material")
    modal.geometry("1000x600")
    modal.minsize(800, 500)
    modal.resizable(False, False)
    modal.transient(tree.winfo_toplevel())
    modal.grab_set()

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_cinza = "#777777"

    img_fundo = "assets/formulario.png"

    canvas = tk.Canvas(modal, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    bg_img = None
    if os.path.exists(img_fundo):
        img = Image.open(img_fundo)
        img = img.resize((1000, 600), Image.Resampling.LANCZOS)
        bg_img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=bg_img, anchor="nw")
        canvas.image = bg_img

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def acao_menu(opcao):
        root_principal = tree.winfo_toplevel()
        modal.destroy()
        root_principal.destroy()
        if opcao == "Cliente":
            from view.tela_clientes import tela_clientes
            tela_clientes(root_anterior=root_principal)
        elif opcao == "Serviços":
            from view.tela_servicos import tela_servicos
            tela_servicos(root_anterior=root_principal)
        elif opcao == "Funcionários":
            from view.lista_funcionarios import tela_lista_funcionarios
            tela_lista_funcionarios(root_anterior=root_principal)
        elif opcao == "Materiais":
            from view.tela_materiais import tela_materiais
            tela_materiais(root_anterior=root_principal)
        elif opcao == "Relatórios":
            from view.tela_servico import tela_execucao_servico
            tela_execucao_servico(root_anterior=root_principal)

    y_pos = 120
    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        ativo = (nome == "Materiais")
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

    campos = ["tipo", "quantidade"]
    labels = ["Tipo", "Quantidade"]
    entries = {}
    itens_form = []

    x_label = 400
    x_entry = 420
    y_inicio = 220

    for i, (campo, label) in enumerate(zip(campos, labels)):
        y_atual = y_inicio + i * 60
        lbl = canvas.create_text(x_label, y_atual, text=label, font=("Arial", 11, "bold"), fill="#ffffff", anchor="e")
        entry = tk.Entry(canvas, width=35, bg="#c2c7cc", fg="#000000", insertbackground="#000000", relief="flat", font=("Arial", 12))
        entry_win = canvas.create_window(x_entry, y_atual, window=entry, anchor="w")
        if dados:
            entry.insert(0, dados[campo] if dados[campo] is not None else "")
        entries[campo] = entry
        itens_form.append((lbl, entry_win))

    def salvar():
        for campo, label in zip(campos, labels):
            if not entries[campo].get().strip():
                messagebox.showwarning("Validação", f"O campo {label} é obrigatório.")
                return
        tipo = entries["tipo"].get().strip()
        quantidade = entries["quantidade"].get().strip()
        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showwarning("Validação", "Quantidade deve ser um número inteiro.")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            if dados:
                cursor.execute(
                    "UPDATE estoque SET tipo=%s, quantidade=%s WHERE id_produto=%s",
                    (tipo, quantidade, dados["id_produto"])
                )
            else:
                cursor.execute(
                    "INSERT INTO estoque (tipo, quantidade) VALUES (%s, %s)",
                    (tipo, quantidade)
                )
            conn.commit()
            cursor.close()
            conn.close()
            modal.destroy()
            carregar_materiais(tree)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    def voltar():
        modal.destroy()
        carregar_materiais(tree)

    btn_salvar = tk.Button(canvas, text="Salvar", command=salvar, width=12,
                           bg="#b88b4a", fg="#ffffff", activebackground="#d4a857",
                           relief="flat", font=("Arial", 11, "bold"))
    canvas.create_window(x_entry + 420, y_inicio + 120, window=btn_salvar, anchor="center")

    btn_cancelar = tk.Button(canvas, text="Cancelar", command=voltar, width=12,
                             bg="#375269", fg="#ffffff", activebackground="#b88b4a",
                             relief="flat", font=("Arial", 11, "bold"))
    canvas.create_window(x_entry + 420, y_inicio + 170, window=btn_cancelar, anchor="center")


def excluir_material(tree):
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um material na lista.")
        return
    if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este material?"):
        return
    id_produto = tree.item(selecionado[0])["values"][0]
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estoque WHERE id_produto = %s", (id_produto,))
        conn.commit()
        cursor.close()
        conn.close()
        carregar_materiais(tree)
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


def tela_materiais(root_anterior=None):
    if root_anterior:
        root_anterior.destroy()
    root = tk.Tk()
    root.title("Soft Car - Lista de Materiais")
    root.state("zoomed")
    root.minsize(800, 500)
    root.resizable(True, True)

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
        if opcao == "Materiais":
            return
        root.destroy()
        if opcao == "Cliente":
            from view.tela_clientes import tela_clientes
            tela_clientes(root_anterior=root)
        elif opcao == "Serviços":
            from view.tela_servicos import tela_servicos
            tela_servicos(root_anterior=root)
        elif opcao == "Funcionários":
            from view.lista_funcionarios import tela_lista_funcionarios
            tela_lista_funcionarios(root_anterior=root)
        elif opcao == "Relatórios":
            from view.tela_servico import tela_execucao_servico
            tela_execucao_servico(root_anterior=root)

    canvas = tk.Canvas(root, highlightthickness=0, bg=cor_fundo)
    canvas.pack(fill="both", expand=True)

    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "tabela.png")
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
    search_var.trace_add("write", lambda *args: buscar_materiais(tree, entry_busca))

    btn_cadastrar = tk.Button(canvas, text="Cadastrar Material +", font=("Arial", 11, "bold"),
                              bg="#375269", fg=cor_branco, activebackground=cor_dourado,
                              activeforeground=cor_branco, relief="flat", bd=0,
                              command=lambda: abrir_formulario_material(tree))
    btn_cadastrar_window = canvas.create_window(0, 0, window=btn_cadastrar, anchor="nw")

    def cmd_editar():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um material na lista.")
            return
        id_produto = tree.item(selecionado[0])["values"][0]
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM estoque WHERE id_produto = %s", (id_produto,))
            dados = cursor.fetchone()
            cursor.close()
            conn.close()
            if dados:
                abrir_formulario_material(tree, dados)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")

    def cmd_excluir():
        excluir_material(tree)

    frame_tabela = tk.Frame(canvas, bg="#375269")
    frame_tabela_window = canvas.create_window(0, 0, window=frame_tabela, anchor="nw")

    colunas = ("id_produto", "tipo", "quantidade")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse", height=15)
    tree.heading("id_produto", text="ID", anchor="center")
    tree.heading("tipo", text="Tipo", anchor="center")
    tree.heading("quantidade", text="Quantidade", anchor="center")
    tree.column("id_produto", width=0, stretch=False)
    tree.column("tipo", width=350, anchor="center")
    tree.column("quantidade", width=120, anchor="center")

    tree.tag_configure("odd", background="#375269")
    tree.tag_configure("even", background="#375269")

    tree.bind("<Double-1>", lambda e: cmd_editar())

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")

    def _atualizar_scrollbar(*args):
        scrollbar.set(*args)

    tree.configure(yscrollcommand=_atualizar_scrollbar)

    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    carregar_materiais(tree)

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

                ativo = (nome == "Materiais")
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

        canvas.coords(frame_top_window, cx + 30, cy - 55)
        canvas.coords(btn_cadastrar_window, cx + cw - 200, cy - 55)
        canvas.coords(frame_tabela_window, cx + 4, cy + 20)
        canvas.itemconfig(frame_tabela_window, width=max(100, cw - 4), height=max(100, ch - 42))

    def redimensionar(event):
        if event.widget != root:
            return
        w, h = event.width, event.height
        if w < 10 or h < 10:
            return
        _redimensionar(w, h)

    root.bind("<Configure>", redimensionar)
    root.after(100, lambda: [root.update_idletasks(), _redimensionar(root.winfo_width(), root.winfo_height())])


if __name__ == "__main__":
    tela_materiais()
