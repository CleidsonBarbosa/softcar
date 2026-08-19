import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from screens.base import BaseScreen

COR_FUNDO = "#1e2d3d"
COR_DOURADO = "#b88b4a"
COR_BRANCO = "#ffffff"
COR_DESTAQUE = "#375269"
COR_HEADER = "#2c4a5c"

def _conectar():
    return mysql.connector.connect(host="localhost", user="root", password="", database="softcar")


class ClientesScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._configurar_treeview_style()
        self._criar_widgets()

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
                        fieldbackground=COR_DESTAQUE, rowheight=32, borderwidth=0)
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
        ov = self.center_frame

        header = ctk.CTkFrame(ov, fg_color="transparent", height=42)
        header.pack(fill="x", padx=20, pady=(10, 5))
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Pesquisar", font=("Arial", 13, "bold"), text_color=COR_BRANCO).pack(side="left", padx=(0, 8))
        self.entry_busca = ctk.CTkEntry(header, width=280, height=32, fg_color=COR_DESTAQUE, text_color="#ffffff",
                                        border_width=1, font=("Arial", 12), corner_radius=8)
        self.entry_busca.pack(side="left", padx=5, ipady=2)
        self.entry_busca.bind("<KeyRelease>", lambda e: self._buscar_clientes())

        ctk.CTkButton(header, text="Cadastrar Cliente +", font=("Arial", 12, "bold"),
                      fg_color=COR_DOURADO, text_color=COR_BRANCO,
                      hover_color="#d4a857", height=32, corner_radius=8,
                      command=self._abrir_formulario_cliente).pack(side="right", padx=5)

        container = ctk.CTkFrame(ov, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 5))

        colunas = ("id_cliente", "nome_cliente", "email_cliente", "telefone_cliente", "cpf", "endereco")
        self.tree = ttk.Treeview(container, columns=colunas, show="headings", selectmode="browse")
        self.tree.heading("id_cliente", text="ID", anchor="center")
        self.tree.heading("nome_cliente", text="Nome", anchor="w")
        self.tree.heading("email_cliente", text="E-mail", anchor="w")
        self.tree.heading("telefone_cliente", text="Telefone", anchor="center")
        self.tree.heading("cpf", text="CPF", anchor="center")
        self.tree.heading("endereco", text="Endereco", anchor="w")

        self.tree.column("id_cliente", width=50, minwidth=50, stretch=False, anchor="center")
        self.tree.column("nome_cliente", width=200, minwidth=120, stretch=True, anchor="w")
        self.tree.column("email_cliente", width=220, minwidth=120, stretch=True, anchor="w")
        self.tree.column("telefone_cliente", width=130, minwidth=100, stretch=False, anchor="center")
        self.tree.column("cpf", width=140, minwidth=100, stretch=False, anchor="center")
        self.tree.column("endereco", width=200, minwidth=120, stretch=True, anchor="w")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 2), pady=2)
        self.tree.pack(side="left", fill="both", expand=True, padx=(2, 0), pady=2)

        self.tree.bind("<Double-1>", lambda e: self._editar_cliente())

        btn_frame = ctk.CTkFrame(ov, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkButton(btn_frame, text="Editar", font=("Arial", 12, "bold"), fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color=COR_HEADER, height=32, corner_radius=8, width=100,
                      command=self._editar_cliente).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Excluir", font=("Arial", 12, "bold"), fg_color="#8b0000", text_color=COR_BRANCO,
                      hover_color="#a52a2a", height=32, corner_radius=8, width=100,
                      command=self._excluir_cliente).pack(side="left", padx=5)

    def on_show(self):
        super().on_show()
        self._carregar_clientes()

    def _carregar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco FROM clientes ORDER BY nome_cliente")
            for i, row in enumerate(cursor.fetchall()):
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=row, tags=(tag,))
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar clientes:\n{e}")

    def _buscar_clientes(self):
        termo = self.entry_busca.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = _conectar()
            cursor = conn.cursor()
            if termo:
                cursor.execute(
                    "SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco FROM clientes WHERE nome_cliente LIKE %s OR email_cliente LIKE %s OR cpf LIKE %s ORDER BY nome_cliente",
                    (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
            else:
                cursor.execute("SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, cpf, endereco FROM clientes ORDER BY nome_cliente")
            for i, row in enumerate(cursor.fetchall()):
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=row, tags=(tag,))
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")

    def _editar_cliente(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione um cliente na lista.")
            return
        vals = self.tree.item(sel[0])["values"]
        id_cli = vals[0]
        try:
            conn = _conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cli,))
            dados = cursor.fetchone()
            cursor.close(); conn.close()
            if dados:
                ClienteForm(self.app.root, dados=dados, on_save=self._carregar_clientes)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")

    def _excluir_cliente(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione um cliente na lista.")
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este cliente?"):
            return
        id_cli = self.tree.item(sel[0])["values"][0]
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cli,))
            conn.commit()
            cursor.close(); conn.close()
            self._carregar_clientes()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

    def _abrir_formulario_cliente(self, dados=None):
        ClienteForm(self.app.root, dados=dados, on_save=self._carregar_clientes)


class ClienteForm(ctk.CTkToplevel):
    def __init__(self, parent, dados=None, on_save=None):
        super().__init__(parent)
        self.dados = dados
        self.on_save = on_save
        self.title("Editar Cliente" if dados else "Novo Cliente")
        self.configure(fg_color=COR_FUNDO)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.after(100, lambda: self.state("zoomed"))

        self.campos = ["nome_cliente", "email_cliente", "telefone_cliente", "cpf", "endereco", "data_nascimento"]
        self.labels = ["Nome", "E-mail", "Telefone", "CPF", "Endereco", "Data de Nasc."]
        self.entries = {}

        container = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        container.pack(fill="both", expand=True, padx=60, pady=40)

        ctk.CTkLabel(container, text="Dados do Cliente", font=("Arial", 20, "bold"), text_color=COR_DOURADO).pack(pady=(0, 25))

        for campo, label in zip(self.campos, self.labels):
            row = ctk.CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", pady=6)
            ctk.CTkLabel(row, text=label, font=("Arial", 13, "bold"), text_color=COR_BRANCO, width=140, anchor="e").pack(side="left")
            entry = ctk.CTkEntry(row, width=400, height=38, corner_radius=8, fg_color="#c2c7cc", text_color="#000000",
                                 border_color=COR_DESTAQUE, border_width=2, font=("Arial", 13))
            entry.pack(side="left", padx=(15, 0))
            if dados and dados.get(campo):
                entry.insert(0, str(dados[campo]))
            self.entries[campo] = entry

        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(pady=25)
        ctk.CTkButton(btn_frame, text="Salvar", font=("Arial", 13, "bold"), width=150, height=40,
                      fg_color=COR_DOURADO, text_color=COR_BRANCO,
                      hover_color="#d4a857", command=self._salvar).pack(side="left", padx=12)
        ctk.CTkButton(btn_frame, text="Cancelar", font=("Arial", 13, "bold"), width=150, height=40,
                      fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color="#2c4a5c", command=self.destroy).pack(side="left", padx=12)

    def _salvar(self):
        valores = {}
        for campo, entry in self.entries.items():
            val = entry.get().strip()
            if campo in ("nome_cliente", "cpf") and not val:
                messagebox.showwarning("Validacao", f"O campo {campo} e obrigatorio.")
                return
            valores[campo] = val if val else None
        try:
            conn = _conectar()
            cursor = conn.cursor()
            if self.dados:
                cursor.execute(
                    "UPDATE clientes SET nome_cliente=%s, email_cliente=%s, telefone_cliente=%s, cpf=%s, endereco=%s, data_nascimento=%s WHERE id_cliente=%s",
                    (valores["nome_cliente"], valores["email_cliente"], valores["telefone_cliente"],
                     valores["cpf"], valores["endereco"], valores["data_nascimento"], self.dados["id_cliente"]))
            else:
                cursor.execute(
                    "INSERT INTO clientes (nome_cliente, email_cliente, telefone_cliente, cpf, endereco, data_nascimento) VALUES (%s,%s,%s,%s,%s,%s)",
                    (valores["nome_cliente"], valores["email_cliente"], valores["telefone_cliente"],
                     valores["cpf"], valores["endereco"], valores["data_nascimento"]))
            conn.commit()
            cursor.close(); conn.close()
            if self.on_save:
                self.on_save()
            self.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")
