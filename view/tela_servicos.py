import tkinter as tk
import customtkinter as ctk
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


def carregar_servicos(tree):
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_servico, nome_servico, estoque_id_produto, data_hora_servico FROM servicos ORDER BY nome_servico")
        for i, row in enumerate(cursor.fetchall()):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao carregar serviços:\n{e}")


def buscar_servicos(tree, entry_busca):
    termo = entry_busca.get().strip()
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        if termo:
            cursor.execute(
                "SELECT id_servico, nome_servico, preco_servico, estoque_id_produto FROM servicos WHERE nome_servico LIKE %s ORDER BY nome_servico",
                (f"%{termo}%",)
            )
        else:
            cursor.execute("SELECT id_servico, nome_servico, preco_servico, estoque_id_produto FROM servicos ORDER BY nome_servico")
        for i, row in enumerate(cursor.fetchall()):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")


def abrir_formulario_servico(tree, dados=None, root_anterior=None):
    if root_anterior:
        root_anterior.destroy()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    modal = ctk.CTk()
    modal.title("Editar Serviço" if dados else "Novo Serviço")
    modal.geometry("1200x700")
    modal.minsize(800, 500)
    modal.resizable(True, True)

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_cinza = "#777777"

    canvas = ctk.CTkCanvas(modal, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_original = None
    if os.path.exists("assets/formulario.png"):
        img_original = Image.open("assets/formulario.png")

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def navegar(opcao):
        if opcao == "Serviços":
            return
        def _navegar():
            modal.destroy()
            if opcao == "Cliente":
                from view.tela_clientes import tela_clientes
                tela_clientes(root_anterior=None)
            elif opcao == "Funcionários":
                from view.lista_funcionarios import tela_lista_funcionarios
                tela_lista_funcionarios(root_anterior=None)
            elif opcao == "Materiais":
                from view.tela_materiais import tela_materiais
                tela_materiais(root_anterior=None)
            elif opcao == "Relatórios":
                from view.tela_servico import tela_execucao_servico
                tela_execucao_servico(root_anterior=None)
        modal.after(100, _navegar)

    menu_items = []
    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        if icone is None:
            icone = _criar_icone_fallback(24, cor_dourado, "circle")
        ativo = (nome == "Serviços")
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

        def make_handler(opcao, i=nome):
            return lambda e: navegar(i)

        canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
        canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))

        canvas.image_refs = getattr(canvas, "image_refs", [])
        canvas.image_refs.append(icone)
        menu_items.append((img_item, txt_item))

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, tipo FROM estoque ORDER BY tipo")
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        produtos = []

    opcoes_produto = {f"{p[1]} (ID {p[0]})": p[0] for p in produtos}
    lista_opcoes = list(opcoes_produto.keys())

    campos = ["nome_servico", "preco_servico", "estoque_id_produto", "data_hora_servico"]
    labels = ["Nome do Serviço", "Preço", "Produto (Estoque)", "Data/Hora"]
    entries = {}
    itens_form = []

    for i, (campo, label) in enumerate(zip(campos, labels)):
        y_atual = 180 + i * 70
        lbl = canvas.create_text(0, 0, text=label, font=("Arial", 11, "bold"), fill="#ffffff", anchor="e")
        if campo == "estoque_id_produto":
            var = tk.StringVar()
            combo = ttk.Combobox(canvas, textvariable=var, values=lista_opcoes, state="readonly", width=35, font=("Arial", 12))
            entry_win = canvas.create_window(0, 0, window=combo, anchor="w")
            if dados and dados[campo]:
                for texto, pid in opcoes_produto.items():
                    if pid == dados[campo]:
                        combo.set(texto)
                        break
            entries[campo] = var
        else:
            entry = ctk.CTkEntry(canvas, fg_color="#c2c7cc", text_color="#000000", corner_radius=8, border_color="#304C62", border_width=2, width=35, font=("Arial", 12))
            entry_win = canvas.create_window(0, 0, window=entry, anchor="w")
            if dados:
                entry.insert(0, dados[campo] if dados[campo] is not None else "")
            entries[campo] = entry
        itens_form.append((lbl, entry_win))

    btn_salvar = ctk.CTkButton(canvas, text="Salvar",
                               fg_color="#b88b4a", text_color="#ffffff", hover_color="#d4a857",
                               corner_radius=8, font=("Arial", 11, "bold"))
    btn_cancelar = ctk.CTkButton(canvas, text="Cancelar",
                                 fg_color="#375269", text_color="#ffffff", hover_color="#b88b4a",
                                 corner_radius=8, font=("Arial", 11, "bold"))

    btn_salvar_win = canvas.create_window(0, 0, window=btn_salvar, anchor="center")
    btn_cancelar_win = canvas.create_window(0, 0, window=btn_cancelar, anchor="center")

    def salvar():
        nome = entries["nome_servico"].get().strip()
        if not nome:
            messagebox.showwarning("Validação", "O campo Nome do Serviço é obrigatório.")
            return
        preco_str = entries["preco_servico"].get().strip()
        if preco_str:
            try:
                preco = float(preco_str)
            except ValueError:
                messagebox.showwarning("Validação", "Preço inválido.")
                return
        else:
            preco = None
        produto_texto = entries["estoque_id_produto"].get().strip()
        if not produto_texto:
            messagebox.showwarning("Validação", "Selecione um Produto.")
            return
        if produto_texto not in opcoes_produto:
            messagebox.showwarning("Validação", "Produto selecionado inválido.")
            return
        id_produto = str(opcoes_produto[produto_texto])
        data_hora = entries["data_hora_servico"].get().strip() or None
        try:
            conn = conectar()
            cursor = conn.cursor()
            if dados:
                cursor.execute(
                    "UPDATE servicos SET nome_servico=%s, preco_servico=%s, estoque_id_produto=%s, data_hora_servico=%s WHERE id_servico=%s",
                    (nome, preco, id_produto, data_hora, dados["id_servico"])
                )
            else:
                cursor.execute(
                    "INSERT INTO servicos (nome_servico, preco_servico, estoque_id_produto, data_hora_servico) VALUES (%s, %s, %s, %s)",
                    (nome, preco, id_produto, data_hora)
                )
            conn.commit()
            cursor.close()
            conn.close()
            modal.after(100, lambda: (modal.destroy(), tela_servicos(root_anterior=None)))
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    def voltar():
        modal.after(100, lambda: (modal.destroy(), tela_servicos(root_anterior=None)))

    btn_salvar.configure(command=salvar)
    btn_cancelar.configure(command=voltar)

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

        x_label = w * 0.30
        x_entry = w * 0.32
        y_inicio = h * 0.35

        for i, (lbl, entry_win) in enumerate(itens_form):
            y_atual = y_inicio + i * 70
            canvas.coords(lbl, x_label, y_atual)
            canvas.coords(entry_win, x_entry, y_atual)

        btn_x = w * 0.75
        btn_y1 = y_inicio + 140
        btn_y2 = y_inicio + 190
        canvas.coords(btn_salvar_win, btn_x, btn_y1)
        canvas.coords(btn_cancelar_win, btn_x, btn_y2)

    modal.bind("<Configure>", _redimensionar)
    modal.after(100, lambda: [modal.update_idletasks(), _redimensionar()])

    def maximizar():
        modal.update_idletasks()
        modal.state("zoomed")
        try:
            modal.attributes('-zoomed', True)
        except:
            pass
        modal.update_idletasks()
        _redimensionar(None)
    modal.after(200, maximizar)

    modal.mainloop()


def excluir_servico(tree):
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um serviço na lista.")
        return
    if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este serviço?"):
        return
    id_servico = tree.item(selecionado[0])["values"][0]
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM servicos WHERE id_servico = %s", (id_servico,))
        conn.commit()
        cursor.close()
        conn.close()
        carregar_servicos(tree)
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


def tela_servicos(root_anterior=None):
    if root_anterior:
        root_anterior.destroy()
    root = ctk.CTk()
    root.title("Soft Car - Lista de Serviços")
    root.geometry("1200x700")
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
        if opcao == "Serviços":
            return
        def _navegar():
            if opcao == "Cliente":
                from view.tela_clientes import tela_clientes
                tela_clientes(root_anterior=root)
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

    frame_top = ctk.CTkFrame(canvas, fg_color="#375269")
    frame_top_window = canvas.create_window(0, 0, window=frame_top, anchor="nw")

    ctk.CTkLabel(frame_top, text="Pesquisar", font=("Arial", 11, "bold"), fg_color="transparent", text_color=cor_branco).pack(side="left", padx=5)
    search_var = tk.StringVar()
    entry_busca = ctk.CTkEntry(frame_top, fg_color="#375269", text_color="#ffffff", corner_radius=8, border_color="#304C62", border_width=2, textvariable=search_var, font=("Arial", 10))
    entry_busca.pack(side="left", padx=5, ipady=3)
    search_var.trace_add("write", lambda *args: buscar_servicos(tree, entry_busca))

    btn_cadastrar = ctk.CTkButton(canvas, text="Cadastrar Serviço +", font=("Arial", 11, "bold"),
                                  fg_color="#375269", text_color=cor_branco, hover_color=cor_dourado,
                                  corner_radius=8,
                                  command=lambda: abrir_formulario_servico(tree, root_anterior=root))
    btn_cadastrar_window = canvas.create_window(0, 0, window=btn_cadastrar, anchor="nw")

    def cmd_editar():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um serviço na lista.")
            return
        id_servico = tree.item(selecionado[0])["values"][0]
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM servicos WHERE id_servico = %s", (id_servico,))
            dados = cursor.fetchone()
            cursor.close()
            conn.close()
            if dados:
                abrir_formulario_servico(tree, dados, root_anterior=root)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")

    def cmd_excluir():
        excluir_servico(tree)

    frame_tabela = ctk.CTkFrame(canvas, fg_color="#375269")
    frame_tabela_window = canvas.create_window(0, 0, window=frame_tabela, anchor="nw")

    colunas = ("id_servico", "nome_servico", "preco_servico", "estoque_id_produto")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse", height=8)
    tree.heading("id_servico", text="ID")
    tree.heading("nome_servico", text="Serviço")
    tree.heading("preco_servico", text="Valor")
    tree.heading("estoque_id_produto", text="ID Produto")
    tree.column("id_servico", width=70, stretch=False, anchor="center")
    tree.column("nome_servico", width=250, stretch=True)
    tree.column("preco_servico", width=100, stretch=True, anchor="center")
    tree.column("estoque_id_produto", width=120, stretch=True, anchor="center")

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

    carregar_servicos(tree)

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

                ativo = (nome == "Serviços")
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
        canvas.coords(btn_cadastrar_window, cx + cw - 190, cy - 55)
        canvas.coords(frame_tabela_window, cx + 4, cy + 20)
        canvas.itemconfig(frame_tabela_window, width=max(100, cw - 4), height=max(100, ch - 42))

        col_w = max(200, cw - 90)
        tree.column("nome_servico", width=int(col_w * 0.50))
        tree.column("preco_servico", width=int(col_w * 0.20))
        tree.column("estoque_id_produto", width=int(col_w * 0.30))

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
        root.update_idletasks()
        _redimensionar(root.winfo_width(), root.winfo_height())
    root.after(200, maximizar)

    btn_sair = ctk.CTkButton(root, text="Sair", command=root.destroy, width=80, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    tela_servicos()
