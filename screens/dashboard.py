import customtkinter as ctk
from PIL import Image, ImageTk
import os
import mysql.connector

COR_FUNDO = "#1e2d3d"
COR_DOURADO = "#b88b4a"
COR_BRANCO = "#ffffff"
COR_DESTAQUE = "#375269"

def _conectar():
    return mysql.connector.connect(host="localhost", user="root", password="", database="softcar")

def _contar_servicos_agendados():
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'aberto'")
        r = cursor.fetchone()
        cursor.close(); conn.close()
        return r[0] if r else 0
    except Exception:
        return 0

def _contar_servicos_realizados():
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'finalizado'")
        r = cursor.fetchone()
        cursor.close(); conn.close()
        return r[0] if r else 0
    except Exception:
        return 0

def _contar_clientes():
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes")
        r = cursor.fetchone()
        cursor.close(); conn.close()
        return r[0] if r else 0
    except Exception:
        return 0

def _contar_veiculos():
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM carros")
        r = cursor.fetchone()
        cursor.close(); conn.close()
        return r[0] if r else 0
    except Exception:
        return 0

def _calcular_total_recebido():
    try:
        conn = _conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ordem_servico WHERE status = 'finalizado'")
        r = cursor.fetchone()
        cursor.close(); conn.close()
        return float(r[0]) if r else 0.0
    except Exception:
        return 0.0


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COR_FUNDO)
        self.app = app

        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "dashboard.png")
        self.img_original = None
        if os.path.exists(img_path):
            self.img_original = Image.open(img_path)

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image_tk = None
        self._bind_events()

    def _bind_events(self):
        self.bind("<Configure>", self._on_configure)

    def on_show(self):
        self.after(50, self._redraw)

    def _on_configure(self, event):
        if event.widget == self:
            self._redraw()

    def _redraw(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return

        self.canvas.delete("all")

        if self.img_original:
            img_resized = self.img_original.resize((w, h), Image.Resampling.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(img_resized)
            self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw", tags="bg")

        self._criar_cards(w, h)

    def _criar_cards(self, w, h):
        c = self.canvas

        sa = _contar_servicos_agendados()
        sr = _contar_servicos_realizados()
        cl = _contar_clientes()
        ve = _contar_veiculos()
        tr = _calcular_total_recebido()

        c.create_text(w * 0.215, h * 0.15, text="Servicos agendados", font=("Arial", 13, "bold"), fill=COR_BRANCO, anchor="w")
        c.create_text(w * 0.315, h * 0.28, text=str(sa), font=("Arial", 54, "bold"), fill=COR_DOURADO)

        c.create_text(w * 0.579, h * 0.15, text="Servicos Realizados", font=("Arial", 13, "bold"), fill=COR_BRANCO)
        c.create_text(w * 0.562, h * 0.28, text=str(sr), font=("Arial", 54, "bold"), fill=COR_DOURADO)

        c.create_text(w * 0.831, h * 0.11, text="Clientes cadastrados", font=("Arial", 13, "bold"), fill=COR_BRANCO)
        c.create_text(w * 0.812, h * 0.17, text=str(cl), font=("Arial", 36, "bold"), fill=COR_DOURADO)

        c.create_text(w * 0.83, h * 0.30, text="Veiculos cadastrados", font=("Arial", 13, "bold"), fill=COR_BRANCO)
        c.create_text(w * 0.812, h * 0.36, text=str(ve), font=("Arial", 36, "bold"), fill=COR_DOURADO)

        c.create_text(w * 0.23, h * 0.55, text="Total recebido", font=("Arial", 13, "bold"), fill=COR_BRANCO, anchor="w")
        valor_fmt = f"R$ {tr:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        c.create_text(w * 0.23, h * 0.68, text=valor_fmt, font=("Arial", 64, "bold"), fill=COR_DOURADO, anchor="w")

        c.create_text(w - 10, h - 20, text="SEJA BEM VINDO AO SOFTCAR", font=("Bungee", 16, "bold"), fill=COR_BRANCO, anchor="se")
