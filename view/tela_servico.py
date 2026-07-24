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


def tela_execucao_servico():
    root = tk.Tk()
    root.title("Soft Car - Execução de Serviço")
    root.state("zoomed")
    root.minsize(800, 500)

    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"
    cor_fundo = "#2b3e50"

    canvas = tk.Canvas(root, highlightthickness=0, bg=cor_fundo)
    canvas.pack(fill="both", expand=True)

    ctk.CTkLabel(canvas, text="EXECUÇÃO DE SERVIÇO", font=("Arial", 18, "bold"), text_color=cor_dourado).place(x=30, y=20)

    frame = tk.Frame(canvas, bg="#2b3e50")
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
