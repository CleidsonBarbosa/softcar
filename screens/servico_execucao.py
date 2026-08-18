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


class ServicoExecucaoScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COR_FUNDO)
        self.app = app
        self._configurar_treeview_style()
        self._criar_widgets()
        self._carregar_ordens()

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
        self.entry_busca.bind("<KeyRelease>", lambda e: self._buscar_ordens())

        container = ctk.CTkFrame(self, fg_color=COR_DESTAQUE, corner_radius=0)
        container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        colunas = ("id_ordem", "id_cliente", "total", "status", "data_hora")
        self.tree = ttk.Treeview(container, columns=colunas, show="headings", selectmode="browse")
        self.tree.heading("id_ordem", text="Ordem")
        self.tree.heading("id_cliente", text="Cliente")
        self.tree.heading("total", text="Total")
        self.tree.heading("status", text="Status")
        self.tree.heading("data_hora", text="Data")
        self.tree.column("id_ordem", width=70, anchor="center")
        self.tree.column("id_cliente", width=70, anchor="center")
        self.tree.column("total", width=120, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("data_hora", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<Double-1>", lambda e: self._finalizar_ordem())

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        ctk.CTkButton(btn_frame, text="Finalizar Ordem", fg_color="#006400", text_color=COR_BRANCO,
                      hover_color="#228b22", command=self._finalizar_ordem).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Excluir Ordem", fg_color="#8b0000", text_color=COR_BRANCO,
                      hover_color="#a52a2a", command=self._excluir_ordem).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Ver Itens", fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color=COR_HEADER, command=self._ver_itens).pack(side="left", padx=5)

    def on_show(self):
        self._carregar_ordens()

    def _carregar_ordens(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_ordem, id_cliente, total, status, data_hora FROM ordem_servico ORDER BY id_ordem DESC")
            for row in cursor.fetchall():
                total = f"R$ {row[2]:.2f}" if row[2] else "-"
                status = row[3] or ""
                data = str(row[4])[:10] if row[4] else ""
                self.tree.insert("", "end", values=(row[0], row[1], total, status, data))
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar ordens:\n{e}")

    def _buscar_ordens(self):
        termo = self.entry_busca.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = _conectar()
            cursor = conn.cursor()
            if termo:
                cursor.execute("SELECT id_ordem, id_cliente, total, status, data_hora FROM ordem_servico WHERE status LIKE %s OR id_ordem LIKE %s ORDER BY id_ordem DESC",
                               (f"%{termo}%", f"%{termo}%"))
            else:
                cursor.execute("SELECT id_ordem, id_cliente, total, status, data_hora FROM ordem_servico ORDER BY id_ordem DESC")
            for row in cursor.fetchall():
                total = f"R$ {row[2]:.2f}" if row[2] else "-"
                status = row[3] or ""
                data = str(row[4])[:10] if row[4] else ""
                self.tree.insert("", "end", values=(row[0], row[1], total, status, data))
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")

    def _finalizar_ordem(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione uma ordem de servico.")
            return
        vals = self.tree.item(sel[0])["values"]
        id_ordem = vals[0]
        status = vals[3]
        if status == "finalizado":
            messagebox.showinfo("Info", "Esta ordem ja foi finalizada.")
            return
        if not messagebox.askyesno("Confirmar", f"Finalizar ordem #{id_ordem}?"):
            return
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE ordem_servico SET status = 'finalizado' WHERE id_ordem = %s", (id_ordem,))
            conn.commit()
            cursor.close(); conn.close()
            self._carregar_ordens()
            messagebox.showinfo("Sucesso", f"Ordem #{id_ordem} finalizada!")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao finalizar:\n{e}")

    def _excluir_ordem(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione uma ordem de servico.")
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta ordem?"):
            return
        id_ordem = self.tree.item(sel[0])["values"][0]
        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ordem_servico_itens WHERE id_ordem = %s", (id_ordem,))
            cursor.execute("DELETE FROM ordem_servico WHERE id_ordem = %s", (id_ordem,))
            conn.commit()
            cursor.close(); conn.close()
            self._carregar_ordens()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

    def _ver_itens(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecao", "Selecione uma ordem de servico.")
            return
        vals = self.tree.item(sel[0])["values"]
        id_ordem = vals[0]
        ItensOrdemModal(self.app.root, id_ordem)


class ItensOrdemModal(ctk.CTkToplevel):
    def __init__(self, parent, id_ordem):
        super().__init__(parent)
        self.id_ordem = id_ordem
        self.title(f"Itens da Ordem #{id_ordem}")
        self.geometry("700x450")
        self.configure(fg_color=COR_FUNDO)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.after(100, lambda: self.state("zoomed"))

        container = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(container, text=f"Itens da Ordem de Servico #{id_ordem}",
                     font=("Arial", 14, "bold"), text_color=COR_DOURADO).pack(pady=(0, 15))

        frame = ctk.CTkFrame(container, fg_color=COR_DESTAQUE, corner_radius=0)
        frame.pack(fill="both", expand=True)

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

        colunas = ("id_item", "id_servico", "nome_servico", "preco")
        tree = ttk.Treeview(frame, columns=colunas, show="headings", selectmode="browse")
        tree.heading("id_item", text="Item")
        tree.heading("id_servico", text="Servico")
        tree.heading("nome_servico", text="Nome")
        tree.heading("preco", text="Preco")
        tree.column("id_item", width=60, anchor="center")
        tree.column("id_servico", width=60, anchor="center")
        tree.column("nome_servico", width=300)
        tree.column("preco", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        try:
            conn = _conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT osi.id_item, osi.id_servico, s.nome_servico, osi.preco
                FROM ordem_servico_itens osi
                LEFT JOIN servicos s ON s.id_servico = osi.id_servico
                WHERE osi.id_ordem = %s
            """, (id_ordem,))
            for row in cursor.fetchall():
                preco = f"R$ {row[3]:.2f}" if row[3] else "-"
                tree.insert("", "end", values=(row[0], row[1], row[2], preco))
            cursor.close(); conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar itens:\n{e}")

        ctk.CTkButton(container, text="Fechar", fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                      hover_color=COR_HEADER, command=self.destroy).pack(pady=(15, 0))
