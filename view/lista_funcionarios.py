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

def carregar_funcionarios(tree):
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_func, nome_func, email_func, telefone_func, cpf_func, cargo FROM funcionarios ORDER BY nome_func")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
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
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")

def abrir_formulario(tree, dados=None):
    modal = tk.Toplevel()
    modal.title("Editar Funcionário" if dados else "Novo Funcionário")
    modal.geometry("400x450")
    modal.resizable(False, False)
    modal.transient(tree.winfo_toplevel())
    modal.grab_set()

    frame = ttk.Frame(modal, padding=20)
    frame.pack(fill="both", expand=True)

    campos = ["nome_func", "email_func", "telefone_func", "cpf_func", "cargo", "endereco_func", "data_nascimento_func", "senha"]
    labels = ["Nome", "E-mail", "Telefone", "CPF", "Cargo (lavador/atendente)", "Endereço", "Data de Nascimento (YYYY-MM-DD)", "Senha"]
    entries = {}

    for i, (campo, label) in enumerate(zip(campos, labels)):
        ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=4)
        entry = ttk.Entry(frame, width=40)
        entry.grid(row=i, column=1, pady=4)
        if dados:
            entry.insert(0, dados[campo])
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
            carregar_funcionarios(tree)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
    ttk.Button(btn_frame, text="Salvar", command=salvar).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Cancelar", command=modal.destroy).pack(side="left", padx=5)

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

def tela_lista_funcionarios():
    janela = tk.Toplevel()
    janela.title("Soft Car - Lista de Funcionários")
    janela.geometry("900x500")
    janela.minsize(700, 400)

    canvas = tk.Canvas(janela, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_path = "assets/listar_funcionarios.png"
    img_original = None
    if os.path.exists(img_path):
        img_original = Image.open(img_path)

    bg_image_tk = None

    # ---- BARRA DE BUSCA ----
    frame_top = tk.Frame(canvas, bg="#f0f0f0", padx=10, pady=10)
    frame_top_window = canvas.create_window(0, 0, window=frame_top, anchor="nw")

    tk.Label(frame_top, text="Buscar:", font=("Arial", 10), bg="#f0f0f0").pack(side="left", padx=5)
    entry_busca = tk.Entry(frame_top, width=30, font=("Arial", 10))
    entry_busca.pack(side="left", padx=5)
    tk.Button(frame_top, text="Buscar", font=("Arial", 9), command=lambda: buscar_funcionarios(tree, entry_busca)).pack(side="left", padx=5)
    tk.Button(frame_top, text="Limpar", font=("Arial", 9), command=lambda: [entry_busca.delete(0, "end"), carregar_funcionarios(tree)]).pack(side="left", padx=5)

    # ---- BOTÕES DE AÇÃO ----
    frame_btns = tk.Frame(canvas, bg="#f0f0f0", padx=10, pady=5)
    frame_btns_window = canvas.create_window(0, 0, window=frame_btns, anchor="nw")
    tk.Button(frame_btns, text="Novo", font=("Arial", 9), command=lambda: abrir_formulario(tree)).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Editar", font=("Arial", 9), command=lambda: editar_selecionado(tree)).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Excluir", font=("Arial", 9), command=lambda: excluir_funcionario(tree)).pack(side="left", padx=5)

    # ---- TABELA (direto no canvas, sem frame opaco) ----
    colunas = ("id_func", "nome_func", "email_func", "telefone_func", "cpf_func", "cargo")
    tree = ttk.Treeview(canvas, columns=colunas, show="headings", selectmode="browse")
    tree.heading("id_func", text="ID")
    tree.heading("nome_func", text="Nome")
    tree.heading("email_func", text="E-mail")
    tree.heading("telefone_func", text="Telefone")
    tree.heading("cpf_func", text="CPF")
    tree.heading("cargo", text="Cargo")
    tree.column("id_func", width=0, stretch=False)  # coluna oculta
    tree.column("cpf_func", width=0, stretch=False)  # coluna oculta
    tree.column("nome_func", width=250)
    tree.column("email_func", width=250)
    tree.column("telefone_func", width=150, anchor="center")
    tree.column("cargo", width=120, anchor="center")

    scrollbar = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree_window = canvas.create_window(0, 0, window=tree, anchor="nw")
    scrollbar_window = canvas.create_window(0, 0, window=scrollbar, anchor="ne")

    def editar_selecionado(tree):
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

    carregar_funcionarios(tree)

    # ---- REDIMENSIONAMENTO ----
    def _redimensionar(w, h):
        nonlocal bg_image_tk
        if img_original:
            img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_image_tk = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
        canvas.coords(frame_top_window, 10, 10)
        canvas.coords(frame_btns_window, 10, 55)
        canvas.coords(tree_window, 10, 100)
        canvas.itemconfig(tree_window, width=w - 40, height=max(100, h - 120))
        canvas.coords(scrollbar_window, w - 20, 100)
        canvas.itemconfig(scrollbar_window, height=max(100, h - 120))

    def redimensionar(event):
        if event.widget != janela:
            return
        w, h = event.width, event.height
        if w < 10 or h < 10:
            return
        _redimensionar(w, h)

    janela.bind("<Configure>", redimensionar)
    janela.after(50, lambda: [janela.update_idletasks(), _redimensionar(janela.winfo_width(), janela.winfo_height())])

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    tela_lista_funcionarios()
    root.mainloop()