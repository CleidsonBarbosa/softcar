
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def tela_dashboard():
    root = tk.Tk()
    root.title("Soft Car - Dashboard")
    
    # CORREÇÃO: Removido o "=" intruso. O formato correto é "LARGURAxALTURA"
    root.geometry("1000x630") 
    root.minsize(800, 500)
    root.resizable(True, True)

    img_path = "assets/Dashboard.png"  

    if not os.path.exists(img_path):
        print(f"Erro: Arquivo '{img_path}' não encontrado.")
        return

    img_original = Image.open(img_path)

    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    cor_menu = "#2b3e50" 

    def acao_menu(opcao):
        messagebox.showinfo("Soft Car", f"Você clicou na opção: {opcao}")

    btn_cliente = tk.Button(root, text="Cliente", font=("Arial", 11, "bold"), fg="white", bg=cor_menu, 
                            activebackground="#3a536b", activeforeground="white", bd=0, anchor="w", padx=10,
                            command=lambda: acao_menu("Cliente"))
    window_cliente = canvas.create_window(0, 0, window=btn_cliente, anchor="w")

    btn_servicos = tk.Button(root, text="Serviços", font=("Arial", 11, "bold"), fg="white", bg=cor_menu, 
                             activebackground="#3a536b", activeforeground="white", bd=0, anchor="w", padx=10,
                             command=lambda: acao_menu("Serviços"))
    window_servicos = canvas.create_window(0, 0, window=btn_servicos, anchor="w")

    btn_funcionarios = tk.Button(root, text="Funcionários", font=("Arial", 11, "bold"), fg="white", bg=cor_menu, 
                                 activebackground="#3a536b", activeforeground="white", bd=0, anchor="w", padx=10,
                                 command=lambda: acao_menu("Funcionários"))
    window_funcionarios = canvas.create_window(0, 0, window=btn_funcionarios, anchor="w")

    btn_materiais = tk.Button(root, text="Materiais", font=("Arial", 11, "bold"), fg="white", bg=cor_menu, 
                              activebackground="#3a536b", activeforeground="white", bd=0, anchor="w", padx=10,
                              command=lambda: acao_menu("Materiais"))
    window_materiais = canvas.create_window(0, 0, window=btn_materiais, anchor="w")

    btn_relatorios = tk.Button(root, text="Relatórios", font=("Arial", 11, "bold"), fg="white", bg=cor_menu, 
                               activebackground="#3a536b", activeforeground="white", bd=0, anchor="w", padx=10,
                               command=lambda: acao_menu("Relatórios"))
    window_relatorios = canvas.create_window(0, 0, window=btn_relatorios, anchor="w")

    valor_agendados = canvas.create_text(0, 0, text="20", font=("Arial", 54, "bold"), fill="#b88b4a")
    valor_realizados = canvas.create_text(0, 0, text="31", font=("Arial", 54, "bold"), fill="#b88b4a")
    valor_clientes = canvas.create_text(0, 0, text="352", font=("Arial", 36, "bold"), fill="#b88b4a")
    valor_veiculos = canvas.create_text(0, 0, text="426", font=("Arial", 36, "bold"), fill="#b88b4a")
    valor_total = canvas.create_text(0, 0, text="R$ 863,00", font=("Arial", 64, "bold"), fill="#b88b4a", anchor="w")

    bg_image_tk = None  

    def redimensionar_dashboard(event):
        nonlocal bg_image_tk
        
        # CORREÇÃO CRÍTICA: Garante que o redimensionamento só trate a mudança da janela principal (root).
        # Sem isso, os sub-widgets disparam o evento de forma recursiva e quebram a interface.
        if event.widget != root:
            return

        if event.width < 10 or event.height < 10:
            return

        img_redimensionada = img_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(img_redimensionada)
        
        canvas.delete("bg")
        canvas.create_image(0, 0, image=bg_image_tk, anchor="nw", tags="bg")
        canvas.tag_lower("bg")

        raio_x_menu = event.width * 0.055  
        largura_botao = int(event.width * 0.11) 

        for btn, window_item, pct_y in [
            (btn_cliente, window_cliente, 0.33),
            (btn_servicos, window_servicos, 0.425),
            (btn_funcionarios, window_funcionarios, 0.52),
            (btn_materiais, window_materiais, 0.615),
            (btn_relatorios, window_relatorios, 0.71)
        ]:
            btn.configure(width=max(8, int(largura_botao / 8))) 
            canvas.coords(window_item, raio_x_menu, event.height * pct_y)

        canvas.coords(valor_agendados, event.width * 0.315, event.height * 0.28)
        canvas.coords(valor_realizados, event.width * 0.562, event.height * 0.28)
        canvas.coords(valor_clientes, event.width * 0.812, event.height * 0.17)
        canvas.coords(valor_veiculos, event.width * 0.812, event.height * 0.36)
        
        canvas.coords(valor_total, event.width * 0.23, event.height * 0.68)

    root.bind("<Configure>", redimensionar_dashboard)
    root.mainloop()

if __name__ == "__main__":
    tela_dashboard()