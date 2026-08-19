import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import mysql.connector


COR_FUNDO = "#1e2d3d"
COR_DOURADO = "#b88b4a"
COR_BRANCO = "#ffffff"
COR_DESTAQUE = "#375269"


def verificar_login(root, entry_login, entry_senha):
    email = entry_login.get().strip()
    senha = entry_senha.get().strip()

    if email == "" or senha == "":
        messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
        return

    try:
        conexao = mysql.connector.connect(
            host="localhost", user="root", password="", database="softcar"
        )
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE email_func = %s AND senha = %s", (email, senha))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()

        if resultado:
            cargo = resultado[5]
            nome = resultado[1]
            from app import App
            App(root, cargo=cargo, nome=nome)
        else:
            messagebox.showerror("Erro", "Usuario ou senha incorretos.")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro de Conexao", f"Falha ao conectar ao banco:\n{erro}")


def _make_eye_icon(size, open_eye=True):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    rx, ry = size // 2 - 2, size // 3
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline="white", width=2)
    pr = size // 6
    draw.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill="white")
    if not open_eye:
        draw.line([2, 2, size - 2, size - 2], fill="white", width=2)
    return img


def tela_login():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.title("Soft Car - Login")
    root.geometry("1200x800")
    root.minsize(900, 600)
    root.resizable(True, True)

    root.after(100, lambda: root.state("zoomed"))

    img_bg_path = "assets/Login.png"
    bg_original = None
    if os.path.exists(img_bg_path):
        bg_original = Image.open(img_bg_path).copy()

    canvas = ctk.CTkCanvas(root, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)

    bg_image_tk = None

    COR_TEXTO = "#000000"
    COR_INPUT_FG = "#2a2a2a"
    COR_INPUT_BORDER = "#000000"

    entry_font = ctk.CTkFont(family="Arial", size=14, weight="bold")

    entry_login = ctk.CTkEntry(root, font=entry_font, border_width=2, corner_radius=25,
                               placeholder_text="", fg_color=COR_INPUT_FG, text_color="#ffffff",
                               border_color=COR_INPUT_BORDER, width=350, height=45)
    entry_senha = ctk.CTkEntry(root, font=entry_font, border_width=2, corner_radius=25,
                               placeholder_text="", show="*", fg_color=COR_INPUT_FG, text_color="#ffffff",
                               border_color=COR_INPUT_BORDER, width=350, height=45)

    canvas_login_id = canvas.create_window(0, 0, window=entry_login, anchor="center")
    canvas_senha_id = canvas.create_window(0, 0, window=entry_senha, anchor="center")

    eye_open_pil = _make_eye_icon(20, open_eye=True)
    eye_closed_pil = _make_eye_icon(20, open_eye=False)
    eye_open_tk = ctk.CTkImage(light_image=eye_open_pil, dark_image=eye_open_pil, size=(20, 20))
    eye_closed_tk = ctk.CTkImage(light_image=eye_closed_pil, dark_image=eye_closed_pil, size=(20, 20))

    btn_senha_var = tk.BooleanVar(value=False)

    def toggle_senha():
        if btn_senha_var.get():
            entry_senha.configure(show="")
            btn_visualizar.configure(image=eye_closed_tk)
        else:
            entry_senha.configure(show="*")
            btn_visualizar.configure(image=eye_open_tk)
        btn_senha_var.set(not btn_senha_var.get())

    btn_visualizar = ctk.CTkButton(root, text="", image=eye_open_tk,
                                   fg_color="transparent", text_color=COR_TEXTO,
                                   hover_color="#cccccc", width=30, height=30, corner_radius=8,
                                   command=toggle_senha)
    canvas_btn_senha_id = canvas.create_window(0, 0, window=btn_visualizar, anchor="center")

    label_titulo = canvas.create_text(0, 0, text="Login", font=("Arial", 36, "bold"),
                                      fill=COR_TEXTO, anchor="center")

    label_usuario = canvas.create_text(0, 0, text="Email  👤", font=("Arial", 14, "bold"),
                                       fill=COR_TEXTO, anchor="center")
    label_senha = canvas.create_text(0, 0, text="Senha", font=("Arial", 14, "bold"),
                                     fill=COR_TEXTO, anchor="center")

    label_esqueci = canvas.create_text(0, 0, text="Esqueceu a senha?",
                                       font=("Arial", 10), fill=COR_TEXTO, anchor="center")

    btn_entrar = ctk.CTkButton(root, text="Entrar", font=("Arial", 15, "bold"),
                               fg_color="transparent", text_color=COR_TEXTO,
                               border_width=2, border_color=COR_TEXTO,
                               hover_color="#e0e0e0", width=350, height=45, corner_radius=25,
                               command=lambda: verificar_login(root, entry_login, entry_senha))
    canvas_btn_entrar_id = canvas.create_window(0, 0, window=btn_entrar, anchor="center")

    label_ou = canvas.create_text(0, 0, text="OU", font=("Arial", 12, "bold"),
                                  fill=COR_TEXTO, anchor="center")
    label_criar = canvas.create_text(0, 0, text="CRIAR CONTA", font=("Arial", 14, "bold"),
                                     fill=COR_TEXTO, anchor="center")

    img_softcar_path = "assets/img_softcar.png"
    softcar_pil = None
    softcar_tk = None
    if os.path.exists(img_softcar_path):
        softcar_pil = Image.open(img_softcar_path).copy()
        softcar_tk = ImageTk.PhotoImage(softcar_pil)
    logo_id = None

    def on_criar_conta(event):
        messagebox.showinfo("Criar Conta", "Funcionalidade em desenvolvimento.")

    def on_esqueci(event):
        messagebox.showinfo("Recuperar Senha", "Funcionalidade em desenvolvimento.")

    canvas.tag_bind(label_criar, "<Button-1>", on_criar_conta)
    canvas.tag_bind(label_criar, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(label_criar, "<Leave>", lambda e: canvas.config(cursor=""))
    canvas.tag_bind(label_esqueci, "<Button-1>", on_esqueci)
    canvas.tag_bind(label_esqueci, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(label_esqueci, "<Leave>", lambda e: canvas.config(cursor=""))

    root.bind("<Return>", lambda e: verificar_login(root, entry_login, entry_senha))

    def redimensionar(event):
        nonlocal bg_image_tk, softcar_tk
        if event.widget != root:
            return
        w, h = event.width, event.height
        if w < 10 or h < 10:
            return

        if bg_original:
            img_resized = bg_original.resize((w, h), Image.Resampling.LANCZOS)
            bg_image_tk = ImageTk.PhotoImage(img_resized)
            canvas.delete("bg")
            canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
            canvas.tag_lower("bg")

        cx = w * 0.5
        entry_w = min(350, int(w * 0.35))
        entry_h = 45

        font_size_title = max(24, int(36 * h / 800))
        font_size_label = max(11, int(14 * h / 800))
        font_size_small = max(9, int(10 * h / 800))
        font_size_btn = max(12, int(15 * h / 800))

        canvas.itemconfig(label_titulo, font=("Arial", font_size_title, "bold"))
        canvas.itemconfig(label_usuario, font=("Arial", font_size_label, "bold"))
        canvas.itemconfig(label_senha, font=("Arial", font_size_label, "bold"))
        canvas.itemconfig(label_esqueci, font=("Arial", font_size_small))
        canvas.itemconfig(label_ou, font=("Arial", font_size_small, "bold"))
        canvas.itemconfig(label_criar, font=("Arial", font_size_label, "bold"))

        cy_titulo = h * 0.20
        cy_email_label = h * 0.30
        cy_email = h * 0.36
        cy_senha_label = h * 0.44
        cy_senha = h * 0.50
        cy_esqueci = h * 0.56
        cy_entrar = h * 0.64
        cy_ou = h * 0.72
        cy_criar = h * 0.77

        canvas.coords(label_titulo, cx, cy_titulo)
        canvas.coords(label_usuario, cx, cy_email_label)
        canvas.coords(canvas_login_id, cx, cy_email)
        canvas.coords(label_senha, cx, cy_senha_label)
        canvas.coords(canvas_senha_id, cx, cy_senha)
        canvas.coords(canvas_btn_senha_id, cx + entry_w // 2 + 24, cy_senha)
        canvas.coords(label_esqueci, cx, cy_esqueci)
        canvas.coords(canvas_btn_entrar_id, cx, cy_entrar)
        canvas.coords(label_ou, cx, cy_ou)
        canvas.coords(label_criar, cx, cy_criar)

        canvas.delete("logo")
        if softcar_pil:
            logo_w = max(80, int(160 * w / 1200))
            logo_h = max(40, int(80 * w / 1200))
            logo_resized = softcar_pil.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            softcar_tk = ImageTk.PhotoImage(logo_resized)
            logo_x = w - logo_w // 2 - 30
            logo_y = h - logo_h // 2 - 20
            logo_id = canvas.create_image(logo_x, logo_y, image=softcar_tk, anchor="center", tags="logo")

    root.bind("<Configure>", redimensionar)

    def iniciar():
        root.update_idletasks()
        w = root.winfo_width()
        h = root.winfo_height()

        class FakeEvent:
            pass
        ev = FakeEvent()
        ev.widget = root
        ev.width = w
        ev.height = h
        redimensionar(ev)

    root.after(100, iniciar)
    root.mainloop()


if __name__ == "__main__":
    tela_login()
