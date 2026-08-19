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
        bg_original = Image.open(img_bg_path)

    canvas = ctk.CTkCanvas(root, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)

    bg_image_tk = None

    entry_font = ctk.CTkFont(family="Arial", size=14, weight="bold")

    entry_login = ctk.CTkEntry(root, font=entry_font, border_width=2, corner_radius=10,
                               placeholder_text="E-mail", fg_color="#c2c7cc", text_color="#333333",
                               border_color=COR_DESTAQUE, width=300, height=40)
    entry_senha = ctk.CTkEntry(root, font=entry_font, border_width=2, corner_radius=10,
                               placeholder_text="Senha", show="*", fg_color="#c2c7cc", text_color="#333333",
                               border_color=COR_DESTAQUE, width=300, height=40)

    canvas_login_id = canvas.create_window(0, 0, window=entry_login, anchor="center")
    canvas_senha_id = canvas.create_window(0, 0, window=entry_senha, anchor="center")

    eye_open_pil = _make_eye_icon(24, open_eye=True)
    eye_closed_pil = _make_eye_icon(24, open_eye=False)
    eye_open_tk = ctk.CTkImage(light_image=eye_open_pil, dark_image=eye_open_pil, size=(24, 24))
    eye_closed_tk = ctk.CTkImage(light_image=eye_closed_pil, dark_image=eye_closed_pil, size=(24, 24))

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
                                    fg_color=COR_DESTAQUE, text_color=COR_BRANCO,
                                    hover_color="#2c4a5c", width=38, height=38, corner_radius=8,
                                    command=toggle_senha)
    canvas_btn_senha_id = canvas.create_window(0, 0, window=btn_visualizar, anchor="center")

    btn_entrar = ctk.CTkButton(root, text="Entrar", font=("Arial", 15, "bold"),
                                fg_color=COR_DOURADO, text_color=COR_BRANCO,
                                hover_color="#d4a857", width=300, height=45, corner_radius=10,
                                command=lambda: verificar_login(root, entry_login, entry_senha))
    canvas_btn_entrar_id = canvas.create_window(0, 0, window=btn_entrar, anchor="center")

    label_usuario = canvas.create_text(0, 0, text="E-mail", font=("Arial", 12, "bold"),
                                       fill=COR_BRANCO, anchor="w")
    label_senha = canvas.create_text(0, 0, text="Senha", font=("Arial", 12, "bold"),
                                     fill=COR_BRANCO, anchor="w")

    root.bind("<Return>", lambda e: verificar_login(root, entry_login, entry_senha))

    def redimensionar(event):
        nonlocal bg_image_tk
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

        cx = w * 0.75
        entry_w = min(320, int(w * 0.28))
        entry_h = 42
        font_size = max(11, int(14 * h / 700))
        entry_font.configure(size=font_size)

        canvas.itemconfig(canvas_login_id, width=entry_w, height=entry_h)
        canvas.itemconfig(canvas_senha_id, width=entry_w, height=entry_h)

        cy_email_label = h * 0.37
        cy_email = h * 0.42
        cy_senha_label = h * 0.51
        cy_senha = h * 0.56
        cy_entrar = h * 0.68

        canvas.coords(canvas_login_id, cx, cy_email)
        canvas.coords(canvas_senha_id, cx, cy_senha)
        canvas.coords(canvas_btn_senha_id, cx + entry_w // 2 + 28, cy_senha)
        canvas.coords(canvas_btn_entrar_id, cx, cy_entrar)

        canvas.coords(label_usuario, cx - entry_w // 2, cy_email_label)
        canvas.coords(label_senha, cx - entry_w // 2, cy_senha_label)

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
