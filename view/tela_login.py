#import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def tela_login():
    root = ctk.CTk()
    root.title("Soft Car - Login")
    root.geometry("800x600")
    root.resizable(True, True)

    img_path = "assets/Login.png"

    if not os.path.exists(img_path):
        print(f"Erro: Arquivo '{img_path}' não encontrado.")
        return

    # 1. Carrega o plano de fundo
    img = Image.open(img_path)
    img = img.resize((800, 600), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(img)

    # 2. Configura o Canvas
    canvas = ctk.CTkCanvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # --- TEXTOS DE IDENTIFICAÇÃO (Novidade) ---
    # Texto descritivo acima do campo de login
    canvas.create_text(645, 255, text="Usuário / E-mail", font=("Arial", 11, "bold"), fill="white")
    
    # Texto descritivo acima do campo de senha
    canvas.create_text(645, 345, text="Senha", font=("Arial", 11, "bold"), fill="white")
    # ------------------------------------------

    # 3. Campo de texto para o LOGIN
    entry_login = ctk.CTkEntry(root, font=("Inclusive Sans", 13, "bold"), border_width=2, corner_radius=10, placeholder_text="E-mail", fg_color="#c2c7cc", text_color="#333333", border_color="#304C62")
    canvas.create_window(645, 278, window=entry_login)

    # 4. Campo de texto para a SENHA
    entry_senha = ctk.CTkEntry(root, font=("Inclusive Sans", 13, "bold"), border_width=2, corner_radius=10, placeholder_text="Senha", show="*", fg_color="#c2c7cc", text_color="#333333", border_color="#304C62")
    canvas.create_window(645, 368, window=entry_senha, width=250, height=35)

    # Botão olho para mostrar/esconder senha
    senha_visivel = False

    def toggle_senha():
        nonlocal senha_visivel
        senha_visivel = not senha_visivel
        entry_senha.configure(show="" if senha_visivel else "*")
        btn_olho.configure(text="🔓" if senha_visivel else "🔒")

    btn_olho = ctk.CTkButton(root, text="🔒", width=40, corner_radius=0, fg_color="#c2c7cc", hover_color="#b0b5b9", text_color="#333333", font=("Arial", 20), command=toggle_senha, border_width=0)
    canvas.create_window(750, 368, window=btn_olho, width=40, height=35)
    
    # 5. Botão ENTRAR
    btn_entrar = ctk.CTkButton(
        root, 
        text="Entrar", 
        font=("Arial", 11, "bold"), 
        bg="#b0b5b9", 
        fg="#333333", 
        activebackground="#c2c7cc",
        bd=0, 
        width=9, 
        height=1,
    )
    canvas.create_window(645, 432, window=btn_entrar)

    canvas.image = bg_image
    root.mainloop()

if __name__ == "__main__":
    tela_login()
