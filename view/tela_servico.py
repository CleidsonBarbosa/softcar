import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
import customtkinter as ctk
from view.img_softcar_utils import carregar_img_softcar, criar_img_softcar, redimensionar_img_softcar

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
from datetime import datetime


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="softcar"
    )


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


def tela_execucao_servico(root_anterior=None):
    if root_anterior:
        root_anterior.destroy()
    root = ctk.CTk()
    root.title("Soft Car - Execução de Serviço")
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
        if opcao == "Relatórios":
            return
        def _navegar():
            if opcao == "Cliente":
                from view.tela_clientes import tela_clientes
                tela_clientes(root_anterior=root)
            elif opcao == "Serviços":
                from view.tela_servicos import tela_servicos
                tela_servicos(root_anterior=root)
            elif opcao == "Funcionários":
                from view.lista_funcionarios import tela_lista_funcionarios
                tela_lista_funcionarios(root_anterior=root)
            elif opcao == "Materiais":
                from view.tela_materiais import tela_materiais
                tela_materiais(root_anterior=root)
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

    bg_image_tk = None
    img_original = None
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img_frame.png")
    if os.path.exists(img_path):
        img_original = Image.open(img_path)

    menu_items = []
    img_refs = []

    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        if icone is None:
            icone = _criar_icone_fallback(24, cor_dourado, "circle")
        ativo = (nome == "Relatórios")
        cor_texto = "#777777" if ativo else cor_branco

        img_item = canvas.create_image(20, 0, image=icone, anchor="nw")
        txt_item = canvas.create_text(50, 12, text=nome, font=("Arial", 11, "bold"), fill=cor_texto, anchor="nw")

        def on_enter(e, txt=txt_item):
            canvas.itemconfig(txt, fill=cor_dourado)
        def on_leave(e, txt=txt_item, cor=cor_texto):
            canvas.itemconfig(txt, fill=cor)

        canvas.tag_bind(img_item, "<Enter>", on_enter)
        canvas.tag_bind(img_item, "<Leave>", on_leave)
        canvas.tag_bind(txt_item, "<Enter>", on_enter)
        canvas.tag_bind(txt_item, "<Leave>", on_leave)

        def make_handler(opcao):
            return lambda e: navegar(opcao)

        canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
        canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))

        img_refs.append(icone)
        menu_items.append((img_item, txt_item))

    titulo_lbl = ctk.CTkLabel(canvas, text="EXECUÇÃO DE SERVIÇO", font=("Arial", 18, "bold"), text_color=cor_dourado)
    titulo_win = canvas.create_window(30, 20, window=titulo_lbl, anchor="nw")

    frame = ctk.CTkFrame(canvas, fg_color="transparent", corner_radius=8, border_width=0)
    frame_win = canvas.create_window(0, 0, window=frame, anchor="nw")

    colunas = ("id_ordem", "cliente", "carro", "total", "data")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=6)
    tree.heading("id_ordem", text="Ordem #")
    tree.heading("cliente", text="Cliente")
    tree.heading("carro", text="Carro (Placa)")
    tree.heading("total", text="Total")
    tree.heading("data", text="Data")
    tree.column("id_ordem", width=70, stretch=False, anchor="center")
    tree.column("cliente", width=200, stretch=True)
    tree.column("carro", width=150, stretch=True)
    tree.column("total", width=100, stretch=True, anchor="center")
    tree.column("data", width=150, stretch=True, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)

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
                    foreground="#ffffff",
                    fieldbackground="#375269",
                    rowheight=28,
                    borderwidth=0,
                    bordercolor="#375269",
                    lightcolor="#375269",
                    darkcolor="#375269",
                    troughcolor="#375269")
    style.configure("Treeview.Heading",
                    background="#2c4a5c",
                    foreground="#ffffff",
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
              background=[("selected", "#b88b4a")])
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
    scrollbar.pack(side="right", fill="y")

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT os.id_ordem, c.nome_cliente, cr.placa, os.total, os.data_hora
            FROM ordem_servico os
            JOIN clientes c ON c.id_cliente = os.id_cliente
            LEFT JOIN carros cr ON cr.id_carro = os.id_carro
            WHERE os.status = 'aberto'
            ORDER BY os.data_hora DESC
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar ordens:\n{e}")

    def finalizar_ordem():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione uma ordem de serviço.")
            return
        id_ordem = tree.item(selecionado[0])["values"][0]
        if messagebox.askyesno("Confirmar", f"Finalizar ordem #{id_ordem}?"):
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("UPDATE ordem_servico SET status = 'finalizado' WHERE id_ordem = %s", (id_ordem,))
                conn.commit()
                cursor.close()
                conn.close()
                tree.delete(selecionado[0])
                messagebox.showinfo("Sucesso", f"Ordem #{id_ordem} finalizada!")
            except mysql.connector.Error as e:
                messagebox.showerror("Erro", f"Erro ao finalizar:\n{e}")

    btn_finalizar = ctk.CTkButton(canvas, text="Finalizar Ordem", command=finalizar_ordem, width=120, fg_color=cor_dourado, text_color=cor_branco, hover_color="#d4a857")
    btn_finalizar_win = canvas.create_window(550, 70, window=btn_finalizar, anchor="nw")

    def voltar_login():
        root.destroy()
        from main import tela_login
        tela_login()

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    def _redimensionar(event=None):
        nonlocal bg_image_tk
        w, h = root.winfo_width(), root.winfo_height()
        if w < 10 or h < 10:
            return

        if img_original:
            img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_image_tk = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
            canvas.tag_lower("bg")

        y = 220
        for img_item, txt_item in menu_items:
            canvas.coords(img_item, 20, y)
            canvas.coords(txt_item, 50, y + 12)
            y += 50

        cx = w * 0.191
        cy = h * 0.178
        cw = w * 0.753
        ch = h * 0.750
        canvas.coords(titulo_win, cx + 176, cy - 42)

        canvas.coords(frame_win, cx + 176, cy - 42)
        canvas.itemconfig(frame_win, width=max(100, cw - 254), height=max(100, ch - 22))

        canvas.coords(btn_finalizar_win, cx + cw - 150, cy - 42)
        canvas.coords(btn_sair_win, w * 0.02, h - 50)

        col_w = max(200, cw - 90)
        tree.column("cliente", width=int(col_w * 0.28))
        tree.column("carro", width=int(col_w * 0.20))
        tree.column("total", width=int(col_w * 0.16))
        tree.column("data", width=int(col_w * 0.16))

        redimensionar_img_softcar(canvas, btn_dashboard_id, img_softcar_original, w, h)

    root.bind("<Configure>", _redimensionar)
    root.after(100, lambda: [root.update_idletasks(), _redimensionar()])

    def maximizar():
        root.update_idletasks()
        root.state("zoomed")
        try:
            root.attributes('-zoomed', True)
        except:
            pass
        root.update_idletasks()
        _redimensionar()
    root.after(200, maximizar)

    root.mainloop()
