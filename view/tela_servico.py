import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
import customtkinter as ctk

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

    bg_image_tk = None
    img_original = None
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "tabela.png")
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

    frame = ctk.CTkFrame(canvas, fg_color="#2b3e50")
    frame_win = canvas.create_window(30, 70, window=frame, anchor="nw")

    colunas = ("id_ordem", "cliente", "carro", "total", "data")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=12)
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

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
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

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=root.destroy, width=80, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
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

        canvas.coords(titulo_win, 30, 20)

        cx = w * 0.03
        cy = h * 0.10
        cw = w * 0.75
        ch = h * 0.70
        canvas.coords(frame_win, cx, cy)
        canvas.itemconfig(frame_win, width=max(100, cw), height=max(100, ch))

        btn_x = w * 0.80
        btn_y = h * 0.10
        canvas.coords(btn_finalizar_win, btn_x, btn_y)
        canvas.coords(btn_sair_win, cx, h * 0.92)

        col_w = max(200, cw - 90)
        tree.column("cliente", width=int(col_w * 0.35))
        tree.column("carro", width=int(col_w * 0.25))
        tree.column("total", width=int(col_w * 0.20))
        tree.column("data", width=int(col_w * 0.20))

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
