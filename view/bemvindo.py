import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector

def _carregar_icone(caminho, tamanho):
    try:
        img = Image.open(caminho)
        img = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

def contar_servicos_agendados():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="softcar")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'aberto'")
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado[0] if resultado else 0
    except Exception:
        return 0

def contar_servicos_realizados():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="softcar")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'finalizado'")
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado[0] if resultado else 0
    except Exception:
        return 0

def contar_clientes():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="softcar")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes")
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado[0] if resultado else 0
    except Exception:
        return 0

def contar_veiculos():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="softcar")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM carros")
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado[0] if resultado else 0
    except Exception:
        return 0

def calcular_total_recebido():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="softcar")
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ordem_servico WHERE status = 'finalizado'")
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(resultado[0]) if resultado else 0.0
    except Exception:
        return 0.0

def _criar_icone_dourado(icone):
    try:
        pil_img = ImageTk.getimage(icone)
        if pil_img.mode != 'RGBA':
            pil_img = pil_img.convert('RGBA')
        dourado = Image.new('RGBA', pil_img.size, (184, 139, 74, 255))
        result = Image.alpha_composite(pil_img, dourado)
        return ImageTk.PhotoImage(dourado)
    except Exception:
        return None

def _criar_icone_fallback(tamanho, cor, forma="circle"):
    from PIL import ImageDraw
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if forma == "circle":
        draw.ellipse([2, 2, tamanho-2, tamanho-2], fill=cor)
    elif forma == "square":
        draw.rectangle([2, 2, tamanho-2, tamanho-2], fill=cor)
    return ImageTk.PhotoImage(img)

def tela_dashboard(cargo='atendente', root_anterior=None):
    if root_anterior:
        root_anterior.destroy()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.title("Soft Car - Dashboard")
    root.geometry("1200x700")
    root.minsize(800, 500)
    root.resizable(True, True)

    cor_menu = "#2b3e50"
    cor_menu_hover = "#3a536b"
    cor_dourado = "#b88b4a"
    cor_branco = "#ffffff"

    icones_info = [
        ("Cliente",     "assets/cliente.png"),
        ("Serviços",    "assets/servicos.png"),
        ("Funcionários","assets/funcionarios.png"),
        ("Materiais",   "assets/materiais.png"),
        ("Relatórios",  "assets/relatorios.png"),
    ]

    def navegar(opcao):
        if opcao == "Cliente":
            from view.tela_clientes import tela_clientes
            root.after(10, lambda: tela_clientes(root_anterior=root))
        elif opcao == "Serviços":
            from view.tela_servicos import tela_servicos
            root.after(10, lambda: tela_servicos(root_anterior=root))
        elif opcao == "Funcionários":
            from view.lista_funcionarios import tela_lista_funcionarios
            root.after(10, lambda: tela_lista_funcionarios(root_anterior=root))
        elif opcao == "Materiais":
            from view.tela_materiais import tela_materiais
            root.after(10, lambda: tela_materiais(root_anterior=root))
        elif opcao == "Relatórios":
            from view.tela_servico import tela_execucao_servico
            root.after(10, lambda: tela_execucao_servico(root_anterior=root))

    # ---- CONTEÚDO PRINCIPAL (CANVAS COM FUNDO) ----
    canvas = ctk.CTkCanvas(root, highlightthickness=0)
    canvas.pack(side="right", fill="both", expand=True)

    img_path = "assets/dashboard.png"
    if not os.path.exists(img_path):
        print(f"Erro: Arquivo '{img_path}' não encontrado.")
        return

    img_original = Image.open(img_path)
    bg_image_tk = None

    # ---- MENU DO LADO (ITENS NO CANVAS, SEM FUNDO) ----
    botoes_menu = []
    y_pos = 220

    for nome, arquivo in icones_info:
        icone = _carregar_icone(arquivo, 24)
        if icone is None:
            icone = _criar_icone_fallback(24, "#b88b4a", "circle")
        
        ativo = False
        cor_texto = cor_branco

        # Cria imagem e texto como itens do canvas (sem widget Button, sem fundo)
        img_item = canvas.create_image(20, y_pos, image=icone, anchor="nw")
        txt_item = canvas.create_text(50, y_pos + 12, text=nome, font=("Arial", 11, "bold"), fill=cor_texto, anchor="nw")
        
        # Bind de clique no texto e na imagem
        def make_handler(opcao):
            return lambda e: navegar(opcao)
        
        canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
        canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))
        
        # Hover visual
        def on_enter(e, txt=txt_item):
            canvas.itemconfig(txt, fill="#b88b4a")
        def on_leave(e, txt=txt_item, cor=cor_texto):
            canvas.itemconfig(txt, fill=cor)
        
        canvas.tag_bind(img_item, "<Enter>", on_enter)
        canvas.tag_bind(img_item, "<Leave>", on_leave)
        canvas.tag_bind(txt_item, "<Enter>", on_enter)
        canvas.tag_bind(txt_item, "<Leave>", on_leave)
        
        # Guarda referência da imagem para não ser coletada
        canvas.image_refs = getattr(canvas, "image_refs", [])
        canvas.image_refs.append(icone)
        
        # Guarda IDs para reposicionar no resize
        botoes_menu.append((img_item, txt_item, icone))
        y_pos += 50

    # ---- CARDS (TEXTOS) ----
    servicos_agendados = contar_servicos_agendados()
    valor_agendados = canvas.create_text(0, 0, text=str(servicos_agendados), font=("Arial", 54, "bold"), fill=cor_dourado)
    servicos_realizados = contar_servicos_realizados()
    valor_realizados = canvas.create_text(0, 0, text=str(servicos_realizados), font=("Arial", 54, "bold"), fill=cor_dourado)
    clientes_cadastrados = contar_clientes()
    valor_clientes = canvas.create_text(0, 0, text=str(clientes_cadastrados), font=("Arial", 36, "bold"), fill=cor_dourado)
    veiculos_cadastrados = contar_veiculos()
    valor_veiculos = canvas.create_text(0, 0, text=str(veiculos_cadastrados), font=("Arial", 36, "bold"), fill=cor_dourado)
    total_recebido = calcular_total_recebido()
    valor_total = canvas.create_text(0, 0, text=f"R$ {total_recebido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), font=("Arial", 64, "bold"), fill=cor_dourado, anchor="w")
    total_servicos_agendados_label = canvas.create_text(0, 0, text="Serviços agendados", font=("Arial", 13, "bold"), fill=cor_branco, anchor="w")
    total_servicos_realizados_label = canvas.create_text(0, 0, text="Serviços Realizados", font=("Arial", 13, "bold"), fill=cor_branco)
    total_clientes_label = canvas.create_text(0, 0, text="Clientes cadastrados", font=("Arial", 13, "bold"), fill=cor_branco)
    total_veiculos_label = canvas.create_text(0, 0, text="Veiculos cadastrados", font=("Arial", 13, "bold"), fill=cor_branco)
    total_recebido_label = canvas.create_text(0, 0, text="Total recebido", font=("Arial", 13, "bold"), fill=cor_branco, anchor="w")
    bem_vindo_label = canvas.create_text(0, 0, text="SEJA BEM VINDO AO SOFTCAR", font=("Bungee", 16, "bold"), fill=cor_branco, anchor="se")

    def voltar_login():
        root.destroy()
        from main import tela_login
        tela_login()

    btn_sair = ctk.CTkButton(canvas, text="Sair", command=voltar_login, width=80, corner_radius=0, fg_color="#375269", text_color=cor_branco, hover_color="#2c4a5c")
    btn_sair_win = canvas.create_window(30, 0, window=btn_sair, anchor="nw")

    def redimensionar_dashboard(w=None, h=None):
        nonlocal bg_image_tk

        if w is None or h is None:
            return
        if w < 10 or h < 10:
            return

        img_redimensionada = img_original.resize((w, h), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(img_redimensionada)

        canvas.delete("bg")
        canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
        canvas.tag_lower("bg")

        # Reposiciona itens do menu
        y = 220
        for img_item, txt_item, _ in botoes_menu:
            canvas.coords(img_item, 20, y)
            canvas.coords(txt_item, 50, y + 12)
            y += 50

        canvas.coords(valor_agendados, w * 0.315, h * 0.28)
        canvas.coords(valor_realizados, w * 0.562, h * 0.28)
        canvas.coords(valor_clientes, w * 0.812, h * 0.17)
        canvas.coords(valor_veiculos, w * 0.812, h * 0.36)
        canvas.coords(valor_total, w * 0.23, h * 0.68)
        canvas.coords(total_recebido_label, w * 0.23, h * 0.55)
        canvas.coords(total_servicos_agendados_label, w * 0.215, h * 0.15)
        canvas.coords(total_servicos_realizados_label, w * 0.579, h * 0.15)
        canvas.coords(total_clientes_label, w * 0.831, h * 0.11)
        canvas.coords(total_veiculos_label, w * 0.83, h * 0.30)
        canvas.coords(bem_vindo_label, w - 10, h - 20)
        canvas.coords(btn_sair_win, w * 0.02, h - 50)

    def _on_configure(event):
        if event.widget != root:
            return
        redimensionar_dashboard(event.width, event.height)

    root.bind("<Configure>", _on_configure)

    def maximizar():
        root.update_idletasks()
        root.state("zoomed")
        try:
            root.attributes('-zoomed', True)
        except:
            pass
        root.update_idletasks()
        redimensionar_dashboard(root.winfo_width(), root.winfo_height())
    root.after(100, maximizar)

    root.mainloop()

if __name__ == "__main__":
    tela_dashboard()