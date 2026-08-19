import customtkinter as ctk
from PIL import Image, ImageDraw
import os

COR_FUNDO = "#1e2d3d"
COR_SIDEBAR = "#2b3e50"
COR_HOVER = "#3a536b"
COR_DOURADO = "#b88b4a"
COR_BRANCO = "#ffffff"
COR_CINZA = "#777777"
COR_DESTAQUE = "#375269"

ICONES_INFO = [
    ("Clientes",        "assets/cliente.png"),
    ("Servicos",        "assets/servicos.png"),
    ("Funcionarios",    "assets/funcionarios.png"),
    ("Materiais",       "assets/materiais.png"),
    ("Ordem de Servico","assets/relatorios.png"),
]


class App:
    def __init__(self, root, cargo="atendente", nome=""):
        self.root = root
        self.cargo = cargo
        self.nome = nome
        self.current_screen = None
        self.screen_refs = {}
        self.sidebar_btns = []
        self._pil_refs = []

        for w in self.root.winfo_children():
            w.destroy()

        self.root.unbind("<Return>")
        self.root.unbind("<Configure>")

        self.root.title("Soft Car")
        self.root.configure(fg_color=COR_FUNDO)
        self.root.minsize(800, 500)
        self.root.resizable(True, True)

        self.root.bind("<Configure>", self._on_resize)

        self._criar_sidebar()
        self._criar_content_area()

        self.root.after(100, self._maximizar)
        self.show_screen("Dashboard")

    def _maximizar(self):
        self.root.update_idletasks()
        self.root.state("zoomed")
        try:
            self.root.attributes("-zoomed", True)
        except Exception:
            pass

    def _make_ctk_icon(self, caminho, tamanho):
        try:
            pil_img = Image.open(caminho).copy()
            self._pil_refs.append(pil_img)
            return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(tamanho, tamanho))
        except Exception:
            return self._make_fallback_icon(tamanho, COR_DOURADO)

    def _make_fallback_icon(self, tamanho, cor):
        img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([2, 2, tamanho - 2, tamanho - 2], fill=cor)
        self._pil_refs.append(img)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(tamanho, tamanho))

    def _criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.root, fg_color=COR_SIDEBAR, corner_radius=0, width=180)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_pil = Image.open("assets/img_softcar.png").copy()
        self._pil_refs.append(logo_pil)
        logo_icon = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(140, 90))

        btn_dashboard = ctk.CTkButton(
            self.sidebar,
            text="",
            image=logo_icon,
            fg_color="transparent",
            hover_color=COR_HOVER,
            height=90,
            corner_radius=6,
            command=lambda: self.show_screen("Dashboard"),
        )
        btn_dashboard.pack(fill="x", padx=8, pady=(10, 2))
        self.sidebar_btns.append(("Dashboard", btn_dashboard))

        ctk.CTkLabel(self.sidebar, text="SOFTCAR", font=("Bungee", 14, "bold"),
                      text_color=COR_DOURADO).pack(pady=(0, 12), padx=10)

        for nome, arquivo in ICONES_INFO:
            icone = self._make_ctk_icon(arquivo, 22)

            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {nome}",
                image=icone,
                anchor="w",
                fg_color="transparent",
                text_color=COR_BRANCO,
                hover_color=COR_HOVER,
                font=("Arial", 12, "bold"),
                height=40,
                corner_radius=6,
                command=lambda n=nome: self.show_screen(n),
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.sidebar_btns.append((nome, btn))

        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        ctk.CTkButton(
            self.sidebar,
            text="Sair",
            fg_color=COR_DESTAQUE,
            text_color=COR_BRANCO,
            hover_color="#2c4a5c",
            height=36,
            corner_radius=6,
            command=self._voltar_para_login,
        ).pack(fill="x", padx=8, pady=(10, 15))

    def _voltar_para_login(self):
        from main import tela_login
        self.root.after(200, lambda: tela_login(self.root))

    def _criar_content_area(self):
        self.content = ctk.CTkFrame(self.root, fg_color=COR_FUNDO, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

    def _highlight_active(self, nome):
        for n, btn in self.sidebar_btns:
            btn.configure(fg_color=COR_HOVER if n == nome else "transparent")

    def show_screen(self, nome):
        if self.current_screen is not None:
            self.current_screen.pack_forget()

        screen = self._get_screen(nome)
        self.current_screen = screen
        self._highlight_active(nome)
        screen.pack(in_=self.content, fill="both", expand=True)
        if hasattr(screen, "on_show"):
            screen.on_show()

    def _get_screen(self, nome):
        if nome not in self.screen_refs:
            cls = self._resolve_screen_cls(nome)
            self.screen_refs[nome] = cls(self.content, self)
        return self.screen_refs[nome]

    def _resolve_screen_cls(self, nome):
        from screens.dashboard import DashboardScreen
        from screens.clientes import ClientesScreen
        from screens.servicos import ServicosScreen
        from screens.funcionarios import FuncionariosScreen
        from screens.materiais import MateriaisScreen
        from screens.servico_execucao import ServicoExecucaoScreen

        mapa = {
            "Dashboard": DashboardScreen,
            "Clientes": ClientesScreen,
            "Servicos": ServicosScreen,
            "Funcionarios": FuncionariosScreen,
            "Materiais": MateriaisScreen,
            "Ordem de Servico": ServicoExecucaoScreen,
        }
        return mapa.get(nome, DashboardScreen)

    def _on_resize(self, event):
        pass
