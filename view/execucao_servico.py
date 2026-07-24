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


def tela_execucao_servico(id_func, nome_func):
    root = ctk.CTk()
    root.title("Soft Car - Execução de Serviços")
    root.geometry("1000x600")
    root.minsize(800, 500)

    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    if os.path.exists("assets/dashboard.png"):
        img = Image.open("assets/dashboard.png")
        img = img.resize((1000, 600), Image.Resampling.LANCZOS)
        bg_img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=bg_img, anchor="nw")
        canvas.image = bg_img

    ctk.CTkLabel(canvas, text=f"Lavador: {nome_func}", font=("Arial", 14, "bold"), text_color="#ffffff").place(x=30, y=20)
    ctk.CTkLabel(canvas, text="ORDENS DE SERVIço EM ABERTO", font=("Arial", 16, "bold"), text_color="#b88b4a").place(x=30, y=60)

    frame = tk.Frame(canvas, bg="#2b3e50")
    frame.place(x=30, y=110, width=940, height=440)

    colunas = ("id_ordem", "cliente", "carro", "data", "total")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=18)
    tree.heading("id_ordem", text="Ordem #")
    tree.heading("cliente", text="Cliente")
    tree.heading("carro", text="Placa")
    tree.heading("data", text="Data/Hora")
    tree.heading("total", text="Total")
    tree.column("id_ordem", width=80, anchor="center")
    tree.column("cliente", width=300)
    tree.column("carro", width=120, anchor="center")
    tree.column("data", width=200, anchor="center")
    tree.column("total", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#375269", foreground="#ffffff", fieldbackground="#375269", rowheight=28, borderwidth=0)
    style.configure("Treeview.Heading", background="#2c4a5c", foreground="#ffffff", borderwidth=0)
    style.layout("Treeview", [("Treeview.field", {"sticky": "nswe", "children": [("Treeview.padding", {"sticky": "nswe", "children": [("Treeview.treearea", {"sticky": "nswe"})]})]})])

    def carregar_ordens():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT os.id_ordem, c.nome_cliente, COALESCE(ca.placa, '-'), os.data_hora, os.total
                FROM ordem_servico os
                JOIN clientes c ON c.id_cliente = os.id_cliente
                LEFT JOIN carros ca ON ca.id_carro = os.id_carro
                WHERE os.status = 'aberto'
                ORDER BY os.data_hora DESC
            """)
            for row in cursor.fetchall():
                data_str = row[3].strftime("%d/%m/%Y %H:%M") if row[3] else "-"
                total_str = f"R$ {row[4]:.2f}" if row[4] else "R$ 0.00"
                tree.insert("", "end", values=(row[0], row[1], row[2], data_str, total_str))
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar ordens:\n{e}")

    carregar_ordens()

    def finalizar_ordem():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione uma ordem de serviço.")
            return
        valores = tree.item(selecionado[0])["values"]
        id_ordem = valores[0]
        if not messagebox.askyesno("Confirmar", f"Finalizar ordem #{id_ordem}?"):
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE ordem_servico SET status = 'finalizado' WHERE id_ordem = %s", (id_ordem,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", f"Ordem #{id_ordem} finalizada!")
            carregar_ordens()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao finalizar:\n{e}")

    def ver_itens():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione uma ordem de serviço.")
            return
        valores = tree.item(selecionado[0])["values"]
        id_ordem = valores[0]
        modal = ctk.CTkToplevel()
        modal.title(f"Itens da Ordem #{id_ordem}")
        modal.geometry("500x400")
        modal.grab_set()
        canvas2 = tk.Canvas(modal, highlightthickness=0, bg="#2b3e50")
        canvas2.pack(fill="both", expand=True)
        frame2 = tk.Frame(canvas2, bg="#2b3e50")
        frame2.place(x=20, y=20, width=460, height=330)
        cols = ("servico", "preco")
        tv = ttk.Treeview(frame2, columns=cols, show="headings", height=14)
        tv.heading("servico", text="Serviço")
        tv.heading("preco", text="Preço")
        tv.column("servico", width=320)
        tv.column("preco", width=100, anchor="center")
        tv.pack(fill="both", expand=True)
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.nome_servico, oi.preco
                FROM ordem_servico_itens oi
                JOIN servicos s ON s.id_servico = oi.id_servico
                WHERE oi.id_ordem = %s
            """, (id_ordem,))
            for servico, preco in cursor.fetchall():
                tv.insert("", "end", values=(servico, f"R$ {preco:.2f}" if preco else "-"))
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar itens:\n{e}")
        ctk.CTkButton(canvas2, text="Fechar", command=modal.destroy).place(x=200, y=360)

    ctk.CTkButton(canvas, text="Ver Itens", command=ver_itens, width=90).place(x=30, y=560)
    ctk.CTkButton(canvas, text="Finalizar", command=finalizar_ordem, width=90).place(x=140, y=560)
    ctk.CTkButton(canvas, text="Atualizar", command=carregar_ordens, width=90).place(x=250, y=560)

    root.mainloop()
