import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from view.bemvindo import tela_dashboard
def verificar_login(root, entry_login, entry_senha):
    email = entry_login.get()
    senha = entry_senha.get()

    if email == "" or senha == "":
        messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
        return

    try:
        # Configuração da conexão com o banco de dados
        conexao = mysql.connector.connect(
            host="localhost",       
            user="root",            
            password="",    # Substitua pela sua senha do MySQL
            database="softcar"         # Nome do banco atualizado para 'banco'
        )
        
        cursor = conexao.cursor()
        
        # Consulta SQL atualizada para a tabela 'funcionarios'
        comando = "SELECT * FROM funcionarios WHERE email_func = %s AND senha = %s"
        cursor.execute(comando, (email, senha))
        resultado = cursor.fetchone()
        
        if resultado:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            # INSIRA AQUI a chamada para abrir a sua próxima tela
            cargo = resultado[5]        # índice do campo 'cargo'
            root.destroy()              # fecha o login
            tela_dashboard(cargo)       # abre o dashboard com o cargo
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
            
        cursor.close()
        conexao.close()
        
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro de Conexão", f"Falha ao conectar ao banco:\n{erro}")


def tela_login():
    root = tk.Tk()
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

    canvas = tk.Canvas(root, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)

    bg_image_ctk = None

    entry_login = ctk.CTkEntry(root, font=("Inclusive Sans", 13, "bold"), border_width=2, corner_radius=10, placeholder_text="E-mail", fg_color="#c2c7cc", text_color="#333333", border_color="#000000")
    entry_senha = ctk.CTkEntry(root, font=("Inclusive Sans", 13, "bold"), border_width=2, corner_radius=10, placeholder_text="Senha", show="*", fg_color="#c2c7cc", text_color="#333333", border_color="#000000")

    canvas_login_window = canvas.create_window(0, 0, window=entry_login, width=250, height=35)
    canvas_senha_window = canvas.create_window(0, 0, window=entry_senha, width=250, height=35)

    img_email = None
    if os.path.exists("assets/txt_email.png"):
        img_e = Image.open("assets/txt_email.png")
        img_e = img_e.resize((100, 30), Image.Resampling.LANCZOS)
        img_email = ImageTk.PhotoImage(img_e)

    if img_email:
        text_usuario = canvas.create_image(0, 0, image=img_email, anchor="nw")
        canvas.image_email = img_email
    else:
        text_usuario = canvas.create_text(0, 0, text="Usuário / E-mail", font=("Arial", 11, "bold"), fill="white")

    img_senha = None
    if os.path.exists("assets/txt_senha.png"):
        img_s = Image.open("assets/txt_senha.png")
        img_s = img_s.resize((100, 25), Image.Resampling.LANCZOS)
        img_senha = ImageTk.PhotoImage(img_s)

    if img_senha:
        text_senha = canvas.create_image(0, 0, image=img_senha, anchor="nw")
        canvas.image_senha = img_senha
    else:
        text_senha = canvas.create_text(0, 0, text="Senha", font=("Arial", 11, "bold"), fill="white")

    img_entrar = None
    if os.path.exists("assets/btn_entrar.png"):
        img_e = Image.open("assets/btn_entrar.png")
        img_e = img_e.resize((100, 35), Image.Resampling.LANCZOS)
        img_entrar = ImageTk.PhotoImage(img_e)

    if img_entrar:
        btn_entrar = canvas.create_image(0, 0, image=img_entrar, anchor="nw")
        canvas.tag_bind(btn_entrar, "<Button-1>", lambda e: verificar_login(root, entry_login, entry_senha))
        canvas.image_entrar = img_entrar
        btn_entrar_img = btn_entrar
    else:
        btn_entrar = ctk.Button(
            root,
            text="Entrar",
            font=("Arial", 11, "bold"),
            bg="#b0b5b9",
            fg="#333333",
            activebackground="#c2c7cc",
            bd=0,
            width=9,
            height=1,
            command=lambda: verificar_login(root, entry_login, entry_senha)
        )
        canvas_btn_window = canvas.create_window(0, 0, window=btn_entrar)

    root.bind("<Return>", lambda e: verificar_login(root, entry_login, entry_senha))

    def redimensionar(event):
        nonlocal bg_image_ctk
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

        canvas.coords(text_usuario, cx - 125, cy_login - 50)
        canvas.coords(canvas_login_window, cx, cy_login)
        canvas.coords(text_senha, cx - 125, cy_senha - 45)
        canvas.coords(canvas_senha_window, cx, cy_senha)

        if 'btn_entrar_img' in locals() or 'btn_entrar_img' in globals():
            canvas.coords(btn_entrar_img, cx - 50, h * 0.68)
        else:
            canvas.coords(canvas_btn_window, cx, h * 0.68)

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
