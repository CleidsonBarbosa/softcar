import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def tela_login():
    root = tk.Tk()
    root.title("Soft Car - Login")
    root.geometry("800x600")
    root.resizable(True, True)

    img_path = "login.png"

    if not os.path.exists(img_path):
        print(f"Erro: Arquivo '{img_path}' não encontrado.")
        return

    # 1. Carrega o plano de fundo
    img = Image.open(img_path)
    img = img.resize((800, 600), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(img)

    # 2. Configura o Canvas
    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # --- TEXTOS DE IDENTIFICAÇÃO (Novidade) ---
    # Texto descritivo acima do campo de login
    canvas.create_text(645, 255, text="Usuário / E-mail", font=("Arial", 11, "bold"), fill="white")
    
    # Texto descritivo acima do campo de senha
    canvas.create_text(645, 345, text="Senha", font=("Arial", 11, "bold"), fill="white")
    # ------------------------------------------

    # 3. Campo de texto para o LOGIN
    entry_login = tk.Entry(root, font=("Arial", 13), width=24, bd=2, bg="#c2c7cc", justify="center")
    canvas.create_window(645, 278, window=entry_login)

    # 4. Campo de texto para a SENHA
    entry_senha = tk.Entry(root, font=("Arial", 13), width=24, bd=2, bg="#c2c7cc", show="*", justify="center")
    canvas.create_window(645, 368, window=entry_senha)
    
    # 5. Botão ENTRAR
    btn_entrar = tk.Button(
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
