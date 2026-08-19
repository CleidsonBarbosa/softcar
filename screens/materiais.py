import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from screens.base import BaseScreen
from service.materiais_service import (
    buscar_materiais,
    excluir_material,
    listar_materiais,
    obter_material,
    salvar_material,
)

COR_FUNDO = "#1e2d3d"
COR_DOURADO = "#b88b4a"
COR_BRANCO = "#ffffff"
COR_DESTAQUE = "#375269"
COR_HEADER = "#2c4a5c"

class MateriaisScreen(BaseScreen):
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
        self.entry_busca.bind("<KeyRelease>", lambda e: self._buscar_materiais())

        ctk.CTkButton(header, text="Novo Item +", font=("Arial", 13, "bold"),
                      fg_color=COR_DOURADO, text_color=COR_BRANCO, hover_color="#d4a857",
                      height=38, corner_radius=10,
                      command=self._abrir_formulario).pack(side="right", padx=5)

        container = ctk.CTkFrame(ov, fg_color=COR_DESTAQUE, corner_radius=12)
        container.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        colunas = ("id_produto", "tipo", "quantidade")
        self.tree = ttk.Treeview(container, columns=colunas, show="headings", selectmode="browse", height=18)
        self.tree.heading("id_produto", text="ID", anchor="center")
        self.tree.heading("tipo", text="Tipo", anchor="w")
        self.tree.heading("quantidade", text="Quantidade", anchor="center")
        self.tree.column("id_produto", width=60, minwidth=60, stretch=False, anchor="center")
        self.tree.column("tipo", width=500, minwidth=250, stretch=True, anchor="w")
        self.tree.column("quantidade", width=160, minwidth=120, stretch=False, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self.tree.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)

        self.tree.bind("<Double-1>", lambda e: self._editar_material())

        btn_frame = ctk.CTkFrame(ov, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(0, 12))
        ctk.CTkButton(btn_frame, text="Editar", font=("Arial", 13, "bold"), fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color=COR_HEADER, height=38, corner_radius=10, width=120,
                      command=self._editar_material).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Excluir", font=("Arial", 13, "bold"), fg_color="#8b0000", text_color=COR_BRANCO,
                      hover_color="#a52a2a", height=38, corner_radius=10, width=120,
                      command=self._excluir_material).pack(side="left", padx=5)

    def on_show(self):
        super().on_show()
        self._carregar_materiais()

    def _carregar_materiais(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            for row in listar_materiais():
                self.tree.insert("", "end", values=row)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar estoque:\n{e}")

    def _buscar_materiais(self):
        termo = self.entry_busca.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            for row in buscar_materiais(termo):
                self.tree.insert("", "end", values=row)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")

    def _editar_material(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione um item na lista.")
            return
        vals = self.tree.item(sel[0])["values"]
        id_prod = vals[0]
        try:
            dados = obter_material(id_prod)
            if dados:
                MaterialForm(self.app.root, dados=dados, on_save=self._carregar_materiais)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")

    def _excluir_material(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione um item na lista.")
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este item?"):
            return
        id_prod = self.tree.item(sel[0])["values"][0]
        try:
            excluir_material(id_prod)
            self._carregar_materiais()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

    def _abrir_formulario(self, dados=None):
        MaterialForm(self.app.root, dados=dados, on_save=self._carregar_materiais)


class MaterialForm(ctk.CTkToplevel):
    def __init__(self, parent, dados=None, on_save=None):
        super().__init__(parent)
        self.dados = dados
        self.on_save = on_save
        self.title("Editar Item" if dados else "Novo Item")
        self.configure(fg_color="#1a2735")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.geometry("650x380")
        self.after(100, lambda: self._center(parent))

        main = ctk.CTkFrame(self, fg_color="#1a2735", corner_radius=15)
        main.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(main, text="Dados do Item", font=("Arial", 22, "bold"), text_color=COR_DOURADO).pack(pady=(20, 25))

        self.entries = {}

        for campo, label in [("tipo", "Tipo"), ("quantidade", "Quantidade")]:
            row = ctk.CTkFrame(main, fg_color="transparent")
            row.pack(fill="x", pady=8, padx=60)
            ctk.CTkLabel(row, text=label, font=("Arial", 14, "bold"), text_color=COR_BRANCO, width=140, anchor="e").pack(side="left")
            entry = ctk.CTkEntry(row, width=380, height=42, corner_radius=10, fg_color="#c2c7cc", text_color="#000000",
                                 border_color=COR_DESTAQUE, border_width=2, font=("Arial", 14))
            entry.pack(side="left", padx=(15, 0))
            if dados and dados.get(campo) is not None:
                entry.insert(0, str(dados[campo]))
            self.entries[campo] = entry

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=25)
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
        x = (pw - 650) // 2
        y = (ph - 380) // 2
        self.geometry(f"+{x}+{y}")

    def _salvar(self):
        tipo = self.entries["tipo"].get().strip()
        qtd_str = self.entries["quantidade"].get().strip()

        try:
            id_produto = self.dados["id_produto"] if self.dados else None
            salvar_material({"tipo": tipo, "quantidade": qtd_str}, id_produto)
            if self.on_save:
                self.on_save()
            self.destroy()
        except ValueError as e:
            messagebox.showwarning("Validacao", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")
