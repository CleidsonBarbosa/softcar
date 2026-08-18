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


class FuncionariosScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COR_FUNDO)
        self.app = app
        self._configurar_treeview_style()
        self._criar_widgets()
        self._carregar_funcionarios()

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
        self.entry_busca.bind("<KeyRelease>", lambda e: self._buscar_funcionarios())

        ctk.CTkButton(header, text="Novo Funcionario +", font=("Arial", 11, "bold"),
                      fg_color=COR_DESTAQUE, text_color=COR_BRANCO, hover_color=COR_HEADER,
                      command=self._abrir_formulario).pack(side="right", padx=15)

        container = ctk.CTkFrame(self, fg_color=COR_DESTAQUE, corner_radius=0)
        container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        colunas = ("id_func", "nome_func", "email_func", "cargo", "telefone_func")
        self.tree = ttk.Treeview(container, columns=colunas, show="headings", selectmode="browse")
        self.tree.heading("id_func", text="ID")
        self.tree.heading("nome_func", text="Nome")
        self.tree.heading("email_func", text="E-mail")
        self.tree.heading("cargo", text="Cargo")
        self.tree.heading("telefone_func", text="Telefone")
        self.tree.column("id_func", width=0, stretch=False)
        self.tree.column("nome_func", width=180)
        self.tree.column("email_func", width=200)
        self.tree.column("cargo", width=120, anchor="center")
        self.tree.column("telefone_func", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<Double-1>", lambda e: self._editar_funcionario())

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        ctk.CTkButton(btn_frame, text="Editar", fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color=COR_HEADER, command=self._editar_funcionario).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Excluir", fg_color="#8b0000", text_color=COR_BRANCO,
                      hover_color="#a52a2a", command=self._excluir_funcionario).pack(side="left", padx=5)

    def on_show(self):
        self._carregar_funcionarios()

    def _carregar_funcionarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_func, nome_func, email_func, cargo, telefone_func FROM funcionarios ORDER BY nome_func")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar funcionarios:\n{e}")

    def _buscar_funcionarios(self):
        termo = self.entry_busca.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = _conectar()
            cursor = conn.cursor()
            if termo:
                cursor.execute("SELECT id_func, nome_func, email_func, cargo, telefone_func FROM funcionarios WHERE nome_func LIKE %s OR email_func LIKE %s OR cargo LIKE %s ORDER BY nome_func",
                               (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
            else:
                cursor.execute("SELECT id_func, nome_func, email_func, cargo, telefone_func FROM funcionarios ORDER BY nome_func")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")

    def _editar_funcionario(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione um funcionario na lista.")
            return
        vals = self.tree.item(sel[0])["values"]
        id_func = vals[0]
        try:
            conn = _conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM funcionarios WHERE id_func = %s", (id_func,))
            dados = cursor.fetchone()
            cursor.close(); conn.close()
            if dados:
                FuncionarioForm(self.app.root, dados=dados, on_save=self._carregar_funcionarios)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")

    def _excluir_funcionario(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione um funcionario na lista.")
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este funcionario?"):
            return
        id_func = self.tree.item(sel[0])["values"][0]
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM funcionarios WHERE id_func = %s", (id_func,))
            conn.commit()
            cursor.close(); conn.close()
            self._carregar_funcionarios()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

    def _abrir_formulario(self, dados=None):
        FuncionarioForm(self.app.root, dados=dados, on_save=self._carregar_funcionarios)


class FuncionarioForm(ctk.CTkToplevel):
    def __init__(self, parent, dados=None, on_save=None):
        super().__init__(parent)
        self.dados = dados
        self.on_save = on_save
        self.title("Editar Funcionario" if dados else "Novo Funcionario")
        self.geometry("600x500")
        self.configure(fg_color=COR_FUNDO)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.after(100, lambda: self.state("zoomed"))

        container = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(container, text="Dados do Funcionario", font=("Arial", 16, "bold"), text_color=COR_DOURADO).pack(pady=(0, 20))

        self.labels_map = {
            "nome_func": "Nome",
            "email_func": "E-mail",
            "senha": "Senha",
            "cargo": "Cargo",
            "telefone_func": "Telefone",
            "cpf_func": "CPF",
            "endereco_func": "Endereco",
        }
        self.campos = ["nome_func", "email_func", "senha", "cargo", "telefone_func", "cpf_func", "endereco_func"]
        self.entries = {}

        for campo in self.campos:
            label = self.labels_map[campo]
            row = ctk.CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=label, font=("Arial", 11, "bold"), text_color=COR_BRANCO, width=100, anchor="e").pack(side="left")
            show = "*" if campo == "senha" else ""
            entry = ctk.CTkEntry(row, width=300, corner_radius=8, fg_color="#c2c7cc", text_color="#000000",
                                 border_color=COR_DESTAQUE, border_width=2, show=show)
            entry.pack(side="left", padx=(10, 0))
            if dados and dados.get(campo):
                entry.insert(0, str(dados[campo]))
            self.entries[campo] = entry

        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(pady=15)
        ctk.CTkButton(btn_frame, text="Salvar", fg_color=COR_DOURADO, text_color=COR_BRANCO,
                      hover_color="#d4a857", command=self._salvar).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color="#2c4a5c", command=self.destroy).pack(side="left", padx=10)

    def _salvar(self):
        nome = self.entries["nome_func"].get().strip()
        email = self.entries["email_func"].get().strip()
        senha = self.entries["senha"].get().strip()
        cargo = self.entries["cargo"].get().strip()
        telefone = self.entries["telefone_func"].get().strip() or None
        cpf = self.entries["cpf_func"].get().strip() or None
        endereco = self.entries["endereco_func"].get().strip() or None

        if not nome or not email:
            messagebox.showwarning("Validacao", "Nome e E-mail sao obrigatorios.")
            return

        try:
            conn = _conectar()
            cursor = conn.cursor()
            if self.dados:
                if senha:
                    cursor.execute("UPDATE funcionarios SET nome_func=%s, email_func=%s, senha=%s, cargo=%s, telefone_func=%s, cpf_func=%s, endereco_func=%s WHERE id_func=%s",
                                   (nome, email, senha, cargo, telefone, cpf, endereco, self.dados["id_func"]))
                else:
                    cursor.execute("UPDATE funcionarios SET nome_func=%s, email_func=%s, cargo=%s, telefone_func=%s, cpf_func=%s, endereco_func=%s WHERE id_func=%s",
                                   (nome, email, cargo, telefone, cpf, endereco, self.dados["id_func"]))
            else:
                if not senha:
                    messagebox.showwarning("Validacao", "A senha e obrigatoria para novos funcionarios.")
                    return
                cursor.execute("INSERT INTO funcionarios (nome_func, email_func, senha, cargo, telefone_func, cpf_func, endereco_func) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                               (nome, email, senha, cargo, telefone, cpf, endereco))
            conn.commit()
            cursor.close(); conn.close()
            if self.on_save:
                self.on_save()
            self.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")
