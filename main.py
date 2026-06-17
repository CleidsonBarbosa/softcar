import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector  # Importação do conector MySQL
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
            root.destroy()          # fecha o login
            tela_dashboard()        # abre o dashboard
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
    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # --- TEXTOS DE IDENTIFICAÇÃO ---
    canvas.create_text(645, 255, text="Usuário / E-mail", font=("Arial", 11, "bold"), fill="white")
    canvas.create_text(645, 345, text="Senha", font=("Arial", 11, "bold"), fill="white")

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
        command=lambda: verificar_login(root, entry_login, entry_senha)
    )
    canvas.create_window(645, 432, window=btn_entrar)

    canvas.image = bg_image
    root.mainloop()

if __name__ == "__main__":
    tela_login()
