import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def _carregar_icone(caminho, tamanho):
    try:
        img = Image.open(caminho)
        img = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

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

def tela_dashboard():
    root = tk.Tk()
    root.title("Soft Car - Dashboard")
    root.geometry("1000x630")
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

    def acao_menu(opcao):
        if opcao == "Cliente":
            from view.tela_clientes import tela_clientes
            tela_clientes()
        elif opcao == "Funcionários":
            from view.lista_funcionarios import tela_lista_funcionarios
            tela_lista_funcionarios()
        else:
            messagebox.showinfo("Soft Car", f"Você clicou na opção: {opcao}")

    # ---- CONTEÚDO PRINCIPAL (CANVAS COM FUNDO) ----
    canvas = tk.Canvas(root, highlightthickness=0)
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
        
        # Cria imagem e texto como itens do canvas (sem widget Button, sem fundo)
        img_item = canvas.create_image(20, y_pos, image=icone, anchor="nw")
        txt_item = canvas.create_text(50, y_pos + 12, text=nome, font=("Arial", 11, "bold"), fill="white", anchor="nw")
        
        # Bind de clique no texto e na imagem
        def make_handler(opcao):
            return lambda e: acao_menu(opcao)
        
        canvas.tag_bind(img_item, "<Button-1>", make_handler(nome))
        canvas.tag_bind(txt_item, "<Button-1>", make_handler(nome))
        
        # Hover visual
        def on_enter(e, txt=txt_item):
            canvas.itemconfig(txt, fill="#b88b4a")
        def on_leave(e, txt=txt_item):
            canvas.itemconfig(txt, fill="white")
        
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
    valor_agendados = canvas.create_text(0, 0, text="20", font=("Arial", 54, "bold"), fill=cor_dourado)
    valor_realizados = canvas.create_text(0, 0, text="31", font=("Arial", 54, "bold"), fill=cor_dourado)
    valor_clientes = canvas.create_text(0, 0, text="352", font=("Arial", 36, "bold"), fill=cor_dourado)
    valor_veiculos = canvas.create_text(0, 0, text="426", font=("Arial", 36, "bold"), fill=cor_dourado)
    valor_total = canvas.create_text(0, 0, text="R$ 863,00", font=("Arial", 64, "bold"), fill=cor_dourado, anchor="w")
    total_servicos_agendados_label = canvas.create_text(0, 0, text="Serviços agendados", font=("Arial", 13, "bold"), fill=cor_branco, anchor="w")
    total_servicos_realizados_label = canvas.create_text(0, 0, text="Serviços Realizados", font=("Arial", 13, "bold"), fill=cor_branco)
    total_clientes_label = canvas.create_text(0, 0, text="Clientes cadastrados", font=("Arial", 13, "bold"), fill=cor_branco)
    total_veiculos_label = canvas.create_text(0, 0, text="Veiculos cadastrados", font=("Arial", 13, "bold"), fill=cor_branco)
    total_recebido_label = canvas.create_text(0, 0, text="Total recebido", font=("Arial", 13, "bold"), fill=cor_branco, anchor="w")
    bem_vindo_label = canvas.create_text(0, 0, text="SEJA BEM VINDO AO SOFTCAR", font=("Bungee", 16, "bold"), fill=cor_branco, anchor="se")

    bg_image_tk = None

    def redimensionar_dashboard(event):
        nonlocal bg_image_tk

        if event.widget != root:
            return
        if event.width < 10 or event.height < 10:
            return

        img_redimensionada = img_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
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

        canvas.coords(valor_agendados, event.width * 0.315, event.height * 0.28)
        canvas.coords(valor_realizados, event.width * 0.562, event.height * 0.28)
        canvas.coords(valor_clientes, event.width * 0.812, event.height * 0.17)
        canvas.coords(valor_veiculos, event.width * 0.812, event.height * 0.36)
        canvas.coords(valor_total, event.width * 0.23, event.height * 0.68)
        canvas.coords(total_recebido_label, event.width * 0.23, event.height * 0.55)
        canvas.coords(total_servicos_agendados_label, event.width * 0.215, event.height * 0.15)
        canvas.coords(total_servicos_realizados_label, event.width * 0.579, event.height * 0.15)
        canvas.coords(total_clientes_label, event.width * 0.831, event.height * 0.11)
        canvas.coords(total_veiculos_label, event.width * 0.83, event.height * 0.3)
        canvas.coords(bem_vindo_label, event.width - 10, event.height - 20)

    canvas.pack(side="right", fill="both", expand=True)
    root.bind("<Configure>", redimensionar_dashboard)
    root.mainloop()

if __name__ == "__main__":
    tela_dashboard()