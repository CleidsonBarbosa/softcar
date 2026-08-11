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

    # ---- MENU VERTICAL ----
    y_pos = 220
    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        if icone is None:
            icone = _criar_icone_fallback(24, cor_dourado, "circle")
        ativo = (nome == "Relatórios")
        cor_texto = "#777777" if ativo else cor_branco

        img_item = canvas.create_image(20, y_pos, image=icone, anchor="nw")
        txt_item = canvas.create_text(50, y_pos + 12, text=nome, font=("Arial", 11, "bold"), fill=cor_texto, anchor="nw")

        def make_handler(opcao):
            return lambda e: navegar(opcao)

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

    ctk.CTkLabel(canvas, text="EXECUÇÃO DE SERVIÇO", font=("Arial", 18, "bold"), text_color=cor_dourado).place(x=30, y=20)

    frame = ctk.CTkFrame(canvas, fg_color="#2b3e50")
    frame.place(x=30, y=70, width=500, height=400)

    colunas = ("id_ordem", "cliente", "carro", "total", "data")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=18)
    tree.heading("id_ordem", text="Ordem #")
    tree.heading("cliente", text="Cliente")
    tree.heading("carro", text="Carro (Placa)")
    tree.heading("total", text="Total")
    tree.heading("data", text="Data")
    tree.column("id_ordem", width=70, anchor="center")
    tree.column("cliente", width=150)
    tree.column("carro", width=120)
    tree.column("total", width=80, anchor="center")
    tree.column("data", width=150)

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

    ctk.CTkButton(canvas, text="Finalizar Ordem", command=finalizar_ordem, width=120).place(x=550, y=70)
    ctk.CTkButton(canvas, text="Sair", command=root.destroy, width=80).place(x=30, y=480)

    root.mainloop()
