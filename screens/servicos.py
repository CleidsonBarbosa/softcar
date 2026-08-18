import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector

COR_FUNDO = "#1e2d3d"
COR_DOURADO = "#b88b4a"
COR_BRANCO = "#ffffff"
COR_DESTAQUE = "#375269"
COR_HEADER = "#2c4a5c"

def _conectar():
    return mysql.connector.connect(host="localhost", user="root", password="", database="softcar")


class ServicosScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COR_FUNDO)
        self.app = app
        self._configurar_treeview_style()
        self._criar_widgets()
        self._carregar_servicos()

    def _configurar_treeview_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.layout("Treeview", [
            ("Treeview.field", {"sticky": "nswe", "children": [
                ("Treeview.padding", {"sticky": "nswe", "children": [
                    ("Treeview.treearea", {"sticky": "nswe"})
                ]})
            ]})
        ])
        style.configure("Treeview", background=COR_DESTAQUE, foreground=COR_BRANCO,
                        fieldbackground=COR_DESTAQUE, rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background=COR_HEADER, foreground=COR_BRANCO, borderwidth=0)
        style.layout("Treeview.Heading", [
            ("Treeview.Heading.cell", {"sticky": "nswe", "children": [
                ("Treeview.Heading.padding", {"sticky": "nswe", "children": [
                    ("Treeview.Heading.label", {"sticky": "nswe"})
                ]})
            ]})
        ])
        style.map("Treeview", background=[("selected", COR_DOURADO)])
        style.configure("Vertical.TScrollbar", background=COR_DESTAQUE, troughcolor=COR_DESTAQUE,
                        borderwidth=0, relief="flat")

    def _criar_widgets(self):
        header = ctk.CTkFrame(self, fg_color=COR_DESTAQUE, corner_radius=0, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Pesquisar", font=("Arial", 11, "bold"), text_color=COR_BRANCO).pack(side="left", padx=(15, 5))
        self.entry_busca = ctk.CTkEntry(header, width=220, fg_color=COR_DESTAQUE, text_color="#ffffff",
                                        border_width=1, font=("Arial", 10))
        self.entry_busca.pack(side="left", padx=5, ipady=3)
        self.entry_busca.bind("<KeyRelease>", lambda e: self._buscar_servicos())

        ctk.CTkButton(header, text="Novo Servico +", font=("Arial", 11, "bold"),
                      fg_color=COR_DESTAQUE, text_color=COR_BRANCO, hover_color=COR_HEADER,
                      command=self._abrir_formulario).pack(side="right", padx=15)

        container = ctk.CTkFrame(self, fg_color=COR_DESTAQUE, corner_radius=0)
        container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        colunas = ("id_servico", "nome_servico", "preco_servico")
        self.tree = ttk.Treeview(container, columns=colunas, show="headings", selectmode="browse")
        self.tree.heading("id_servico", text="ID")
        self.tree.heading("nome_servico", text="Servico")
        self.tree.heading("preco_servico", text="Preco")
        self.tree.column("id_servico", width=0, stretch=False)
        self.tree.column("nome_servico", width=400)
        self.tree.column("preco_servico", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<Double-1>", lambda e: self._editar_servico())

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        ctk.CTkButton(btn_frame, text="Editar", fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color=COR_HEADER, command=self._editar_servico).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Excluir", fg_color="#8b0000", text_color=COR_BRANCO,
                      hover_color="#a52a2a", command=self._excluir_servico).pack(side="left", padx=5)

    def on_show(self):
        self._carregar_servicos()

    def _carregar_servicos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_servico, nome_servico, preco_servico FROM servicos ORDER BY nome_servico")
            for row in cursor.fetchall():
                preco = f"R$ {row[2]:.2f}" if row[2] else "-"
                self.tree.insert("", "end", values=(row[0], row[1], preco))
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar servicos:\n{e}")

    def _buscar_servicos(self):
        termo = self.entry_busca.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = _conectar()
            cursor = conn.cursor()
            if termo:
                cursor.execute("SELECT id_servico, nome_servico, preco_servico FROM servicos WHERE nome_servico LIKE %s ORDER BY nome_servico",
                               (f"%{termo}%",))
            else:
                cursor.execute("SELECT id_servico, nome_servico, preco_servico FROM servicos ORDER BY nome_servico")
            for row in cursor.fetchall():
                preco = f"R$ {row[2]:.2f}" if row[2] else "-"
                self.tree.insert("", "end", values=(row[0], row[1], preco))
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")

    def _editar_servico(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione um servico na lista.")
            return
        vals = self.tree.item(sel[0])["values"]
        id_serv = vals[0]
        try:
            conn = _conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM servicos WHERE id_servico = %s", (id_serv,))
            dados = cursor.fetchone()
            cursor.close(); conn.close()
            if dados:
                ServicoForm(self.app.root, dados=dados, on_save=self._carregar_servicos)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")

    def _excluir_servico(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione um servico na lista.")
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este servico?"):
            return
        id_serv = self.tree.item(sel[0])["values"][0]
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM servicos WHERE id_servico = %s", (id_serv,))
            conn.commit()
            cursor.close(); conn.close()
            self._carregar_servicos()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

    def _abrir_formulario(self, dados=None):
        ServicoForm(self.app.root, dados=dados, on_save=self._carregar_servicos)


class ServicoForm(ctk.CTkToplevel):
    def __init__(self, parent, dados=None, on_save=None):
        super().__init__(parent)
        self.dados = dados
        self.on_save = on_save
        self.title("Editar Servico" if dados else "Novo Servico")
        self.geometry("600x400")
        self.configure(fg_color=COR_FUNDO)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.after(100, lambda: self.state("zoomed"))

        container = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(container, text="Dados do Servico", font=("Arial", 16, "bold"), text_color=COR_DOURADO).pack(pady=(0, 20))

        self.campos = ["nome_servico", "preco_servico"]
        self.labels = ["Nome", "Preco"]
        self.entries = {}

        for campo, label in zip(self.campos, self.labels):
            row = ctk.CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=label, font=("Arial", 11, "bold"), text_color=COR_BRANCO, width=100, anchor="e").pack(side="left")
            entry = ctk.CTkEntry(row, width=300, corner_radius=8, fg_color="#c2c7cc", text_color="#000000",
                                 border_color=COR_DESTAQUE, border_width=2)
            entry.pack(side="left", padx=(10, 0))
            if dados and dados.get(campo) is not None:
                entry.insert(0, str(dados[campo]))
            self.entries[campo] = entry

        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="Salvar", fg_color=COR_DOURADO, text_color=COR_BRANCO,
                      hover_color="#d4a857", command=self._salvar).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color="#2c4a5c", command=self.destroy).pack(side="left", padx=10)

    def _salvar(self):
        nome = self.entries["nome_servico"].get().strip()
        if not nome:
            messagebox.showwarning("Validacao", "O campo Nome e obrigatorio.")
            return
        preco_str = self.entries["preco_servico"].get().strip()
        preco = float(preco_str.replace(",", ".")) if preco_str else None

        try:
            conn = _conectar()
            cursor = conn.cursor()
            if self.dados:
                cursor.execute("UPDATE servicos SET nome_servico=%s, preco_servico=%s WHERE id_servico=%s",
                               (nome, preco, self.dados["id_servico"]))
            else:
                cursor.execute("INSERT INTO servicos (nome_servico, preco_servico) VALUES (%s,%s)",
                               (nome, preco))
            conn.commit()
            cursor.close(); conn.close()
            if self.on_save:
                self.on_save()
            self.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")
