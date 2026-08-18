import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector


def verificar_login(root, entry_login, entry_senha):
    email = entry_login.get()
    senha = entry_senha.get()

    if email == "" or senha == "":
        messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
        return

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="softcar"
        )
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE email_func = %s AND senha = %s", (email, senha))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()

        if resultado:
            cargo = resultado[5]
            from app import App
            App(root, cargo=cargo)
        else:
            messagebox.showerror("Erro", "Usuario ou senha incorretos.")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro de Conexao", f"Falha ao conectar ao banco:\n{erro}")


def tela_login():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.title("Soft Car - Login")
    root.geometry("800x600")
    root.minsize(600, 450)
    root.resizable(True, True)
    root.state("zoomed")
    try:
        root.attributes('-zoomed', True)
    except:
        pass

    img_path = "assets/Login.png"

    if not os.path.exists(img_path):
        print(f"Erro: Arquivo '{img_path}' não encontrado.")
        return

    img_original = Image.open(img_path)

    canvas = ctk.CTkCanvas(root, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)

    bg_image_ctk = None

    entry_login_font = ctk.CTkFont(family="Inclusive Sans", size=13, weight="bold")
    entry_senha_font = ctk.CTkFont(family="Inclusive Sans", size=13, weight="bold")

    entry_login = ctk.CTkEntry(root, font=entry_login_font, border_width=0, corner_radius=10, placeholder_text="E-mail", fg_color="#c2c7cc", text_color="#333333", border_color="#304C62")
    entry_senha = ctk.CTkEntry(root, font=entry_senha_font, border_width=0, corner_radius=10, placeholder_text="Senha", show="*", fg_color="#c2c7cc", text_color="#333333", border_color="#EE1101")

    canvas_login_window = canvas.create_window(0, 0, window=entry_login, width=250, height=35)
    canvas_senha_window = canvas.create_window(0, 0, window=entry_senha, width=250, height=35)

    img_email_pil = Image.open("assets/txt_email.png") if os.path.exists("assets/txt_email.png") else None
    img_senha_pil = Image.open("assets/txt_senha.png") if os.path.exists("assets/txt_senha.png") else None
    img_entrar_pil = Image.open("assets/btn_entrar.png") if os.path.exists("assets/btn_entrar.png") else None

    text_usuario_id = None
    text_senha_id = None
    btn_entrar_img_id = None
    canvas_btn_window = None

    root.bind("<Return>", lambda e: verificar_login(root, entry_login, entry_senha))

    def redimensionar(event):
        nonlocal bg_image_ctk, btn_entrar_img_id, canvas_btn_window, text_usuario_id, text_senha_id
        if event.widget != root:
            return
        w, h = event.width, event.height
        if w < 10 or h < 10:
            return

        img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
        bg_image_ctk = ImageTk.PhotoImage(img_resized)
        canvas.delete("bg")
        canvas.create_image(0, 0, image=bg_image_ctk, anchor="nw", tags="bg")
        canvas.tag_lower("bg")

        cx = w * 0.806
        cy_login = h * 0.463
        cy_senha = h * 0.613

        entry_w = int(250 * w / 800)
        entry_h = int(35 * h / 600)
        label_w = int(100 * w / 800)
        label_h = int(30 * h / 600)
        btn_w = int(100 * w / 800)
        btn_h = int(35 * h / 600)

        # Responsively resize font
        font_size = max(10, int(13 * h / 600))
        entry_login_font.configure(size=font_size)
        entry_senha_font.configure(size=font_size)

        entry_x = cx
        entry_w_canvas = entry_w

        canvas.itemconfig(canvas_login_window, width=entry_w, height=entry_h)
        canvas.itemconfig(canvas_senha_window, width=entry_w, height=entry_h)
        canvas.coords(canvas_login_window, entry_x, cy_login)
        canvas.coords(canvas_senha_window, entry_x, cy_senha)

        # Position label images at top-left of each entry
        entry_left = entry_x - entry_w // 2
        label_y_login = cy_login - entry_h // 2 - label_h - 2
        label_y_senha = cy_senha - entry_h // 2 - label_h - 2

        if img_email_pil:
            img_e_resized = img_email_pil.resize((label_w, label_h), Image.Resampling.LANCZOS)
            img_email_tk = ImageTk.PhotoImage(img_e_resized)
            canvas.image_email = img_email_tk
            if text_usuario_id is None:
                text_usuario_id = canvas.create_image(entry_left, label_y_login, image=img_email_tk, anchor="nw")
            else:
                canvas.itemconfig(text_usuario_id, image=img_email_tk)
                canvas.coords(text_usuario_id, entry_left, label_y_login)
        else:
            if text_usuario_id is None:
                text_usuario_id = canvas.create_text(entry_left, label_y_login, text="Usuário / E-mail", font=("Arial", 11, "bold"), fill="white", anchor="nw")
            else:
                canvas.coords(text_usuario_id, entry_left, label_y_login)

        if img_senha_pil:
            img_s_resized = img_senha_pil.resize((label_w, label_h), Image.Resampling.LANCZOS)
            img_senha_tk = ImageTk.PhotoImage(img_s_resized)
            canvas.image_senha = img_senha_tk
            if text_senha_id is None:
                text_senha_id = canvas.create_image(entry_left, label_y_senha, image=img_senha_tk, anchor="nw")
            else:
                canvas.itemconfig(text_senha_id, image=img_senha_tk)
                canvas.coords(text_senha_id, entry_left, label_y_senha)
        else:
            if text_senha_id is None:
                text_senha_id = canvas.create_text(entry_left, label_y_senha, text="Senha", font=("Arial", 11, "bold"), fill="white", anchor="nw")
            else:
                canvas.coords(text_senha_id, entry_left, label_y_senha)

        btn_y = h * 0.72

        if img_entrar_pil:
            img_e_resized = img_entrar_pil.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
            img_entrar_tk = ImageTk.PhotoImage(img_e_resized)
            canvas.image_entrar = img_entrar_tk
            if btn_entrar_img_id is None:
                btn_entrar_img_id = canvas.create_image(entry_x, btn_y, image=img_entrar_tk, anchor="center")
                canvas.tag_bind(btn_entrar_img_id, "<Button-1>", lambda e: verificar_login(root, entry_login, entry_senha))
            else:
                canvas.itemconfig(btn_entrar_img_id, image=img_entrar_tk)
                canvas.coords(btn_entrar_img_id, entry_x, btn_y)
        else:
            if canvas_btn_window is None:
                btn_entrar_widget = ctk.CTkButton(
                    root,
                    text="Entrar",
                    font=("Inclusive Sans", 13, "bold"),
                    width=btn_w,
                    height=btn_h,
                    command=lambda: verificar_login(root, entry_login, entry_senha)
                )
                canvas_btn_window = canvas.create_window(entry_x, btn_y, window=btn_entrar_widget, anchor="center")
            else:
                canvas.coords(canvas_btn_window, entry_x, btn_y)

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
