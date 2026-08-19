import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from screens.base import BaseScreen
from service.funcionarios_service import (
    buscar_funcionarios,
    excluir_funcionario,
    listar_funcionarios,
    obter_funcionario,
    salvar_funcionario,
)

COR_FUNDO = "#1e2d3d"
COR_DOURADO = "#b88b4a"
COR_BRANCO = "#ffffff"
COR_DESTAQUE = "#375269"
COR_HEADER = "#2c4a5c"

class FuncionariosScreen(BaseScreen):
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
                        fieldbackground=COR_DESTAQUE, rowheight=36, borderwidth=0,
                        font=("Arial", 12))
        style.configure("Treeview.Heading", background=COR_HEADER, foreground=COR_BRANCO, borderwidth=0,
                        font=("Arial", 12, "bold"))
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

        header = ctk.CTkFrame(ov, fg_color="transparent", height=48)
        header.pack(fill="x", padx=30, pady=(15, 8))
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Pesquisar", font=("Arial", 14, "bold"), text_color=COR_BRANCO).pack(side="left", padx=(0, 10))
        self.entry_busca = ctk.CTkEntry(header, width=320, height=38, fg_color=COR_DESTAQUE, text_color="#ffffff",
                                        border_width=1, font=("Arial", 13), corner_radius=10)
        self.entry_busca.pack(side="left", padx=5, ipady=2)
        self.entry_busca.bind("<KeyRelease>", lambda e: self._buscar_funcionarios())

        ctk.CTkButton(header, text="Novo Funcionario +", font=("Arial", 13, "bold"),
                      fg_color=COR_DOURADO, text_color=COR_BRANCO, hover_color="#d4a857",
                      height=38, corner_radius=10,
                      command=self._abrir_formulario).pack(side="right", padx=5)

        container = ctk.CTkFrame(ov, fg_color=COR_DESTAQUE, corner_radius=12)
        container.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        colunas = ("id_func", "nome_func", "email_func", "cargo", "telefone_func")
        self.tree = ttk.Treeview(container, columns=colunas, show="headings", selectmode="browse", height=18)
        self.tree.heading("id_func", text="ID", anchor="center")
        self.tree.heading("nome_func", text="Nome", anchor="w")
        self.tree.heading("email_func", text="E-mail", anchor="w")
        self.tree.heading("cargo", text="Cargo", anchor="center")
        self.tree.heading("telefone_func", text="Telefone", anchor="center")
        self.tree.column("id_func", width=50, minwidth=50, stretch=False, anchor="center")
        self.tree.column("nome_func", width=220, minwidth=140, stretch=True, anchor="w")
        self.tree.column("email_func", width=240, minwidth=140, stretch=True, anchor="w")
        self.tree.column("cargo", width=130, minwidth=100, stretch=False, anchor="center")
        self.tree.column("telefone_func", width=140, minwidth=110, stretch=False, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self.tree.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)

        self.tree.bind("<Double-1>", lambda e: self._editar_funcionario())

        btn_frame = ctk.CTkFrame(ov, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(0, 12))
        ctk.CTkButton(btn_frame, text="Editar", font=("Arial", 13, "bold"), fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color=COR_HEADER, height=38, corner_radius=10, width=120,
                      command=self._editar_funcionario).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Excluir", font=("Arial", 13, "bold"), fg_color="#8b0000", text_color=COR_BRANCO,
                      hover_color="#a52a2a", height=38, corner_radius=10, width=120,
                      command=self._excluir_funcionario).pack(side="left", padx=5)

    def on_show(self):
        super().on_show()
        self._carregar_funcionarios()

    def _carregar_funcionarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            for row in listar_funcionarios():
                self.tree.insert("", "end", values=row)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar funcionarios:\n{e}")

    def _buscar_funcionarios(self):
        termo = self.entry_busca.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            for row in buscar_funcionarios(termo):
                self.tree.insert("", "end", values=row)
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
            dados = obter_funcionario(id_func)
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
            excluir_funcionario(id_func)
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
        self.configure(fg_color="#1a2735")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.geometry("680x600")
        self.after(100, lambda: self._center(parent))

        main = ctk.CTkFrame(self, fg_color="#1a2735", corner_radius=15)
        main.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(main, text="Dados do Funcionario", font=("Arial", 22, "bold"), text_color=COR_DOURADO).pack(pady=(15, 18))

        self.labels_map = {
            "nome_func": "Nome", "email_func": "E-mail", "senha": "Senha",
            "cargo": "Cargo", "telefone_func": "Telefone",
            "cpf_func": "CPF", "endereco_func": "Endereco",
        }
        self.campos = ["nome_func", "email_func", "senha", "cargo", "telefone_func", "cpf_func", "endereco_func"]
        self.entries = {}

        for campo in self.campos:
            label = self.labels_map[campo]
            row = ctk.CTkFrame(main, fg_color="transparent")
            row.pack(fill="x", pady=3, padx=50)
            ctk.CTkLabel(row, text=label, font=("Arial", 13, "bold"), text_color=COR_BRANCO, width=120, anchor="e").pack(side="left")
            show = "*" if campo == "senha" else ""
            entry = ctk.CTkEntry(row, width=380, height=38, corner_radius=10, fg_color="#c2c7cc", text_color="#000000",
                                 border_color=COR_DESTAQUE, border_width=2, show=show, font=("Arial", 13))
            entry.pack(side="left", padx=(15, 0))
            if dados and dados.get(campo):
                entry.insert(0, str(dados[campo]))
            self.entries[campo] = entry

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=18)
        ctk.CTkButton(btn_frame, text="Salvar", font=("Arial", 14, "bold"), width=160, height=42,
                      fg_color=COR_DOURADO, text_color=COR_BRANCO,
                      hover_color="#d4a857", corner_radius=10, command=self._salvar).pack(side="left", padx=12)
        ctk.CTkButton(btn_frame, text="Cancelar", font=("Arial", 14, "bold"), width=160, height=42,
                      fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color="#2c4a5c", corner_radius=10, command=self.destroy).pack(side="left", padx=12)

    def _center(self, parent):
        parent.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = (pw - 680) // 2
        y = (ph - 600) // 2
        self.geometry(f"+{x}+{y}")

    def _salvar(self):
        nome = self.entries["nome_func"].get().strip()
        email = self.entries["email_func"].get().strip()
        senha = self.entries["senha"].get().strip()
        cargo = self.entries["cargo"].get().strip()
        telefone = self.entries["telefone_func"].get().strip() or None
        cpf = self.entries["cpf_func"].get().strip() or None
        endereco = self.entries["endereco_func"].get().strip() or None

        try:
            dados = {
                "nome_func": nome,
                "email_func": email,
                "senha": senha,
                "cargo": cargo,
                "telefone_func": telefone,
                "cpf_func": cpf,
                "endereco_func": endereco,
            }
            id_func = self.dados["id_func"] if self.dados else None
            salvar_funcionario(dados, id_func)
            if self.on_save:
                self.on_save()
            self.destroy()
        except ValueError as e:
            messagebox.showwarning("Validacao", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")
