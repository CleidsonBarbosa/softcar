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

def _criar_icone_fallback(tamanho, cor, formato):
    from PIL import ImageDraw
    import math
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margem = tamanho // 5
    if formato == "circle":
        draw.ellipse([margem, margem, tamanho - margem, tamanho - margem], fill=cor)
    elif formato == "square":
        draw.rectangle([margem, margem, tamanho - margem, tamanho - margem], fill=cor)
    elif formato == "triangle":
        draw.polygon([(tamanho//2, margem), (margem, tamanho - margem), (tamanho - margem, tamanho - margem)], fill=cor)
    elif formato == "diamond":
        draw.polygon([(tamanho//2, margem), (tamanho - margem, tamanho//2), (tamanho//2, tamanho - margem), (margem, tamanho//2)], fill=cor)
    elif formato == "hexagon":
        cx, cy = tamanho//2, tamanho//2
        r = tamanho//2 - margem
        pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in [math.radians(60*i+30) for i in range(6)]]
        draw.polygon(pts, fill=cor)
    return ImageTk.PhotoImage(img)

def tela_dashboard():
    root = tk.Tk()
    root.title("Soft Car - Dashboard")
    root.geometry("1000x630")
    root.minsize(800, 500)
    root.resizable(True, True)

    cor_menu = "#2b3e50"
    cor_menu_hover = "#3a536b"
    cor_dourado = "#b88b4a"

    icones_info = [
        ("Cliente",     "assets/cliente.svg",      "#4CAF50", "circle"),
        ("Serviços",    "assets/Car Sale.svg",           "#2196F3", "square"),
        ("Funcionários","assets/Supplier.svg",           "#FF9800", "triangle"),
        ("Materiais",   "assets/Shopping Cart.svg",      "#9C27B0", "diamond"),
        ("Relatórios",  "assets/Business Report.svg",    "#F44336", "hexagon"),
    ]

    def acao_menu(opcao):
        if opcao == "Cliente":
            from view.lista_clientes import tela_lista_clientes
            tela_lista_clientes()
        elif opcao == "Funcionários":
            from view.lista_funcionarios import tela_lista_funcionarios
            tela_lista_funcionarios()
        else:
            messagebox.showinfo("Soft Car", f"Você clicou na opção: {opcao}")

    # ---- MENU LATERAL (FRAME) ----
    menu_frame = tk.Frame(root, bg=cor_menu, width=200)
    menu_frame.pack(side="left", fill="y")
    menu_frame.pack_propagate(False)

    # Logo no topo do menu
    logo_path = "assets/sofcar.png"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((140, 140), Image.Resampling.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(menu_frame, image=logo_tk, bg=cor_menu)
        logo_label.image = logo_tk
        logo_label.pack(pady=(15, 20))

    for nome, arquivo, cor, forma in icones_info:
        icone = _carregar_icone(arquivo, 24)
        if icone is None:
            icone = _criar_icone_fallback(24, cor, forma)
        btn = tk.Button(
            menu_frame,
            image=icone,
            text=f"  {nome}",
            compound=tk.LEFT,
            font=("Arial", 11, "bold"),
            fg="white",
            bg=cor_menu,
            activebackground=cor_menu_hover,
            activeforeground="white",
            bd=0,
            anchor="w",
            padx=15,
            pady=12,
            cursor="hand2",
            command=lambda o=nome: acao_menu(o)
        )
        btn.image = icone
        btn.pack(fill="x")
        btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=cor_menu_hover))
        btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=cor_menu))

    # ---- CONTEÚDO PRINCIPAL (CANVAS COM FUNDO) ----
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(side="right", fill="both", expand=True)

    img_path = "assets/dashboard.png"
    if not os.path.exists(img_path):
        print(f"Erro: Arquivo '{img_path}' não encontrado.")
        return

    img_original = Image.open(img_path)
    bg_image_tk = None

    # ---- CARDS (TEXTOS) ----
    valor_agendados = canvas.create_text(0, 0, text="20", font=("Arial", 54, "bold"), fill=cor_dourado)
    valor_realizados = canvas.create_text(0, 0, text="31", font=("Arial", 54, "bold"), fill=cor_dourado)
    valor_clientes = canvas.create_text(0, 0, text="352", font=("Arial", 36, "bold"), fill=cor_dourado)
    valor_veiculos = canvas.create_text(0, 0, text="426", font=("Arial", 36, "bold"), fill=cor_dourado)
    valor_total = canvas.create_text(0, 0, text="R$ 863,00", font=("Arial", 64, "bold"), fill=cor_dourado, anchor="w")

    # ---- REDIMENSIONAMENTO ----
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

        canvas.coords(valor_agendados, event.width * 0.315, event.height * 0.28)
        canvas.coords(valor_realizados, event.width * 0.562, event.height * 0.28)
        canvas.coords(valor_clientes, event.width * 0.812, event.height * 0.17)
        canvas.coords(valor_veiculos, event.width * 0.812, event.height * 0.36)
        canvas.coords(valor_total, event.width * 0.23, event.height * 0.68)

    root.bind("<Configure>", redimensionar_dashboard)
    root.mainloop()

if __name__ == "__main__":
    tela_dashboard()