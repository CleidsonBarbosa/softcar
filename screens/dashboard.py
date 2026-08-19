import customtkinter as ctk
from screens.base import BaseScreen
from PIL import Image, ImageDraw
import mysql.connector
import math

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


def _rounded_rect_polygon(x1, y1, x2, y2, r):
    points = []
    steps = 20
    cx, cy = x1 + r, y1 + r
    for i in range(steps + 1):
        angle = math.pi + (math.pi / 2) * i / steps
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    cx, cy = x2 - r, y1 + r
    for i in range(steps + 1):
        angle = -math.pi / 2 + (math.pi / 2) * i / steps
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    cx, cy = x2 - r, y2 - r
    for i in range(steps + 1):
        angle = 0 + (math.pi / 2) * i / steps
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    cx, cy = x1 + r, y2 - r
    for i in range(steps + 1):
        angle = math.pi / 2 + (math.pi / 2) * i / steps
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return points


class DashboardScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app, bg_image="Dashboard.png")
        self.center_frame.place_forget()
        self.nome_usuario = getattr(app, "nome", "")

    def on_show(self):
        super().on_show()
        self.after(80, self._criar_cards)

    def _redraw_bg(self):
        super()._redraw_bg()
        self.after(10, self._criar_cards)

    def _criar_cards(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return
        c = self.canvas

        sa = _contar_servicos_agendados()
        sr = _contar_servicos_realizados()
        cl = _contar_clientes()
        ve = _contar_veiculos()
        tr = _calcular_total_recebido()

        c.delete("cards")

        pad_l = int(w * 0.08)
        pad_r = int(w * 0.05)
        area_w = w - pad_l - pad_r

        card_w1 = int(area_w * 0.42)
        card_w2 = int(area_w * 0.42)
        card_w3 = area_w - card_w1 - card_w2 - 16
        gap = 8

        x1 = pad_l
        x2 = pad_l + card_w1 + gap
        x3 = pad_l + card_w1 + card_w2 + gap * 2

        top_y = int(h * 0.18)
        card_h1 = int(h * 0.30)
        mid_y = top_y + card_h1 + 12
        card_h2 = int(h * 0.22)

        radius = 18

        def draw_rounded_rect(x_a, y_a, x_b, y_b, r, fill, outline_c="", tags=""):
            pts = _rounded_rect_polygon(x_a, y_a, x_b, y_b, r)
            flat = [coord for p in pts for coord in p]
            c.create_polygon(flat, fill=fill, outline="", smooth=False, tags=tags)
            if outline_c:
                c.create_polygon(flat, fill="", outline=outline_c, smooth=False, width=2, tags=tags)

        draw_rounded_rect(x1, top_y, x1 + card_w1, top_y + card_h1, radius, COR_DESTAQUE, COR_BRANCO, "cards")
        draw_rounded_rect(x2, top_y, x2 + card_w2, top_y + card_h1, radius, COR_DESTAQUE, COR_BRANCO, "cards")

        card_h_right = int((card_h1 - 12) / 2)
        draw_rounded_rect(x3, top_y, x3 + card_w3, top_y + card_h_right, radius, COR_DESTAQUE, COR_BRANCO, "cards")
        draw_rounded_rect(x3, top_y + card_h_right + 12, x3 + card_w3, top_y + card_h_right * 2 + 12, radius, COR_DESTAQUE, COR_BRANCO, "cards")

        draw_rounded_rect(pad_l, mid_y, w - pad_r, mid_y + card_h2, radius, COR_DESTAQUE, COR_BRANCO, "cards")

        nome_exib = self.nome_usuario.split()[0] if self.nome_usuario else ""
        c.create_text(w // 2, int(h * 0.05), text=f"Seja Bem Vindo, {nome_exib}",
                       font=("Arial", 22, "bold"), fill=COR_BRANCO, tags="cards")

        f_label = ("Arial", 15, "bold")
        f_num_big = ("Arial", 58, "bold")
        f_num_med = ("Arial", 40, "bold")
        f_valor = ("Arial", 52, "bold")

        cx1 = x1 + card_w1 // 2
        c.create_text(cx1, top_y + 28, text="Servicos agendados", font=f_label, fill=COR_BRANCO, tags="cards")
        c.create_text(cx1, top_y + card_h1 // 2 + 14, text=str(sa), font=f_num_big, fill=COR_DOURADO, tags="cards")

        cx2 = x2 + card_w2 // 2
        c.create_text(cx2, top_y + 28, text="Servicos Realizados", font=f_label, fill=COR_BRANCO, tags="cards")
        c.create_text(cx2, top_y + card_h1 // 2 + 14, text=str(sr), font=f_num_big, fill=COR_DOURADO, tags="cards")

        cx3 = x3 + card_w3 // 2
        c.create_text(cx3, top_y + 20, text="Clientes cadastrados", font=f_label, fill=COR_BRANCO, tags="cards")
        c.create_text(cx3, top_y + card_h_right // 2 + 12, text=str(cl), font=f_num_med, fill=COR_DOURADO, tags="cards")

        ry2 = top_y + card_h_right + 12
        c.create_text(cx3, ry2 + 18, text="Veiculos cadastrados", font=f_label, fill=COR_BRANCO, tags="cards")
        c.create_text(cx3, ry2 + card_h_right // 2 + 10, text=str(ve), font=f_num_med, fill=COR_DOURADO, tags="cards")

        c.create_text(pad_l + 25, mid_y + 28, text="Total recebido", font=f_label, fill=COR_BRANCO, anchor="w", tags="cards")
        valor_fmt = f"R$ {tr:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        c.create_text(pad_l + 25, mid_y + card_h2 // 2 + 14, text=valor_fmt, font=f_valor, fill=COR_DOURADO, anchor="w", tags="cards")
