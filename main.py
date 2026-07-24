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

    img_path = "assets/Login.png"

    if not os.path.exists(img_path):
        print(f"Erro: Arquivo '{img_path}' não encontrado.")
        return

    img_original = Image.open(img_path)

    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    bg_image_tk = None

    entry_login = tk.Entry(root, font=("Arial", 13), bd=2, bg="#c2c7cc", justify="center")
    entry_senha = tk.Entry(root, font=("Arial", 13), bd=2, bg="#c2c7cc", show="*", justify="center")

    canvas_login_window = canvas.create_window(0, 0, window=entry_login)
    canvas_senha_window = canvas.create_window(0, 0, window=entry_senha)

    text_usuario = canvas.create_text(0, 0, text="Usuário / E-mail", font=("Arial", 11, "bold"), fill="white")
    text_senha = canvas.create_text(0, 0, text="Senha", font=("Arial", 11, "bold"), fill="white")

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
    canvas_btn_window = canvas.create_window(0, 0, window=btn_entrar)

    root.bind("<Return>", lambda e: verificar_login(root, entry_login, entry_senha))

    def redimensionar(event):
        nonlocal bg_image_tk
        if event.widget != root:
            return
        w, h = event.width, event.height
        if w < 10 or h < 10:
            return

        img_resized = img_original.resize((w, h), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(img_resized)
        canvas.delete("bg")
        canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
        canvas.tag_lower("bg")

        cx = w * 0.806
        canvas.coords(text_usuario, cx, h * 0.425)
        canvas.coords(canvas_login_window, cx, h * 0.463)
        canvas.coords(text_senha, cx, h * 0.575)
        canvas.coords(canvas_senha_window, cx, h * 0.613)
        canvas.coords(canvas_btn_window, cx, h * 0.720)

    root.bind("<Configure>", redimensionar)
    root.after(100, lambda: [root.update_idletasks(), redimensionar(type('Event', (), {'widget': root, 'width': root.winfo_width(), 'height': root.winfo_height()})())])

    root.mainloop()

if __name__ == "__main__":
    tela_login()
